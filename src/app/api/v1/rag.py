from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.db.database import async_get_db
from ...services.embeddings_service import EmbeddingsService
from ...services.rag_service import RAGService

router = APIRouter(prefix="/rag", tags=["RAG"])
embeddings_service = EmbeddingsService()
rag_service = RAGService()


class QueryRequest(BaseModel):
    question: str
    top_k: int | None = 3  # Default to 3 if not specified


@router.post("/documents")
async def upload_document(
    file: UploadFile,
    db: AsyncSession = Depends(async_get_db)
):
    """Upload a document and store its chunks with embeddings."""
    content = await file.read()
    text = content.decode("utf-8")
    await embeddings_service.load_and_store_embeddings(text, db)
    return {"message": "Document processed successfully"}


@router.post("/query")
async def query(
    req: QueryRequest,
    db: AsyncSession = Depends(async_get_db)
):
    """Query the RAG system with streaming response.

    Args:
        req: Query request containing the question and optional top_k parameter
            to limit the number of retrieved contexts
    """
    return StreamingResponse(
        rag_service.stream_response(req.question, db=db, top_k=req.top_k),
        media_type="text/plain"
    )
