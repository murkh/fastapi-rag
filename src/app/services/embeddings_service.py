from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import PGVector
from langchain.schema import Document
from ..core.config import settings
import numpy as np


class EmbeddingsService:
    def __init__(self):
        self.embedding_model = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY)
        self.text_splitter = CharacterTextSplitter(
            chunk_size=500, chunk_overlap=50)

    async def load_and_store_embeddings(self, text: str, db: PGVector):
        """Split text into chunks and store with embeddings."""
        chunks = self.text_splitter.split_text(text)
        documents = [Document(page_content=chunk) for chunk in chunks]
        ids = await db.aadd_documents(documents)
        return {"ids": ids}

    def get_vector_store(self) -> PGVector:
        """Get PGVector store for similarity search."""
        return PGVector(
            collection_name="documents",
            connection_string=settings.DATABASE_URL,
            embedding_function=self.embedding_model
        )
