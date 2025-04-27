
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.chains.question_generate_chain import QuestionGenerateChain
from src.server.jobs.service import get_by_id
from src.server.questions.models import Question
from src.server.questions.schemas import QuestionGenerateReqeust
from src.vectorstores.question_vectorstore import QuestionVectorStore


def generate_questions(db: Session, request: QuestionGenerateReqeust) -> None:
    try:
        job = get_by_id(db, request.job_id)

        chain = QuestionGenerateChain()
        new_questions = chain.generate_questions(
            job=job.position,
            difficulty=request.difficulty.get_code,
            count=request.count
        )

        question_entities = []
        vector_store = QuestionVectorStore.get_instance()

        for q in new_questions:
            text = q["content"]

            embedding = vector_store.generate_embedding(text)
            print(f"생성하려는 질문: {text}")
            if vector_store.find_similar_question(embedding):
                continue

            question = Question(
                job_id=request.job_id,
                content=q["content"],
                difficulty=request.difficulty.get_code,
            )
            question_entities.append(question)

            vector_store.save_question(text, embedding)

        db.add_all(question_entities)
        db.commit()

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process generate question",
        ) from e
