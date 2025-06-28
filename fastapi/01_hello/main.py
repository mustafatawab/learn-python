from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class MessageInput(BaseModel):
    role: str
    content: str

class InputClass(BaseModel):
    messages: list[MessageInput]

@app.post("/")
def root(input : InputClass):
    print(input.messages)
    print(input.model_dump())
    print(f'Data = {input}')
    return {"message" : "This is root", "data" : input}         