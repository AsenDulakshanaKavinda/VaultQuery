import asyncio
import hashlib
import json
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import List, Optional, Tuple

from sqlalchemy import DateTime, Index, String, create_engine, delete, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from data_onboarding.core import get_settings

settings = get_settings()

async_database_url = settings.secrets.async_database_url
if not async_database_url:
    raise ValueError("async database url can not be None")

engine = create_engine(async_database_url, echo=True, pool_size=10, max_overflow=20)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase): ...


class DocumentState(Base):
    """represent the state of a document in the db, including its content hash, ACL hash and last synced timestamp."""

    __tablename__ = "document_state"

    source_system: Mapped[str] = mapped_column(
        String(64), primary_key=True, nullable=False
    )
    source_id: Mapped[str] = mapped_column(
        String(512), primary_key=True, nullable=False
    )
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    acl_groups_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    last_synced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    # Maps to: CREATE INDEX IF NOT EXISTS idx_doc_state_system ON document_state(source_system);
    __table_args__ = (Index("idx_doc_state_system", "source_system"),)


class Database:
    """Singleton class to manage async SQLAlchemy engine and session factory. Ensures thread/task-safe initialization."""

    _instance: Optional["Database"] = None
    _lock: asyncio.Lock = asyncio.Lock()
    engine: AsyncEngine
    session_factory: async_sessionmaker[AsyncSession]

    @classmethod
    async def get_instance(cls, db_url: str = "") -> "Database":
        """Async thread/task-safe singleton retriever."""
        if cls._instance is None:
            async with cls._lock:
                if cls._instance is None:
                    if not db_url:
                        raise ValueError(
                            "Database URL must be provided on first initialization."
                        )

                    instance = super().__new__(cls)

                    print("Initializing Async SQLAlchemy Engine and SessionFactory...")
                    instance.engine = create_async_engine(
                        db_url, pool_size=5, max_overflow=10, echo=False
                    )

                    instance.session_factory = async_sessionmaker(
                        bind=instance.engine,
                        autoflush=False,
                        expire_on_commit=False,
                        class_=AsyncSession,
                    )

                    cls._instance = instance

        return cls._instance

    def get_session(self) -> AsyncSession:
        """Creates a new AsyncSession from the session factory."""
        return self.session_factory()


@asynccontextmanager
async def get_db_session(db_url: str) -> AsyncGenerator[AsyncSession, None]:
    """Async context manager for safely managing database sessions."""
    db = await Database.get_instance(db_url)
    session = db.get_session()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


"""
    PostgresStateStore act as persistent ledger and memory between synchronization runs
    1. When the pipeline runs a sync, it checks the live file's hash against the stored hash. If the file hasn't changed, the pipeline skips chunking and embedding completely
    2. In enterprise systems like SharePoint or S3, files are frequently moved between folders. If a document moves from a public folder to a restricted C-Suite folder, its content hasn't changed, but its access permissions have. The state store detects this ACL change, allowing the pipeline to update the Qdrant payload directly (changing the allowed_groups metadata) without re-embedding the document.
    3. If an object is deleted or removed from S3, SharePoint, or Jira, the pipeline compares the active live items against the state store. Any document present in the state store but missing from the live source is flagged as a tombstone, triggering the automatic removal of its vectors from Qdrant to ensure stale or deleted data doesn't remain searchable.
    4. Network failures, pipeline crashes, or scheduled cron jobs can cause syncs to overlap or restart midway. The state store (backed by a composite primary key on source_system and source_id) ensures that running the ingestion pipeline multiple times is entirely safe and idempotent—it will update state rather than duplicate vector points or corrupt tracking data.
    """


class PostgresStateStore:
    """Persistent state store for document hashes and ACLs, backed by PostgreSQL."""

    def __init__(self, db_url: str):
        self.db_url = db_url

    async def get_state(
        self, source_system: str, source_id: str
    ) -> Optional[Tuple[str, str]]:
        """Returns (content_hash, acl_groups_hash) if exists."""
        db = await Database.get_instance(self.db_url)
        async with db.session_factory() as session:
            stmt = select(
                DocumentState.content_hash, DocumentState.acl_groups_hash
            ).where(
                DocumentState.source_system == source_system,
                DocumentState.source_id == source_id,
            )
            result = await session.execute(stmt)
            row = result.first()
            if row:
                return row.content_hash, row.acl_groups_hash
        return None

    async def upsert_state(
        self,
        source_system: str,
        source_id: str,
        content_bytes: bytes,
        allowed_groups: List[str],
    ):
        """Upserts state using PostgreSQL native ON CONFLICT via SQLAlchemy construct."""
        content_hash = hashlib.sha256(content_bytes).hexdigest()
        acl_hash = self.compute_acl_hash(allowed_groups)
        sync_time = datetime.now(timezone.utc)

        db = await Database.get_instance(self.db_url)
        async with db.session_factory() as session:
            async with session.begin():
                stmt = pg_insert(DocumentState).values(
                    source_system=source_system,
                    source_id=source_id,
                    content_hash=content_hash,
                    acl_groups_hash=acl_hash,
                    last_synced_at=sync_time,
                )

                upsert_stmt = stmt.on_conflict_do_update(
                    index_elements=["source_system", "source_id"],
                    set_dict={
                        "content_hash": stmt.excluded.content_hash,
                        "acl_groups_hash": stmt.excluded.acl_groups_hash,
                        "last_synced_at": stmt.excluded.last_synced_at,
                    },
                )
                await session.execute(upsert_stmt)

    @staticmethod
    def compute_acl_hash(allowed_groups: List[str]) -> str:
        """Computes a deterministic hash for the list of allowed groups."""
        return hashlib.sha256(
            json.dumps(sorted(list(set(allowed_groups)))).encode()
        ).hexdigest()

    async def get_all_source_ids(self, source_system: str) -> list[str]:
        """returns all source_ids currently registered in the state store for a given system"""
        async with self.session_factory() as session:
            stmt = select(DocumentState.source_id).where(
                DocumentState.source_system == source_system
            )
            result = await session.scalars(stmt)
            return list(result.all())

    async def delete_states(self, source_system: str, source_ids: list[str]) -> None:
        """removes tracking state for tombstoned documents in bulk."""
        if not source_ids:
            return

        async with self.session_factory() as session:
            async with session.begin():
                stmt = delete(DocumentState).where(
                    DocumentState.source_system == source_system,
                    DocumentState.source_id.in_(source_ids),
                )
                await session.execute(stmt)
