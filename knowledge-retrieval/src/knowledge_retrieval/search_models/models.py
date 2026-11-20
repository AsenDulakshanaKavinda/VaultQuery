
from fastembed import TextEmbedding, SparseTextEmbedding
from knowledge_retrieval.core import get_settings
from fastembed.rerank.cross_encoder import TextCrossEncoder

settings = get_settings()

def get_dense_model():
    return TextEmbedding(
        model_name=settings.secrets.dence_model,
        cache_dir="models",
        local_files_only=True,
    )



def get_sparse_model():
    return SparseTextEmbedding(
        model_name=settings.secrets.sparse_model,
        cache_dir="models",
        local_files_only=True,
    )



def get_reranker_model():
    return TextCrossEncoder(
        model_name=settings.secrets.reranker_model,
        cache_dir="models",
        local_files_only=True,
    )


