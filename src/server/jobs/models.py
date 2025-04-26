from datetime import datetime

from sqlalchemy import TIMESTAMP, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from src.db.database import Base


class Job(Base):
    __tablename__ = "job"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    position: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())