from qdrant_client import QdrantClient
from qdrant_client import models
from functools import lru_cache

from knowledge_retrieval.core import get_settings

settings = get_settings()

class QdrantVectorStore:
    def __init__(self, client: QdrantClient, collection_name: str = "vtl_knowledge"):
        self.client = client
        self.collection_name = collection_name
        self.collection = self.bootstrap_collection()

    def bootstrap_collection(self, vector_size: int = 384):
        """responsible for creating QdrantClient the collection if it doesn't exist yet"""
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size, distance=models.Distance.COSINE
                ),
            )

            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="allowed_groups",
                field_schema=models.PayloadSchemaType.KEYWORD,
            )

@lru_cache(max_size=1)
def get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=settings.secrets.qdrant_url)    