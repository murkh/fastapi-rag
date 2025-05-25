from typing import AsyncGenerator
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from sqlalchemy.ext.asyncio import AsyncSession
from .embeddings_service import EmbeddingsService
from ..core.config import settings


class RAGService:
    def __init__(self):
        self.embeddings_service = EmbeddingsService()
        self.llm = OpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            streaming=True
        )

    async def get_chain(self, db: AsyncSession, top_k: int | None = 3) -> RetrievalQA:
        """Get RAG chain with vector store retriever.

        Args:
            db: Database session
            top_k: Number of most relevant chunks to retrieve. Defaults to 3.
        """
        vector_store = await self.embeddings_service.get_vector_store(db)
        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": top_k}
        )
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=retriever
        )

    async def stream_response(self, question: str, db: AsyncSession, top_k: int | None = 3) -> AsyncGenerator[str, None]:
        """Stream response chunks from the RAG chain.

        Args:
            question: The question to ask
            db: Database session
            top_k: Number of most relevant chunks to retrieve. Defaults to 3.
        """
        chain = await self.get_chain(db, top_k=top_k)
        async for chunk in chain.astream(question):
            if "result" in chunk:
                print(chunk["result"])
                yield chunk["result"]
