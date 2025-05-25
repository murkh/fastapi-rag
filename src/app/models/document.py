from datetime import datetime
from sqlalchemy import String, Text, DateTime, JSON
from ..core.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class DocumentRecord(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata: Mapped[dict] = mapped_column(JSON, default={})
    embedding: Mapped[str] = mapped_column(
        "embedding", Text)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<DocumentRecord(id='{self.id}', content='{self.content[:50]}...')>"
