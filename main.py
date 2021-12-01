from typing import Dict

from fastapi import FastAPI

from src.models import DataModel

app = FastAPI()


@app.get("/")
def healthcheck() -> dict:
    return {"status": "OK"}


@app.post("/validate")
def validate(models: Dict[str, DataModel]) -> dict:
    return models
