from pgvector import Vector
from sqlalchemy import Column, String

from src.app.core.db.models import TimestampMixin, UUIDMixin


class Document(UUIDMixin, TimestampMixin):
    """Document model for storing text chunks and their embeddings."""
    __tablename__ = "documents"

    content = Column(String, nullable=False)
    embedding = Column(Vector(1536))
