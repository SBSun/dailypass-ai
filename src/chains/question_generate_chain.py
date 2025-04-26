from typing import Any, Dict, List

from langchain.chains.llm import LLMChain
from langchain_community.chat_models import ChatOpenAI

from src.prompts.question_generate_prompts import QUESTION_GENERATE_PROMPT


class QuestionGenerateChain:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.7
        )
        self.chain = LLMChain(
            llm=self.llm,
            prompt=QUESTION_GENERATE_PROMPT
        )

    def generate_questions(self, job: str, difficulty: str, count: int) -> List[Dict[str, Any]]:
        response = self.chain.run(
            job=job,
            difficulty=difficulty,
            count=count
        )

        import json
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            raise ValueError("응답을 JSON으로 파싱할 수 없습니다:\n" + response)