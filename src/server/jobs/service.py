from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.server.jobs.models import Job
from src.server.jobs.repository import find_by_id


def get_by_id(db: Session, id: UUID) -> Job:
    job = find_by_id(db, id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The job does not exist."
        )
    return job