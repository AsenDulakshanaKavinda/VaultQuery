from data_onboarding.acl.mapper import AclMapper
from data_onboarding.chunkers.token_chunker import TokenChunker
from data_onboarding.connectors.base import BaseConnector
from data_onboarding.domain.ids import make_doc_id
from data_onboarding.embedding.providers import LocalSentenceTransformerEmbedder
from data_onboarding.processing.parsers.layout_parser import LayoutParser
from data_onboarding.storage.qdrant_store import QdrantVectorStore


class IngestionPipeline:
    def __init__(
        self,
        connector: BaseConnector,
        mapper: AclMapper,
        chunker: TokenChunker,
        embedder: LocalSentenceTransformerEmbedder,
        vector_store: QdrantVectorStore,
        source_system_name: str,
    ):
        self.connector = connector
        self.mapper = mapper
        self.chunker = chunker
        self.embedder = embedder
        self.vector_store = vector_store
        self.source_system = source_system_name
        self.org_id = "test"

    async def run(self):
        async for source_id in self.connector.list_changes():
            # 1. fetch the file bytes and ACL hints from the connector
            file_bytes, hints = await self.connector.fetch(source_id)

            # 2. map the ACL hints to a decision using the mapper
            decision = self.mapper.map(self.source_system, hints)

            # 3. parse the file bytes into a structured format using the layout parser
            markdown_text = LayoutParser.parse(file_bytes, source_id)

            document_id = make_doc_id(self.org_id, self.source_system, source_id)
            chunks = self.chunker.create_chunk(
                markdown_text,
                document_id=document_id,
                # org_id=self.org_id,
                # source_system=self.source_system,
                # source_url=hints["path"],
                # allowed_groups=list(decision.allowed_groups),
            )

            # 5. embed the chunks using the embedder and upsert them into the vector store
            texts = [c.text_chunk for c in chunks]
            vectors = self.embedder.embed(texts)

            payload_template = {
                "org_id": self.org_id,
                "doc_id": document_id,
                "source_system": self.source_system,
                "source_id": source_id,
                "allowed_groups": list(decision.allowed_groups),
                "rule_id": decision.rule_id,
                "model_name": self.embedder.model_name,
            }

            self.vector_store.upsert_chunks(chunks, vectors, payload_template)
