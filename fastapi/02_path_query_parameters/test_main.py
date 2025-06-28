from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_call_info():
    reponse = client.get('info/test/23')
    assert response.status.code == 200
    assert response.json() == { "username" : "test", "user_id" : 23 }