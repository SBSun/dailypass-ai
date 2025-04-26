from langchain.prompts import ChatPromptTemplate

QUESTION_GENERATE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """너는 직무 기반 인터뷰 질문을 생성하는 전문 AI야.
아래 조건에 따라 JSON 형식으로 질문을 생성해.

<요구 사항>
- 질문은 반드시 "{job}" 직무에 적합해야 해.
- 난이도는 "{difficulty}" 수준으로 맞춰야 해. (난이도는 easy, medium, hard 중 하나야)
- 총 {count}개의 질문을 생성해.
- 각 질문은 명확하고 구체적이어야 해.
- 중복된 질문이 있으면 안 돼.
- 오직 JSON 형식의 결과만 출력하고, JSON 외 다른 텍스트는 포함하지 마.

<출력 예시>
{{
  "content": "트랜잭션이란 무엇이고, 어떻게 관리하나요?",
  "difficulty": "{difficulty}",
}}

모든 항목은 이 예시 형식과 동일하게 구성해. JSON 배열로 여러 개를 출력할 것.
""",
        ),
        ("human", "질문을 생성해줘."),
    ]
)