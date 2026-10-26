from qdrant_client import QdrantClient, models


class QdrantVectorStore:
    def __init__(self, client: QdrantClient, collection_name: str = "vtl_knowledge"):
        self.client = client
        self.collection_name = collection_name

    def bootstrap_collection(self, vector_size: int = 1536):
        """responsible for creatingQdrantClient the collection if it doesn't exist yet"""
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

    def upsert_chunks(
        self, chunks: list, vectors: list[list[float]], payload_template: dict
    ):
        """responsible for upserting the chunks into the collection"""
        points = []
        for i, chunk in enumerate(chunks):
            payload = {
                **payload_template,
                "chunk_id": chunk.chunk_id,
                "text": chunk.text,
                "chunker_version": chunk.chunker_version,
            }
            points.append(
                models.PointStruct(
                    id=chunk.chunk_id,
                    vector=vectors[i],
                    payload=payload,
                )
            )
        self.client.upsert(collection_name=self.collection_name, points=points)
