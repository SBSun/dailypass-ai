from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.server.jobs.models import Job


def find_by_id(db: Session, id: UUID) -> Optional[Job]:
    return db.scalar(
        select(Job)
        .where(Job.id == id)
    )