from fastapi.testclient import TestClient
# from .main import app
from fastapi import FastAPI
app = FastAPI()
client = TestClient(app)

def test_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message" : "Agentic AI Classes"}