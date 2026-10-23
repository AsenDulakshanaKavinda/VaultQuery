





from data_onboarding.acl.mapper import AclMapper
from data_onboarding.chunkers.token_chunker import TokenChunker
from data_onboarding.connectors.base import BaseConnector
from data_onboarding.processing.parsers.layout_parser import LayoutParser
from data_onboarding.storage.qdrant_store import QdrantVectorStore


class IngestionPipeline:
    def __init__(
        self,
        connector: BaseConnector,
        mapper: AclMapper,
        chunker: TokenChunker,
        embedder,
        vector_store: QdrantVectorStore,
        source_system_name: str,
    ):
        self.connector = connector
        self.mapper = mapper
        self.chunker = chunker
        self.embedder = embedder
        self.vector_store = vector_store
        self.source_system = source_system_name

    async def run(self):
        async for source_id in self.connector.list_changes():
            file_bytes, hints = await self.connector.fetch(source_id)

            decision = self.mapper.map(self.source_system, hints)

            markdown_text = LayoutParser.parse(file_bytes, source_id)

            chunks = self.chunker.chunk(markdown_text, document_id=source_id)

            texts = [c.text for c in chunks]
            vectors = self.embedder.embed(texts)

            payload_template = {
                "source_system": self.source_system,
                "source_id": source_id,
                "allowed_groups": list(decision.allowed_groups),
                "rule_id": decision.rule_id,
                "model_name": self.embedder.model_name,
            }

            self.vector_store.upsert_chunks(chunks, vectors, payload_template)







