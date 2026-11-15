from functools import lru_cache


from data_onboarding.storage import QdrantVectorStore

settings = get_settings()

@lru_cache(maxsize=1)
def get_qbrant_client() -> QdrantVectorStore:
    return QdrantVectorStore(collection_name="")




















