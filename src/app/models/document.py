from pgvector import Vector
from sqlalchemy import Column, String

from ..core.db.models import UUIDMixin, TimestampMixin


class Document(UUIDMixin, TimestampMixin):
    """Document model for storing text chunks and their embeddings."""
    __tablename__ = "documents"

    content = Column(String, nullable=False)
    embedding = Column(Vector())
