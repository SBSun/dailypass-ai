from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI

from src.prompts.answer_generate_prompts import ANSWER_GENERATE_PROMPT

class AnswerGenerateChain:
    _instance: "AnswerGenerateChain" = None

    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.
        )
        self.chain = RunnableSequence(ANSWER_GENERATE_PROMPT | self.llm)

    @classmethod
    def get_instance(cls) -> "AnswerGenerateChain":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def generate_answer(self, question: str) -> str:
        response = self.chain.invoke(input={"question": question})

        if isinstance(response, AIMessage):
            print("AIMessage content:", response.content)
        else:
            raise ValueError("Response is not an AIMessage object.", response)

        content = response.content

        import json
        try:
            result = json.loads(content)
            return result["content"]
        except json.JSONDecodeError as e:
            raise ValueError("JSON 파싱 실패:\n" + content + f"\n\n에러: {e}")
        except KeyError:
            raise ValueError("`content` 키를 찾을 수 없습니다:\n" + content)
