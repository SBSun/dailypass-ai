from fastapi import FastAPI
from starlette.responses import JSONResponse

app = FastAPI(
    swagger_ui_parameters={
        "docExpansion": "none",
        "operationsSorter": "method",
        "filter": True,
        "tagsSorter": "alpha",
        "displayRequestDuration": True,
        "syntaxHighlight.theme": "tomorrow-night",
    }
)

@app.get("/")
def hello():
    return JSONResponse(content={"Hello": "FastAPI"})