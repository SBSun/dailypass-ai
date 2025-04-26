import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.server.endpoints import question_endpoint
from src.server.endpoints.question_endpoint import QuestionResponse

load_dotenv()

app = FastAPI(
    title="Jobterview AI API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/question-generate")
async def question_generate(reqeust: question_endpoint.QuestionGenerateReqeust) -> List[QuestionResponse]:
    return await question_endpoint.question_generate(reqeust)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app, host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", 8000))
    )