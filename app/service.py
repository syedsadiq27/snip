from __future__ import annotations

import secrets
import sqlite3
from datetime import datetime, timezone

from fastapi import HTTPException

from app.validation import validate_alias, validate_expires_at, validate_url

MAX_ALIAS_RETRIES = 5


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def generate_alias() -> str:
    return secrets.token_urlsafe(6)


def build_short_url(base_url: str, alias: str) -> str:
    return f"{base_url.rstrip('/')}/{alias}"


def create_link(
    conn: sqlite3.Connection,
    *,
    url: str,
    alias: str | None,
    expires_at: datetime | None,
    base_url: str,
) -> dict:
    original_url = validate_url(url)
    provided_alias = validate_alias(alias)
    expires_at_iso = validate_expires_at(expires_at)
    created_at = utc_now_iso()

    if provided_alias is not None:
        try:
            conn.execute(
                """
                INSERT INTO links (alias, original_url, created_at, expires_at, visit_count)
                VALUES (?, ?, ?, ?, 0)
                """,
                (provided_alias, original_url, created_at, expires_at_iso),
            )
            conn.commit()
        except sqlite3.IntegrityError as exc:
            conn.rollback()
            raise HTTPException(status_code=409, detail="Alias already taken") from exc
        row = get_link_by_alias(conn, provided_alias)
        assert row is not None
        return _row_to_link(row, base_url)

    last_error: Exception | None = None
    for _ in range(MAX_ALIAS_RETRIES):
        candidate = generate_alias()
        try:
            conn.execute(
                """
                INSERT INTO links (alias, original_url, created_at, expires_at, visit_count)
                VALUES (?, ?, ?, ?, 0)
                """,
                (candidate, original_url, created_at, expires_at_iso),
            )
            conn.commit()
            row = get_link_by_alias(conn, candidate)
            assert row is not None
            return _row_to_link(row, base_url)
        except sqlite3.IntegrityError as exc:
            conn.rollback()
            last_error = exc
            continue

    raise HTTPException(
        status_code=500,
        detail="Failed to generate a unique alias",
    ) from last_error


def get_link_by_alias(conn: sqlite3.Connection, alias: str) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM links WHERE alias = ? COLLATE NOCASE",
        (alias,),
    ).fetchone()


def is_expired(expires_at: str | None, now: str | None = None) -> bool:
    if expires_at is None:
        return False
    current = now if now is not None else utc_now_iso()
    return expires_at <= current


def record_visit(conn: sqlite3.Connection, alias: str) -> sqlite3.Row | None:
    now = utc_now_iso()
    cursor = conn.execute(
        """
        UPDATE links
        SET visit_count = visit_count + 1
        WHERE alias = ? COLLATE NOCASE
          AND (expires_at IS NULL OR expires_at > ?)
        """,
        (alias, now),
    )
    conn.commit()
    if cursor.rowcount == 0:
        return None
    return get_link_by_alias(conn, alias)


def get_stats(conn: sqlite3.Connection, alias: str, base_url: str) -> dict | None:
    row = get_link_by_alias(conn, alias)
    if row is None:
        return None
    data = _row_to_link(row, base_url)
    data["expired"] = is_expired(row["expires_at"])
    return data


def _row_to_link(row: sqlite3.Row, base_url: str) -> dict:
    return {
        "alias": row["alias"],
        "short_url": build_short_url(base_url, row["alias"]),
        "original_url": row["original_url"],
        "created_at": row["created_at"],
        "expires_at": row["expires_at"],
        "visit_count": row["visit_count"],
    }
