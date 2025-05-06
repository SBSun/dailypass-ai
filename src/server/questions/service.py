
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.chains.answer_generate_chain import AnswerGenerateChain
from src.chains.question_generate_chain import QuestionGenerateChain
from src.server.jobs.service import get_by_id
from src.server.questions.models import Question
from src.server.questions.schemas import QuestionGenerateReqeust
from src.vectorstores.question_vectorstore import QuestionVectorStore


def generate_questions(db: Session, request: QuestionGenerateReqeust) -> None:
    try:
        job = get_by_id(db, request.job_id)

        question_chain = QuestionGenerateChain()
        answer_chain = AnswerGenerateChain()
        vector_store = QuestionVectorStore.get_instance()

        new_questions = question_chain.generate_questions(
            job=job.position,
            difficulty=request.difficulty.get_code,
            count=request.count
        )

        question_entities = []

        for q in new_questions:
            question = q["content"]

            embedding = vector_store.generate_embedding(question)
            print(f"생성하려는 질문: {question}")
            if vector_store.find_similar_question(embedding):
                continue

            # 답변 생성
            try:
                answer = answer_chain.generate_answer(question)
            except Exception as ex:
                print(ex)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to process generate answer",
                ) from ex

            new_question = Question(
                job_id=request.job_id,
                content=question,
                difficulty=request.difficulty.get_code,
                answer=answer
            )
            question_entities.append(new_question)

            vector_store.save_question(question, embedding)

        db.add_all(question_entities)
        db.commit()

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process generate question",
        ) from e
