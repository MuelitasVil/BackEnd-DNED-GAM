import jwt
from fastapi.testclient import TestClient

from app.configuration.settings import settings
from app.main import app

client = TestClient(app)


def _build_token(email: str) -> str:
    return jwt.encode(
        {"sub": email},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def test_root_requires_token():
    response = client.get("/")
    assert response.status_code == 401


def test_root_accepts_valid_token():
    token = _build_token("student@unal.edu.co")
    response = client.get(
        "/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == {"Hello": "World GAM"}
