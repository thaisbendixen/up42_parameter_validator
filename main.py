from fastapi import FastAPI

from src.models import DataBlocks

app = FastAPI()


@app.get("/")
def healthcheck() -> dict:
    return {"status": "OK"}


@app.post("/validate")
def validate(models: DataBlocks) -> DataBlocks:
    return models
