# VaultQuery
Permission-Aware Enterprise Knowledge Systems

```
vaultquery-rag/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI app entrypoint, lifespan events (DB/model init)
│   │
│   ├── api/                         # HTTP / gRPC routing layer
│   │   ├── __init__.py
│   │   ├── deps.py                  # Dependency injection (auth, tenant/vault ID, clients)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py            # Aggregates v1 routes
│   │       ├── ingest.py            # Endpoints: upload docs, trigger sync, check job status
│   │       ├── query.py             # Endpoints: /query (JSON) & /query/stream (SSE)
│   │       └── health.py            # Liveness & readiness probes (checks vector DB + LLM)
│   │
│   ├── core/                        # Cross-cutting infrastructure & config
│   │   ├── __init__.py
│   │   ├── config.py                # Pydantic BaseSettings (env vars, model names, keys)
│   │   ├── logging.py               # Structured JSON logging & trace IDs
│   │   ├── security.py              # Internal service-to-service auth / JWT / API keys
│   │   └── exceptions.py            # Custom RAG exceptions & HTTP error handlers
│   │
│   ├── schemas/                     # Pydantic v2 request/response & internal DTOs
│   │   ├── __init__.py
│   │   ├── document.py              # Document metadata, chunk schema, ingestion status
│   │   ├── query.py                 # QueryRequest (filters, top_k), Citation, QueryResponse
│   │   └── eval.py                  # Evaluation payload schemas
│   │
│   ├── ingestion/                   # Offline pipeline: Raw File -> Vector Store
│   │   ├── __init__.py
│   │   ├── loaders/                 # Format-specific parsers (PDF, Markdown, DOCX, HTML)
│   │   │   ├── base.py
│   │   │   ├── pdf_loader.py
│   │   │   └── markdown_loader.py
│   │   ├── chunkers/                # Splitting strategies
│   │   │   ├── base.py
│   │   │   ├── semantic.py
│   │   │   └── recursive.py
│   │   ├── enrichers.py             # Metadata extraction, parent-child mapping, summaries
│   │   └── pipeline.py              # Orchestrates load -> clean -> chunk -> embed -> upsert
│   │
│   ├── retrieval/                   # Online pipeline: User Query -> Ranked Context
│   │   ├── __init__.py
│   │   ├── query_transformer.py     # HyDE, query expansion, multi-query rewriting
│   │   ├── search.py                # Dense (vector) + Sparse (BM25/keyword) hybrid search
│   │   ├── reranker.py              # Cross-encoder / Cohere / FlashRank reranking
│   │   └── filters.py               # Multi-tenant / vault-level ACL metadata filtering
│   │
│   ├── generation/                  # Context -> Grounded Answer
│   │   ├── __init__.py
│   │   ├── prompts/                 # Versioned prompt templates (YAML or Jinja2)
│   │   │   ├── system_qa.jinja2
│   │   │   └── query_rewrite.jinja2 Cross-encoder / Cohere / FlashRank reranking
│   │   ├── synthesizer.py           # LLM invocation, streaming, and citation grounding
│   │   └── guardrails.py            # Hallucination / context-adherence & PII checks
│   │
│   ├── clients/                     # External service wrappers (easy to mock/swap)
│   │   ├── __init__.py
│   │   ├── vector_store.py          # Qdrant / pgvector / Milvus / Pinecone client
│   │   ├── embedder.py              # Embedding model client (OpenAI, Voyage, local ONNX)
│   │   ├── llm.py                   # LiteLLM / OpenAI / Anthropic / vLLM wrapper
│   │   └── cache.py                 # Redis semantic & embedding cache
│   │
│   └── workers/                     # Async background processing (if ingestion is heavy)
│       ├── __init__.py
│       ├── broker.py                # Celery / Taskiq / ARQ setup
│       └── tasks.py                 # Async document indexing & re-indexing jobs
│
├── evals/                           # RAG quality benchmarking (RAGAS / DeepEval)
│   ├── datasets/                    # Golden Q&A pairs for VaultQuery
│   ├── run_eval.py                  # CI script for faithfulness, recall, & MRR metrics
│   └── metrics.py
│
├── tests/
│   ├── conftest.py                  # Fixtures (in-memory vector store, mock LLM)
│   ├── unit/                        # Chunking, prompt rendering, filter logic tests
│   └── integration/                 # End-to-end ingest -> retrieve -> generate tests
│
├── scripts/
│   └── reindex_vault.py             # CLI script for zero-downtime collection migrations
│
├── Dockerfile                       # Multi-stage slim production image
├── docker-compose.yml               # Local dev stack (API + Vector DB + Redis + Worker)
├── pyproject.toml                   # Dependencies & linter config (uv / poetry + ruff)
└── .env.example                     # Template for required environment variables
```