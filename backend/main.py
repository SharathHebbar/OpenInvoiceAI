from fastapi import FastAPI
from pydantic import BaseModel


class Request(BaseModel):
    text: str

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.post("/test")
def test(request: Request):
    return {"message": f"Received text: {request.text}"}