from __future__ import annotations

from fastapi.testclient import TestClient

from app.db import connect
from app.main import app


def test_redirect_increments_visit(client, db_path):
    created = client.post(
        "/api/links",
        json={"url": "https://example.com/dest", "alias": "goto"},
    )
    assert created.status_code == 201

    response = client.get("/goto", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com/dest"

    stats = client.get("/api/links/goto")
    assert stats.status_code == 200
    assert stats.json()["visit_count"] == 1

    conn = connect(db_path)
    row = conn.execute(
        "SELECT visit_count FROM links WHERE alias = ?",
        ("goto",),
    ).fetchone()
    conn.close()
    assert row["visit_count"] == 1


def test_visit_persists_across_new_client(db_path, monkeypatch):
    monkeypatch.setenv("DATABASE_PATH", db_path)

    with TestClient(app) as first_client:
        created = first_client.post(
            "/api/links",
            json={"url": "https://example.com/persist", "alias": "persist"},
        )
        assert created.status_code == 201
        redirect = first_client.get("/persist", follow_redirects=False)
        assert redirect.status_code == 307

    with TestClient(app) as second_client:
        stats = second_client.get("/api/links/persist")
        assert stats.status_code == 200
        assert stats.json()["visit_count"] == 1


def test_redirect_missing_alias(client):
    response = client.get("/missing", follow_redirects=False)
    assert response.status_code == 404
