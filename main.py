from fastapi import FastAPI

from src.models import Blocks

app = FastAPI()


@app.get("/")
def healthcheck() -> dict:
    return {"status": "OK"}


@app.post("/validate")
def validate(models: Blocks) -> Blocks:
    return models
