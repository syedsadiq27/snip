from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.db import connect


def test_stats_for_active_link(client):
    created = client.post(
        "/api/links",
        json={"url": "https://example.com/stats", "alias": "stats1"},
    )
    assert created.status_code == 201

    response = client.get("/api/links/stats1")
    assert response.status_code == 200
    body = response.json()
    assert body["alias"] == "stats1"
    assert body["original_url"] == "https://example.com/stats"
    assert body["visit_count"] == 0
    assert body["expired"] is False


def test_stats_for_expired_link(client, db_path):
    future = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    created = client.post(
        "/api/links",
        json={
            "url": "https://example.com/old",
            "alias": "oldlink",
            "expires_at": future,
        },
    )
    assert created.status_code == 201

    past = (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat().replace(
        "+00:00", "Z"
    )
    conn = connect(db_path)
    conn.execute(
        "UPDATE links SET expires_at = ? WHERE alias = ?",
        (past, "oldlink"),
    )
    conn.commit()
    conn.close()

    response = client.get("/api/links/oldlink")
    assert response.status_code == 200
    body = response.json()
    assert body["expired"] is True
    assert body["alias"] == "oldlink"


def test_stats_unknown_alias(client):
    response = client.get("/api/links/does-not-exist")
    assert response.status_code == 404
