from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import PGVector
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.db.models import Document
from ..core.config import settings

class EmbeddingsService:
    def __init__(self):
        self.embedding_model = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
        self.text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        
    async def load_and_store_embeddings(self, text: str, db: AsyncSession):
        """Split text into chunks and store with embeddings."""
        chunks = self.text_splitter.split_text(text)
        embeddings = self.embedding_model.embed_documents(chunks)
        
        documents = []
        for chunk, vector in zip(chunks, embeddings):
            doc = Document(content=chunk, embedding=vector)
            documents.append(doc)
        
        db.add_all(documents)
        await db.commit()
        
    def get_vector_store(self) -> PGVector:
        """Get PGVector store for similarity search."""
        return PGVector(
            collection_name="documents",
            connection_string=settings.DATABASE_URL,
            embedding_function=self.embedding_model
        )
