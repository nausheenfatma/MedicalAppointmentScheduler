from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InputData(BaseModel):
    text: str

@app.post("/process")
def process(data: InputData):
    # simple "processing"
    result = data.text.upper()
    return {"processed": result}