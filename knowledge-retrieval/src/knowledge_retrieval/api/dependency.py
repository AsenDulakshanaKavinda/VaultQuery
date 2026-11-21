from fastapi import Depends

from knowledge_retrieval.retrieval import HybridRetrievalEngine


def get_retrieval_engine() -> HybridRetrievalEngine:
    """  """
    return HybridRetrievalEngine()