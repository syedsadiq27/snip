from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.db import connect


def test_past_expires_at_on_create(client):
    past = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    response = client.post(
        "/api/links",
        json={"url": "https://example.com", "expires_at": past},
    )
    assert response.status_code == 400


def test_naive_expires_at_rejected(client):
    naive = (datetime.now(timezone.utc) + timedelta(hours=1)).replace(tzinfo=None)
    response = client.post(
        "/api/links",
        json={"url": "https://example.com", "expires_at": naive.isoformat()},
    )
    assert response.status_code == 400


def test_expired_redirect_404_visit_unchanged(client, db_path):
    future = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    created = client.post(
        "/api/links",
        json={
            "url": "https://example.com/expiring",
            "alias": "expire-me",
            "expires_at": future,
        },
    )
    assert created.status_code == 201

    past = (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat().replace(
        "+00:00", "Z"
    )
    conn = connect(db_path)
    conn.execute(
        "UPDATE links SET expires_at = ?, visit_count = 0 WHERE alias = ?",
        (past, "expire-me"),
    )
    conn.commit()
    conn.close()

    response = client.get("/expire-me", follow_redirects=False)
    assert response.status_code == 404

    conn = connect(db_path)
    row = conn.execute(
        "SELECT visit_count FROM links WHERE alias = ?",
        ("expire-me",),
    ).fetchone()
    conn.close()
    assert row["visit_count"] == 0
