from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.db import connect, init_db
from app.main import app


@pytest.fixture()
def db_path(tmp_path) -> str:
    path = str(tmp_path / "test.db")
    conn = connect(path)
    init_db(conn)
    conn.close()
    return path


@pytest.fixture()
def client(db_path: str, monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    monkeypatch.setenv("DATABASE_PATH", db_path)
    with TestClient(app) as test_client:
        yield test_client
