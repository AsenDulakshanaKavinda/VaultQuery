from fastapi import FastAPI, Depends, HTTPException, status
from knowledge_retrieval.retrieval import HybridRetrievalEngine
from knowledge_retrieval.api.dependency import get_retrieval_engine
from knowledge_retrieval.schemas import SearchRequest



app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello from the knowledge retrieval service"}

@app.get("/health")
async def health():
    return {"message": "checking health"}

@app.post("/test-h-retrieval")
async def hybrid_retrieval_engine(payload: SearchRequest, engine: HybridRetrievalEngine = Depends(get_retrieval_engine)):
    try:
        result = engine.search(payload)
        
        return {"data": result}
    except Exception as e:
        HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


