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

                # question_type enum을 문자열로 변환
                question_type_str = question_pb2.QuestionGenerateRequest.QuestionType.Name(request.question_type)

                # OpenAI로 문제 생성
                questions = question_chain.generate_questions(extracted_text, question_type_str)

                response = question_pb2.QuestionGenerateResponse()

                for q_data in questions:
                    question_info = response.questions.add()
                    question_info.question = q_data.question

                    if q_data.context is not None:
                        question_info.context = q_data.context

                    # MULTIPLE_CHOICE (0) 일 때만 options 추가
                    if request.question_type == question_pb2.QuestionGenerateRequest.QuestionType.MULTIPLE_CHOICE:
                        if q_data.options:
                            question_info.options.extend(q_data.options)
                            
                    question_info.correct_answer = q_data.correct_answer
                    question_info.category = q_data.category
                    question_info.language = q_data.language

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

            

            return full_text.strip()

        except Exception as e:
            raise Exception(f"PDF 텍스트 추출 실패: {str(e)}")