from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello from the knowledge retrieval service"}

@app.get("/health")
async def health():
    return {"message": "checking health"}



