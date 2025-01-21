from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_generate_story():
    response = client.post("/generate/", json={"prompt": "Il était une fois..."})
    assert response.status_code == 200
    assert "story" in response.json()