

from functools import lru_cache
from pathlib import Path
from qdrant_client import QdrantClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from data_onboarding.core import get_settings
from data_onboarding.connectors.base import BaseConnector
from data_onboarding.connectors.s3 import S3Connector
from data_onboarding.acl.mapper import AclMapper
from data_onboarding.chunkers.token_chunker import TokenChunker
from data_onboarding.embedding.providers import LocalSentenceTransformerEmbedder
from data_onboarding.storage.qdrant_store import QdrantVectorStore
from data_onboarding.storage.state_store import PostgresStateStore
from data_onboarding.pipeline.ingest_pipeline import SmartIngestionPipeline

settings = get_settings()

# 1. Initialize Heavy Global Infrastructure Clients Once
@lru_cache(maxsize=1)
def get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=settings.secrets.qdrant_url)

# /home/rapter/projects/VaultQuery/data-onboarding/src/data_onboarding/core/settings.py
# .parent.parent.parent.parent points to the root 'data-onboarding/' directory
ROOT = Path(__file__).resolve().parent.parent.parent.parent

def get_config_path(filename: str) -> Path:
    """Returns the absolute path to any file inside the root 'config/' directory."""
    return ROOT / "config" / filename


@lru_cache(maxsize=1)
def get_session_factory() -> async_sessionmaker:
    engine = create_async_engine(settings.secrets.async_database_url, echo=False)
    return async_sessionmaker(engine, expire_on_commit=False)


@lru_cache(maxsize=1)
def get_embedder() -> LocalSentenceTransformerEmbedder:
    # Loaded into worker memory once
    return LocalSentenceTransformerEmbedder(model_name="all-MiniLM-L6-v2")


@lru_cache(maxsize=1)
def get_acl_mapper() -> AclMapper:
    # return AclMapper.from_yaml("acl_mapping.yaml")
    return AclMapper.from_yaml(get_config_path("acl_mapping.yaml"))


@lru_cache(maxsize=1)
def get_chunker() -> TokenChunker:
    return TokenChunker(chunk_size=512, overlap=64)


# 2. Connector Factory (M3.1)
def get_connector(source_system: str) -> BaseConnector:
    """Returns the appropriate connector implementation based on the source system name."""
    system_lower = source_system.lower()
    
    if system_lower in ("s3", "minio"):
        return S3Connector(bucket_name=settings.secrets.s3_bucket_name)
    elif system_lower == "sharepoint":
        # Example for future connectors
        # from data_onboarding.connectors.sharepoint_connector import SharePointConnector
        # return SharePointConnector()
        raise NotImplementedError("SharePoint connector not yet implemented")
    
    raise ValueError(f"Unknown source system: {source_system}")


# 3. Smart Pipeline Factory
def get_smart_pipeline(source_system: str) -> SmartIngestionPipeline:
    """Wires up and returns a fully initialized SmartIngestionPipeline for the given source."""
    connector = get_connector(source_system)
    mapper = get_acl_mapper()
    chunker = get_chunker()
    embedder = get_embedder()
    
    vector_store = QdrantVectorStore(client=get_qdrant_client(), collection_name="vtl_knowledge")
    vector_store.bootstrap_collection()


    # state_store = PostgresStateStore(session_factory=get_session_factory())
    state_store = PostgresStateStore(settings.secrets.async_database_url)

    return SmartIngestionPipeline(
        connector=connector,
        mapper=mapper,
        chunker=chunker,
        embedder=embedder,
        vector_store=vector_store,
        state_store=state_store,
        source_system_name=source_system,
    )