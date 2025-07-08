from typing import Any, Dict, List

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI

from src.prompts.question_generate_prompts import QUESTION_GENERATE_PROMPT


class QuestionGenerateChain:
    _instance: "QuestionGenerateChain" = None

    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.7
        )
        self.chain = RunnableSequence(QUESTION_GENERATE_PROMPT | self.llm)

    @classmethod
    def get_instance(cls) -> "QuestionGenerateChain":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def generate_questions(self, job: str, difficulty: str, count: int) -> List[Dict[str, Any]]:
        response = self.chain.invoke(input={"job": job, "difficulty": difficulty, "count": count})

        if isinstance(response, AIMessage):
            print("AIMessage content:", response.content)
        else:
            raise ValueError("Response is not an AIMessage object.", response)

        import json
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            raise ValueError("응답을 JSON으로 파싱할 수 없습니다:\n" + response)