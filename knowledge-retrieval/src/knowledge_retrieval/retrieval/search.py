
import math
import os
import time
from typing import Any

from knowledge_retrieval.schemas.schemas import ChunkMetadata, RetrievedChunk, SearchRequest, SearchResponse
from knowledge_retrieval.store import get_qdrant_client
from knowledge_retrieval.search_models import get_reranker_model, get_sparse_model, get_dense_model
from knowledge_retrieval.core import get_settings

from qdrant_client.models import models

from knowledge_retrieval.observability import log

def sigmoid(logit: float) -> float:
    """Numerically stable sigmoid mapping (-inf, +inf) -> (0.0, 1.0)."""
    if logit >= 0:
        return 1.0 / (1.0 + math.exp(-logit))
    exp_x = math.exp(logit)
    return exp_x / (1.0 + exp_x)


class HybridRetrievalEngine:
    def __init__(self):
        self.settings = get_settings()
        self.qdrant_client = get_qdrant_client()
        self.dense_model = get_dense_model()
        self.sparse_model = get_sparse_model()
        self.reranker_model = get_reranker_model()

        if self.settings.secrets.local_files_only:
            os.environ["HF_HUB_OFFLINE"] = "1"


    def warmup(self) -> None:
        """Forces ONNX Runtime session initialization and memory allocation at startup."""
        _ = next(self.dense_model.query_embed("warmup query"))
        _ = next(self.sparse_model.query_embed("warmup query"))
        _ = list(self.reranker_model.rerank("warmup query", ["warmup document"]))

    def close(self) -> None:
        self.qdrant_client.close()

    def _build_acl_filter(self, req: SearchRequest) -> models.Filter:
        must_conditions: list[models.Condition] = [
            models.FieldCondition(
                key="org_id",
                match=models.MatchValue(value=req.org_id),
            ),
            models.FieldCondition(
                key="allowed_groups",
                match=models.MatchAny(any=req.user_groups),
            ),
        ]

        if req.source_systems:
            must_conditions.append(
                models.FieldCondition(
                    key="source_system",
                    match=models.MatchAny(any=req.source_systems),
                )
            )

        if req.doc_id:
            must_conditions.append(
                models.FieldCondition(
                    key="doc_id",
                    match=models.MatchValue(value=req.doc_id),
                )
            )

        return models.Filter(must=must_conditions)


    def _check_model_version(
        self,
        payload: dict[str, Any],
        warned_models: set[str],
    ) -> None:
        """Logs a warning if a retrieved chunk was indexed with a different embedding model."""
        stored_model = payload.get("model_name")
        if (
            stored_model
            and stored_model != self.settings.secrets.dence_model
            and stored_model not in warned_models
        ):
            warned_models.add(stored_model)
            log.warning(
                "Embedding model mismatch detected during retrieval: "
                "chunk was indexed with '%s', but active query model is '%s' "
                "(org_id=%s, doc_id=%s). Cosine similarity scores may be degraded.",
                stored_model,
                self.settings.secrets.dence_model,
                payload.get("org_id"),
                payload.get("doc_id"),
            )

    @staticmethod
    def _extract_text(payload: dict[str, Any]) -> str:
        """Extracts chunk text safely across common payload key conventions."""
        return str(payload.get("text") or payload.get("chunk_text") or "")

    def search(self, req: SearchRequest) -> SearchResponse:
        t0 = time.perf_counter()

        # 1. encode query into dense and sparse representations
        query_dense = next(self.dense_model.query_embed(req.query)).tolist()
        raw_sparse = next(self.sparse_model.query_embed(req.query))
        query_sparse = models.SparseVector(
            indices=raw_sparse.indices.tolist(),
            values=raw_sparse.values.tolist(),
        )
        t_embed = time.perf_counter()

        # 2. build multi-tenant and group ACL filter
        acl_filter = self._build_acl_filter(req)

        # 3. stage 01 - hybrid prefetch + server side reciprocal rank fusion (RRF)
        prefetch_limit = req.stage1_candidates * 2
        stage1_hits = self.client.query_points(
            collection_name=self.settings.secrets.collection_name,
            prefetch=[
                models.Prefetch(
                    query=query_dense,
                    using="dense",
                    filter=acl_filter,
                    limit=prefetch_limit,
                ),
                models.Prefetch(
                    query=query_sparse,
                    using="sparse",
                    filter=acl_filter,
                    limit=prefetch_limit,
                ),
            ],
            query=models.FusionQuery(fusion=models.Fusion.RRF),
            limit=req.stage1_candidates,
            with_payload=True,
        ).points
        t_stage1 = time.perf_counter()

        if not stage1_hits:
            return SearchResponse(
                query=req.query,
                org_id=req.org_id,
                results=[],
                total_returned=0,
                latency_ms={
                    "embed": round((t_embed - t0) * 1000, 2),
                    "stage1_rrf": round((t_stage1 - t_embed) * 1000, 2),
                    "stage2_rerank": 0.0,
                    "total": round((t_stage1 - t0) * 1000, 2),
                },
            )

        # 4. stage 02 - Cross-Encoder Reranking + Sigmoid Thresholding + Metadata Hydration
        candidate_texts = [
            self._extract_text(hit.payload or {}) for hit in stage1_hits
        ]
        logits = list(
            self.reranker_model.rerank(query=req.query, documents=candidate_texts)
        )

        warned_models: set[str] = set()
        scored_chunks: list[RetrievedChunk] = []

        for hit, chunk_text, raw_logit in zip(stage1_hits, candidate_texts, logits):
            prob = sigmoid(float(raw_logit))
            if prob < req.min_confidence:
                continue

            payload = hit.payload or {}
            self._check_model_version(payload, warned_models)

            metadata = ChunkMetadata(
                org_id=str(payload.get("org_id", req.org_id)),
                doc_id=str(payload.get("doc_id", "")),
                source_system=str(payload.get("source_system", "")),
                source_id=str(payload.get("source_id", "")),
                allowed_groups=list(payload.get("allowed_groups", [])),
                rule_id=str(payload.get("rule_id", "")),
                model_name=str(payload.get("model_name", "")),
            )

            scored_chunks.append(
                RetrievedChunk(
                    id=str(hit.id),
                    text=chunk_text,
                    metadata=metadata,
                    confidence=round(prob, 4),
                    raw_logit=round(float(raw_logit), 4),
                    rrf_score=round(float(hit.score), 4),
                )
            )

        scored_chunks.sort(key=lambda c: c.confidence, reverse=True)
        final_chunks = scored_chunks[: req.top_k]
        t_stage2 = time.perf_counter()
        

        return SearchResponse(
            query=req.query,
            org_id=req.org_id,
            results=final_chunks,
            total_returned=len(final_chunks),
            latency_ms={
                "embed": round((t_embed - t0) * 1000, 2),
                "stage1_rrf": round((t_stage1 - t_embed) * 1000, 2),
                "stage2_rerank": round((t_stage2 - t_stage1) * 1000, 2),
                "total": round((t_stage2 - t0) * 1000, 2),
            },
        )


def get_hybrid_retrieval_engine():
    return HybridRetrievalEngine()






