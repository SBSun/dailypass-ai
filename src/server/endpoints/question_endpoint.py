from typing import Dict, List

from fastapi import HTTPException, status
from pydantic import BaseModel

from src.chains.question_generate_chain import QuestionGenerateChain


class QuestionGenerateReqeust(BaseModel):
    job: str
    difficulty: str
    count: int


class QuestionResponse(BaseModel):
    content: str
    difficulty: str


async def question_generate(request: QuestionGenerateReqeust) -> List[QuestionResponse]:
    try:
        chain = QuestionGenerateChain()
        questions = chain.generate_questions(
            job=request.job,
            difficulty=request.difficulty,
            count=request.count
        )
        return [QuestionResponse(**q) for q in questions]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process create question",
        ) from e