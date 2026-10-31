from fastapi import FastAPI
from app.routes.query import router as query_router
from app.routes.upload import router as upload_router

app = FastAPI(
    title="RAG with FastAPI",
    description="A simple RAG application using FastAPI, LangChain, and Qdrant",
    version="0.1.0"
)

app.include_router(query_router)
app.include_router(upload_router)

@app.get("/")
def root():
    return {"message": "Welcome to the RAG FastAPI application!"}
