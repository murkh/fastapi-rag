from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import PGVector
from langchain.schema import Document
from ..core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession


class EmbeddingsService:
    def __init__(self):
        self.embedding_model = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY)
        self.text_splitter = CharacterTextSplitter(
            chunk_size=500, chunk_overlap=50)
        self._vector_store = None

        self.connection_string = (
            f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
            f"@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
        )

    async def init_vector_store(self, db: AsyncSession):
        """Initialize vector store with vector extension."""
        store = PGVector(
            collection_name="documents",
            connection_string=self.connection_string,
            embedding_function=self.embedding_model
        )
        try:
            store.create_collection()
        except Exception as e:
            if "already exists" not in str(e):
                raise e
        return store

    async def load_and_store_embeddings(self, text: str, db: AsyncSession):
        """Split text into chunks and store with embeddings."""
        if not self._vector_store:
            self._vector_store = await self.init_vector_store(db)

        chunks = self.text_splitter.split_text(text)
        documents = [Document(page_content=chunk) for chunk in chunks]
        ids = self._vector_store.add_documents(documents)
        return {"ids": ids}

    async def get_vector_store(self, db: AsyncSession) -> PGVector:
        """Get PGVector store for similarity search."""
        if not self._vector_store:
            self._vector_store = await self.init_vector_store(db)
        return self._vector_store
