import time
from pathlib import Path
from typing import Any

import jwt
import pytest
from fastapi.testclient import TestClient

from app.main import create_app

TEST_JWT_SECRET = "Fictional-Test-Only-Signing-Key-32-Bytes-Minimum"


def token(
    username: str = "student",
    role: str = "STUDENT",
    secret: str = TEST_JWT_SECRET,
    expires_at: int | None = None,
    algorithm: str = "HS256",
) -> str:
    now = int(time.time())
    return jwt.encode(
        {
            "sub": username,
            "role": role,
            "iat": now,
            "exp": expires_at if expires_at is not None else now + 3600,
        },
        secret,
        algorithm=algorithm,
    )


def headers(username: str = "student", role: str = "STUDENT") -> dict[str, str]:
    return {"Authorization": f"Bearer {token(username, role)}"}


def test_lists_seeded_tasks(tmp_path: Path) -> None:
    app = create_app(str(tmp_path / "workshop.db"), str(tmp_path / "uploads"), TEST_JWT_SECRET)
    with TestClient(app) as client:
        response = client.get("/api/tasks", headers=headers())
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_creates_task_and_summary(tmp_path: Path) -> None:
    app = create_app(str(tmp_path / "workshop.db"), str(tmp_path / "uploads"), TEST_JWT_SECRET)
    with TestClient(app) as client:
        created = client.post(
            "/api/tasks",
            headers=headers(),
            json={"title": "Add tests", "description": "Improve coverage", "status": "TODO", "priority": "HIGH"},
        )
        summary = client.get("/api/summary", headers=headers())
    assert created.status_code == 201
    assert created.json()["owner"] == "student"
    assert summary.json()["total"] == 3


def test_uploads_requirement(tmp_path: Path) -> None:
    upload_dir = tmp_path / "uploads"
    app = create_app(str(tmp_path / "workshop.db"), str(upload_dir), TEST_JWT_SECRET)
    with TestClient(app) as client:
        response = client.post(
            "/api/requirements",
            headers=headers(),
            files={"file": ("requirements.txt", b"Login must be accessible", "text/plain")},
        )
    assert response.status_code == 201
    assert (upload_dir / "requirements.txt").exists()


@pytest.mark.parametrize(
    ("authorization", "method", "path", "request_kwargs"),
    [
        (authorization, method, path, request_kwargs)
        for authorization in (
            None,
            "Basic invalid",
            "Bearer malformed",
            f"Bearer {token(secret='different-test-signing-key-that-is-long-enough')}",
            f"Bearer {token(expires_at=int(time.time()) - 1)}",
            f"Bearer {token(algorithm='HS512')}",
        )
        for method, path, request_kwargs in (
            ("GET", "/api/tasks", {}),
            ("POST", "/api/tasks", {"json": {"title": "test"}}),
            ("GET", "/api/summary", {}),
            ("POST", "/api/requirements", {"files": {"file": ("req.txt", b"requirements")}}),
            ("GET", "/api/backend-health", {}),
        )
    ],
)
def test_rejects_invalid_token(
    tmp_path: Path,
    authorization: str | None,
    method: str,
    path: str,
    request_kwargs: dict[str, Any],
) -> None:
    app = create_app(str(tmp_path / "workshop.db"), str(tmp_path / "uploads"), TEST_JWT_SECRET)
    request_headers = {"Authorization": authorization} if authorization is not None else {}
    with TestClient(app) as client:
        response = client.request(method, path, headers=request_headers, **request_kwargs)
    assert response.status_code == 401
    assert response.json() == {"detail": "ocurrio un error"}


def test_requires_configured_jwt_secret(tmp_path: Path) -> None:
    app = create_app(str(tmp_path / "workshop.db"), str(tmp_path / "uploads"), "too-short")
    with pytest.raises(RuntimeError, match="AUTH_JWT_SECRET must contain at least 32 bytes"):
        with TestClient(app):
            pass
