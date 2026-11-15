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


class SmartIngestionPipeline:
    """A more intelligent ingestion pipeline that tracks document state and only re-embeds when necessary."""

    def __init__(
        self,
        connector: BaseConnector,
        mapper: AclMapper,
        chunker: TokenChunker,
        embedder: LocalSentenceTransformerEmbedder,
        vector_store: QdrantVectorStore,
        state_store: PostgresStateStore,
        source_system_name: str,
    ):
        self.connector = connector
        self.mapper = mapper
        self.chunker = chunker
        self.embedder = embedder
        self.vector_store = vector_store
        self.state_store = state_store
        self.source_system = source_system_name

    async def run_sync(self):
        """Runs the ingestion pipeline in a sync mode, processing all changes and handling deletions."""
        seen_source_ids = set()

        async for source_id in self.connector.list_changes():
            seen_source_ids.add(source_id)
            await self._process_single_item(source_id)

        await self._handle_deletions(seen_source_ids)

    async def _process_single_item(self, source_id: str):
        """Processes a single document from the source system, handling state tracking and conditional re-embedding."""

        file_bytes, hints = await self.connector.fetch(source_id)
        decision = self.mapper.map(self.source_system, hints)

        new_content_hash = hashlib.sha256(file_bytes).hexdigest()
        new_acl_hash = PostgresStateStore.compute_acl_hash(
            list(decision.allowed_groups)
        )

        existing_state = await self.state_store.get_state(self.source_system, source_id)

        if existing_state:
            old_content_hash, old_acl_hash = existing_state

            if old_content_hash == new_content_hash and old_acl_hash:
                # skip completely unchanged documents - embedder never called
                return

            if old_content_hash == new_content_hash and old_acl_hash != new_acl_hash:
                # acl only update (file moved to different dir) - update payload no re-embedding
                self.vector_store.update_payload_by_source_id(
                    source_id=source_id,
                    new_allowed_groups=list(decision.allowed_groups),
                    new_rule_id=decision.rule_id,
                )
                await self.state_store.upsert_state(
                    self.source_system,
                    source_id,
                    file_bytes,
                    list(decision.allowed_groups),
                )
                return

        markdown_text = LayoutParser.parse(file_bytes, source_id)
        document_id = make_doc_id(self.org_id, self.source_system, source_id)
        chunks = self.chunker.create_chunk(
            markdown_text,
            document_id=document_id,
        )

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
        await self.state_store.upsert_state(
            self.source_system, source_id, file_bytes, list(decision.allowed_groups)
        )

    async def _handle_deletions(self, live_source_ids: set[str]):
        """Handle deletions of documents from the source system."""

        # fetch all ids registered in db for this system
        stored_ids = await self.state_store.get_all_source_ids(self.source_system)

        # identify items present in db but missing from the live source
        orphaned_ids = [sid for sid in stored_ids if sid not in live_source_ids]

        if orphaned_ids:
            log.warning(
                f"Tombstone sweep: Found {len(orphaned_ids)} deleted documents in {self.source_system}. Purging vectors and state."
            )

        # purge vector chunks from qdrant
        self.vector_store.delete_points_by_source_ids(orphaned_ids)

        # purge tracking metadata row from db
        await self.state_store.delete_states(self.source_system, orphaned_ids)


