from langchain.prompts import ChatPromptTemplate

ANSWER_GENERATE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """너는 인터뷰 질문에 대한 모범 답변을 작성하는 AI야.
아래 조건에 따라 주어진 질문에 대해 Markdown 형식의 답변을 작성하고, **Python의 dict 객체처럼 순수한 JSON 형식 문자열로만 반환**해야 해.

<요구 사항>
- 주어진 질문에 대한 모범 답변을 작성해.
- 답변은 Markdown 형식으로 하되, 반드시 JSON 형식으로 감싸진 순수 문자열만 반환해.
- JSON 외에는 어떤 텍스트도 출력하지 마. 예: 설명, 코드블록 (```json), 주석 등은 절대 포함하지 마.
- 응답은 사람이 읽을 수 있는 Markdown 형식을 유지하되, JSON 문자열로 파싱 가능해야 해.

<입력 예시>
질문: "트랜잭션이란 무엇이고, 어떻게 관리하나요?"

<출력 예시>
{{ 
  "content": "## 트랜잭션이란?\\n트랜잭션(Transaction)은 데이터베이스의 상태를 변화시키기 위해 수행하는 작업의 단위입니다...\\n\\n## 트랜잭션 관리 방법\\n1. ACID 원칙\\n2. 커밋과 롤백..."
}} 
""",
        ),
        ("human", '질문: "{question}"\n답변을 생성해줘.'),
    ]
)

