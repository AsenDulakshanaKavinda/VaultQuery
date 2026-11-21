from langchain.tools import tool, ToolException

from knowledge_retrieval.retrieval import HybridRetrievalEngine, get_hybrid_retrieval_engine
from knowledge_retrieval.schemas import SearchRequest



@tool(
    name="search document",
    args_schema=SearchRequest,
    handle_tool_error=True,
    handle_validation_error="",
)
def search_documents(
    query: str, 
    org_id: str, 
    user_groups: list[str], 
    source_systems: list[str], 
    doc_id: str, 
    stage1_candidates: int = 15, 
    top_k: int = 5, 
    min_confidence: float = 0.25
) -> str:
    try:
        payload = SearchRequest(
            query=query,
            org_id=org_id,
            user_groups=user_groups,
            source_systems=source_systems,
            doc_id=doc_id,
            stage1_candidates=stage1_candidates,
            top_k=top_k,
            min_confidence=min_confidence
        )
        search_engine: HybridRetrievalEngine = get_hybrid_retrieval_engine()
        result = search_engine.search(req=payload)
        return result.model_dump_json()
    except PermissionError as exc:
        raise ToolException(f"error while using tool: {str(exc)}")