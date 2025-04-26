from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.server.questions.enums import QuestionDifficulty
from src.server.questions.models import Question


def get_questions_by_job(db: Session, job_id: UUID, difficulty: QuestionDifficulty):
    return db.execute(
        select(Question.content, Question.difficulty)
        .where(
            Question.job_id == job_id,
            Question.difficulty == difficulty.value
        )
    ).all()