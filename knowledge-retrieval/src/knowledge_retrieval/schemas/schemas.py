from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=1000)

    # Mandatory security & multi-tenant context
    org_id: str = Field(..., min_length=1, description="User organization ID")
    user_groups: list[str] = Field(
        ...,
        min_length=1,
        description="Groups/roles belonging to the querying user for ACL enforcement",
    )

    # Optional narrowing filters
    source_systems: list[str] | None = Field(
        default=None,
        description="Optional filter to restrict search to specific systems (e.g., ['jira', 'sharepoint'])",
    )
    doc_id: str | None = Field(
        default=None,
        description="Optional filter to search within a single document",
    )

    # Retrieval & reranking controls
    stage1_candidates: int = Field(default=15, ge=5, le=100)
    top_k: int = Field(default=5, ge=1, le=25)
    min_confidence: float = Field(
        default=0.25,
        ge=0.0,
        le=1.0,
        description="Minimum sigmoid-calibrated cross-encoder probability (0.0 to 1.0)",
    )


class ChunkMetadata(BaseModel):
    org_id: str
    doc_id: str
    source_system: str
    source_id: str
    allowed_groups: list[str]
    rule_id: str
    model_name: str


class RetrievedChunk(BaseModel):
    id: str
    text: str
    metadata: ChunkMetadata
    confidence: float = Field(..., description="Sigmoid probability from Stage 2 reranker")
    raw_logit: float = Field(..., description="Raw unbounded cross-encoder logit")
    rrf_score: float = Field(..., description="Stage 1 Reciprocal Rank Fusion score")


class SearchResponse(BaseModel):
    query: str
    org_id: str
    results: list[RetrievedChunk]
    total_returned: int
    latency_ms: dict[str, float]