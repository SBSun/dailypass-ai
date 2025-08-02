from typing import List, Optional

from pydantic import BaseModel


class Question(BaseModel):
    question: str
    options: List[str]
    correct_answer: int  # 정답의 인덱스 (0부터 시작)

class QuestionGenerateRequest(BaseModel):
    num_questions: Optional[int] = 10
    question_type: Optional[str] = "multiple_choice"

class QuestionGenerateResponse(BaseModel):
    questions: List[Question]
    total_count: int