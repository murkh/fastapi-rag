from typing import AsyncGenerator
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from .embeddings_service import EmbeddingsService
from ..core.config import settings


class RAGService:
    def __init__(self):
        self.embeddings_service = EmbeddingsService()
        self.llm = OpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            streaming=True
        )

    def get_chain(self, top_k: int | None = 3) -> RetrievalQA:
        """Get RAG chain with vector store retriever.

        Args:
            top_k: Number of most relevant chunks to retrieve. Defaults to 3.
        """
        vector_store = self.embeddings_service.get_vector_store()
        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": top_k}
        )
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=retriever
        )

    async def stream_response(self, question: str, top_k: int | None = 3) -> AsyncGenerator[str, None]:
        """Stream response chunks from the RAG chain.

        Args:
            question: The question to ask
            top_k: Number of most relevant chunks to retrieve. Defaults to 3.
        """
        chain = self.get_chain(top_k=top_k)
        async for chunk in chain.astream(question):
            if "answer" in chunk:
                yield chunk["answer"]
