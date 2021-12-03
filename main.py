import uvicorn
from fastapi import FastAPI

from src.models import Blocks
from src.up42_parameter_validator import UP42ParamaterValidator

app = FastAPI()


@app.get("/")
def healthcheck() -> dict:
    return {"status": "OK"}


@app.post("/validate")
def validate(models: Blocks) -> Blocks:
    error_dict = UP42ParamaterValidator(input_parameters=models).check_parameters()
    import pdb;
    pdb.set_trace()
    return error_dict

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
