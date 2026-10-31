from fastapi import APIRouter
from app.schemas.query import QueryRequest, QueryResponse
from app.services.rag import ask_question

router = APIRouter(
    prefix="/query",
    tags=["query"]
)


@router.post("/", response_model=QueryResponse)
async def query(request: QueryRequest):
    return ask_question(request.question)