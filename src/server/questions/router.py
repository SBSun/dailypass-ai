from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.server.questions.enums import QuestionDifficulty
from src.server.questions.repository import get_questions_by_job
from src.server.questions.schemas import QuestionGenerateReqeust, QuestionResponse
from src.server.questions.service import generate_questions

router = APIRouter(
    prefix="/questions",
    tags=["Question"],
)

@router.post("", summary="면접 질문 생성")
def generate(
    request: QuestionGenerateReqeust,
    db: Session = Depends(get_db)
):
    return generate_questions(db, request)


@router.get("", summary="면접 질문 조회")
def get_questions(
    job_id: UUID = Query(...),
    difficulty: QuestionDifficulty = Query(...),
    db: Session = Depends(get_db)
) -> List[QuestionResponse]:
    return get_questions_by_job(db, job_id, difficulty)