from io import BytesIO

import logging

from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from src.chains.question_generate_chain import QuestionGenerateChain
from src.generated import question_pb2_grpc, question_pb2

class QuestionService(question_pb2_grpc.QuestionServiceServicer):
    """QuestionService의 실제 구현"""

    def GenerateQuestions(self, request, context):
        """
        파일 내용을 받아서 질문들을 생성하는 메서드
        """
        logging.info("GenerateQuestions 호출")
        try:
            # 파일 내용 추출
            file_content = request.file_content

            if not file_content:
                raise Exception("파일 내용이 비어있습니다.")

            # PDF에서 텍스트 추출
            try:
                extracted_text = self._extract_text_from_pdf(file_content)
            except Exception as e:
                raise Exception(f"PDF 텍스트 추출 실패: {str(e)}")

            # 질문 생성
            try:
                question_chain = QuestionGenerateChain.get_instance()

                # OpenAI로 문제 생성
                questions = question_chain.generate_questions(extracted_text)

                # 응답 객체 생성
                response = question_pb2.QuestionGenerateResponse()

                # 생성된 질문들을 응답에 추가
                for q_data in questions:
                    question_info = response.questions.add()
                    question_info.question = q_data.question
                    question_info.options.extend(q_data.options)
                    question_info.correct_answer = q_data.correct_answer

                logging.info(f"총 {len(questions)}개의 질문을 생성했습니다.")
                return response

            except Exception as e:
                raise Exception(f"문제 생성 중 오류 발생: {str(e)}")

        except Exception as e:
            raise Exception(f"GenerateQuestions 처리 중 오류: {str(e)}")

    def _extract_text_from_pdf(self, file_content: bytes) -> str:
        try:
            # BytesIO로 래핑하여 PdfReader에서 사용
            pdf_file = BytesIO(file_content)
            reader = PdfReader(pdf_file)

            # 모든 페이지에서 텍스트 추출
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text() + "\n"

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
            )

            if len(full_text) > 10000:  # 10,000자 이상이면 분할
                chunks = text_splitter.split_text(full_text)
                full_text = "\n".join(chunks[:10])  # 처음 10개 청크만 사용

            return full_text.strip()

        except Exception as e:
            raise Exception(f"PDF 텍스트 추출 실패: {str(e)}")