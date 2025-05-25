from datetime import UTC, datetime
import uuid as uuid_mod
from sqlalchemy import Column, DateTime, text
from sqlalchemy.dialects.postgresql import UUID


class UUIDMixin:
    uuid: uuid_mod.UUID = Column(
        UUID, primary_key=True, default=uuid_mod.uuid4, server_default=text("gen_random_uuid()")
    )


class TimestampMixin:
    created_at: datetime = Column(DateTime, default=datetime.now(
        UTC), server_default=text("current_timestamp(0)"))
    updated_at: datetime = Column(DateTime, nullable=True, onupdate=datetime.now(
        UTC), server_default=text("current_timestamp(0)"))
