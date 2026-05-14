import jwt
from fastapi.security import HTTPAuthorizationCredentials

from app.configuration.settings import settings
from app.utils.auth import get_current_user


def _build_token(email: str) -> str:
    return jwt.encode(
        {"sub": email},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def test_get_current_user_accepts_valid_token():
    token = _build_token("student@unal.edu.co")
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token,
    )

    assert get_current_user(credentials) == "student@unal.edu.co"


def test_get_current_user_rejects_invalid_token():
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="invalid-token",
    )

    try:
        get_current_user(credentials)
        assert False, "Expected HTTPException"
    except Exception as exc:
        assert getattr(exc, "status_code", None) == 401
