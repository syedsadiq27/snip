from __future__ import annotations

from app.db import connect


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_valid_link(client, db_path):
    response = client.post(
        "/api/links",
        json={"url": "https://example.com/path"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["original_url"] == "https://example.com/path"
    assert body["visit_count"] == 0
    assert body["expires_at"] is None
    assert body["alias"]
    assert body["short_url"].endswith(f"/{body['alias']}")
    assert body["created_at"]

    conn = connect(db_path)
    row = conn.execute(
        "SELECT * FROM links WHERE alias = ?",
        (body["alias"],),
    ).fetchone()
    conn.close()
    assert row is not None
    assert row["original_url"] == "https://example.com/path"
    assert row["visit_count"] == 0


def test_create_with_custom_alias(client):
    response = client.post(
        "/api/links",
        json={"url": "https://example.com", "alias": "my-link"},
    )
    assert response.status_code == 201
    assert response.json()["alias"] == "my-link"


def test_duplicate_alias_conflict(client):
    first = client.post(
        "/api/links",
        json={"url": "https://example.com/one", "alias": "taken"},
    )
    assert first.status_code == 201

    second = client.post(
        "/api/links",
        json={"url": "https://example.com/two", "alias": "taken"},
    )
    assert second.status_code == 409
