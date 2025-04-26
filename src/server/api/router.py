from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.server.questions.router import router as question_router

load_dotenv()

app = FastAPI(
    title="Jobterview AI API",
    swagger_ui_parameters={
        "docExpansion": "none",
        "operationsSorter": "method",
        "filter": True,
        "tagsSorter": "alpha",
        "displayRequestDuration": True,
        "syntaxHighlight.theme": "tomorrow-night",
    }
)

app.include_router(question_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app, host="127.0.0.1", port=8000
    )