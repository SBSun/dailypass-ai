import json
import logging
from typing import List

from fastapi import HTTPException
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI

from src.prompts.question_generate_prompts import QUESTION_GENERATE_PROMPT
from src.server.questions.schema import QuestionGenerateRequest, Question

logger = logging.getLogger(__name__)

class QuestionGenerateChain:
    _instance: "QuestionGenerateChain" = None

    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.7,
            max_tokens=3000
        )
        self.chain = RunnableSequence(QUESTION_GENERATE_PROMPT | self.llm)

    @classmethod
    def get_instance(cls) -> "QuestionGenerateChain":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def generate_questions(self, content: str, request: QuestionGenerateRequest) -> List[Question]:
        """LangChain을 사용하여 자격증 문제 생성"""
        try:
            response = self.chain.invoke(
                input={
                    "content": content[:4000],  # 토큰 제한을 위해 처음 4000자만 사용
                    "num_questions": request.num_questions,
                    "question_type": request.question_type
                }
            )

            if isinstance(response, AIMessage):
                response_text = response.content
                logger.error(f"[LangChain 응답]:\n{response_text}")

                # JSON 형태로 파싱 시도
                try:
                    questions_data = json.loads(response_text)
                    questions = [Question(**q) for q in questions_data["questions"]]
                    return questions
                except json.JSONDecodeError:
                    # JSON 파싱 실패 시 에러 발생
                    raise HTTPException(status_code=500, detail="LangChain 응답을 JSON으로 파싱할 수 없습니다.")
            else:
                raise HTTPException(status_code=500, detail=f"응답이 AIMessage 객체가 아닙니다: {type(response)}")

        except Exception as e:
            logger.error(f"문제 생성 중 오류 발생: {str(e)}")
            raise HTTPException(status_code=500, detail=f"문제 생성 중 오류가 발생했습니다: {str(e)}")