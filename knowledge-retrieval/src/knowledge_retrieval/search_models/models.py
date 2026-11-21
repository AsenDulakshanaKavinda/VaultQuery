from pathlib import Path
from fastembed import SparseTextEmbedding, TextEmbedding
from fastembed.rerank.cross_encoder import TextCrossEncoder
from knowledge_retrieval.core import get_settings

settings = get_settings()

# Resolves to /home/rapter/projects/VaultQuery/knowledge-retrieval/models_cache
# Works both on your local host and inside Docker (e.g., /app/models_cache)
PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODELS_CACHE_DIR = PROJECT_ROOT / "models_cache"


def get_dense_model() -> TextEmbedding:
    return TextEmbedding(
        model_name=settings.secrets.dence_model,
        cache_dir=str(MODELS_CACHE_DIR / "sentence-transformers--all-MiniLM-L6-v2"),
        local_files_only=True,
    )


def get_sparse_model() -> SparseTextEmbedding:
    return SparseTextEmbedding(
        model_name=settings.secrets.sparse_model,
        cache_dir=str(MODELS_CACHE_DIR / "Qdrant--bm25"),
        local_files_only=True,
    )


def get_reranker_model() -> TextCrossEncoder:
    return TextCrossEncoder(
        model_name=settings.secrets.reranker_model,
        cache_dir=str(MODELS_CACHE_DIR / "Xenova--ms-marco-MiniLM-L-6-v2"),
        local_files_only=True,
    )