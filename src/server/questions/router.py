from fastapi import APIRouter, UploadFile, File
import logging

from src.server.questions.schema import QuestionGenerateResponse, QuestionGenerateRequest
from src.server.services import question_generate_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/questions",
    tags=["Question"],
)

@router.post("/generate-questions",
          summary="PDF 기반 자격증 문제 생성",
          description="PDF 파일을 업로드하여 자격증 시험 문제를 생성합니다.")
async def generate_questions(
    file: UploadFile = File(..., description="분석할 PDF 파일"),
    num_questions: int = 10,
    question_type: str = "multiple_choice"
) -> QuestionGenerateResponse:
    # 요청 객체 생성
    request = QuestionGenerateRequest(
        num_questions=num_questions,
        question_type=question_type
    )

    return await question_generate_service.generate_questions(file, request)