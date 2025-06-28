from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    """ Root URL """
    return {"Message" : "This is root url"}


@app.get("/home")
def home():
    return {"message" : "Home Page"}


@app.post("/chat/start")
def chat_start(msg: dict):
    return {"msg" : "ok" , "data" : msg}



