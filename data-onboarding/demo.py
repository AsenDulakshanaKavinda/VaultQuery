import asyncio

from huggingface_hub import login
from qdrant_client import QdrantClient

from data_onboarding.acl.mapper import AclMapper
from data_onboarding.chunkers.token_chunker import TokenChunker
from data_onboarding.connectors.s3 import S3Connector
from data_onboarding.core.settings import get_settings
from data_onboarding.embedding.providers import LocalSentenceTransformerEmbedder
from data_onboarding.pipeline.ingest_pipeline import IngestionPipeline, SmartIngestionPipeline
from data_onboarding.storage.qdrant_store import QdrantVectorStore
from data_onboarding.storage.state_store import PostgresStateStore

settings = get_settings()

login(token=settings.secrets.hf_token_read)


async def run_pipeline():
    connector = S3Connector(bucket_name="vtl-enterprise-docs-prod")
    mapper = AclMapper.from_yaml("./config/acl_mapping.yaml")
    chunker = TokenChunker(chunk_size=512, overlap=64)

    embedder = LocalSentenceTransformerEmbedder(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_store = QdrantVectorStore(client=QdrantClient(url="http://localhost:6333"))

    in_pipeline = IngestionPipeline(
        connector=connector,
        mapper=mapper,
        chunker=chunker,
        embedder=embedder,
        vector_store=vector_store,
        source_system_name="s3",
    )

    await in_pipeline.run()

async def run_smart_pipeline():
    connector = S3Connector(bucket_name="vtl-enterprise-docs-prod")
    mapper = AclMapper.from_yaml("./config/acl_mapping.yaml")
    chunker = TokenChunker(chunk_size=512, overlap=64)

    embedder = LocalSentenceTransformerEmbedder(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_store = QdrantVectorStore(client=QdrantClient(url="http://localhost:6333"))
    state_store = PostgresStateStore(db_url=settings.secrets.async_database_url)

    smart_pipeline = SmartIngestionPipeline(
        connector=connector,
        mapper=mapper,
        chunker=chunker,
        embedder=embedder,
        vector_store=vector_store,
        state_store=state_store,
        source_system_name="s3",
    )

if __name__ == "__main__":
    asyncio.run(run_smart_pipeline())
