from fastapi import UploadFile, HTTPException
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.chains.question_generate_chain import QuestionGenerateChain

import logging

from src.server.questions.schema import QuestionGenerateRequest, QuestionGenerateResponse

logger = logging.getLogger(__name__)


async def extract_text_from_pdf(file: UploadFile) -> str:
    """PDF에서 텍스트를 추출하는 함수"""
    try:
        from io import BytesIO
        from pypdf import PdfReader

        # 파일 내용을 메모리로 읽기
        file_content = await file.read()

        # BytesIO로 래핑하여 PdfReader에서 사용
        pdf_file = BytesIO(file_content)
        reader = PdfReader(pdf_file)

        # 모든 페이지에서 텍스트 추출
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"

        # 텍스트 분할기 설정 (선택사항)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

        # 텍스트가 너무 길면 분할해서 합치기
        if len(full_text) > 10000:  # 10,000자 이상이면 분할
            chunks = text_splitter.split_text(full_text)
            full_text = "\n".join(chunks[:10])  # 처음 10개 청크만 사용

        return full_text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF 텍스트 추출 실패: {str(e)}")

async def generate_questions(
    file: UploadFile,
    request: QuestionGenerateRequest
) -> QuestionGenerateResponse:
    # 파일 확장자 검증
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="PDF 파일만 업로드 가능합니다.")

    try:
        # PDF에서 텍스트 추출 (파일 경로 없이 직접 처리)
        extracted_text = await extract_text_from_pdf(file)

        question_chain = QuestionGenerateChain.get_instance()

        # OpenAI로 문제 생성
        questions = question_chain.generate_questions(extracted_text, request)

        # 응답 생성
        response = QuestionGenerateResponse(
            questions=questions,
            total_count=len(questions),
        )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"처리 중 오류 발생: {str(e)}")