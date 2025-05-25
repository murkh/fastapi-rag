from fastapi import APIRouter
from .v1.rag import router as rag_router

router = APIRouter()
router.include_router(rag_router, prefix="/v1")