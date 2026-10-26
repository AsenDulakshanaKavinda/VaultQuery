
import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Index, String, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from data_onboarding.core import get_settings

settings = get_settings()

engine = create_engine(
    settings.secrets.async_database_url,
    echo=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

class Base(DeclarativeBase):
    ...

class DocumentState(Base):
    __tablename__ = "document_state"

    source_system: Mapped[str] = mapped_column(String(64), primary_key=True, nullable=False)
    source_id: Mapped[str] = mapped_column(String(512), primary_key=True, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    acl_groups_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    last_synced_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # Maps to: CREATE INDEX IF NOT EXISTS idx_doc_state_system ON document_state(source_system);
    __table_args__ = (
        Index("idx_doc_state_system", "source_system"),
    )


class Database:
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
                        db_url,
                        pool_size=5,
                        max_overflow=10,
                        echo=False
                    )

                    instance.session_factory = async_sessionmaker(
                        bind=instance.engine,
                        autoflush=False,
                        expire_on_commit=False,
                        class_=AsyncSession
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