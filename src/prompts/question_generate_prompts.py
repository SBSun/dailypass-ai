from langchain.prompts import ChatPromptTemplate

QUESTION_GENERATE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """당신은 자격증 시험 문제를 생성하는 전문가입니다. 
주어진 PDF 내용을 바탕으로 실제 자격증 시험에 나올 수 있는 수준 높은 문제를 만들어야 합니다.
항상 정확한 JSON 형식으로 응답해야 합니다."""
        ),
        (
            "user",
            """다음 PDF 내용을 바탕으로 자격증 시험 문제를 생성해주세요.

=== PDF 내용 ===
{content}

=== 문제 생성 요구사항 ===
- 문제 개수: {num_questions}개
- 문제 유형: {question_type}

=== 출력 형식 ===
반드시 다음 JSON 형식으로만 응답해주세요:

{{
  "questions": [
    {{
      "question": "문제 내용 (명확하고 구체적으로)",
      "options": ["선택지1", "선택지2", "선택지3", "선택지4"],
      "correct_answer": 1,
    }}
  ]
}}

주의: 
- correct_answer는 1부터 시작하세요.
- 응답에 절대로 코드블럭(예: ```json)이나 설명을 포함하지 마세요. JSON 데이터만 반환하세요.

=== 문제 생성 규칙 ===
1. **PDF 내용 기반**: 제공된 PDF 내용에서만 문제를 생성
2. **실무 적용**: 실제 업무에서 활용 가능한 지식 위주
3. **명확한 정답**: 애매하지 않은 명확한 정답이 있어야 함
4. **오답 선택지**: 그럴듯하지만 틀린 선택지 포함
5. **한국어 사용**: 모든 내용을 한국어로 작성
6. **전문 용어**: 해당 분야의 정확한 전문 용어 사용

반드시 올바른 JSON 형식으로만 응답하세요."""
        )
    ]
)