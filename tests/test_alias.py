from __future__ import annotations


def test_invalid_alias_too_short(client):
    response = client.post(
        "/api/links",
        json={"url": "https://example.com", "alias": "ab"},
    )
    assert response.status_code == 400


def test_invalid_alias_characters(client):
    response = client.post(
        "/api/links",
        json={"url": "https://example.com", "alias": "bad alias!"},
    )
    assert response.status_code == 400


def test_reserved_alias_rejected(client):
    for alias in ("api", "health", "docs", "openapi.json", "redoc", "API", "Health"):
        response = client.post(
            "/api/links",
            json={"url": "https://example.com", "alias": alias},
        )
        assert response.status_code == 400, alias


def test_auto_generated_alias(client):
    response = client.post(
        "/api/links",
        json={"url": "https://example.com/auto"},
    )
    assert response.status_code == 201
    alias = response.json()["alias"]
    assert 3 <= len(alias) <= 32
    assert all(c.isalnum() or c in "-_" for c in alias)
