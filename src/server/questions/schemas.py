from uuid import UUID

from pydantic import BaseModel, Field

from src.server.questions.enums import QuestionDifficulty


class QuestionGenerateReqeust(BaseModel):
    job_id: UUID
    difficulty: QuestionDifficulty
    count: int = Field(..., ge=1)


class QuestionResponse(BaseModel):
    content: str
    difficulty: QuestionDifficulty