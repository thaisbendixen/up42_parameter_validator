from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def healthcheck() -> dict:
    return {"status": "OK"}
