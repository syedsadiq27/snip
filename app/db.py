from __future__ import annotations

import os
import sqlite3
from pathlib import Path

DEFAULT_DATABASE_PATH = "./data/shortener.db"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alias TEXT NOT NULL UNIQUE COLLATE NOCASE,
    original_url TEXT NOT NULL,
    created_at TEXT NOT NULL,
    expires_at TEXT NULL,
    visit_count INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_links_expires_at ON links(expires_at);
"""


def get_database_path() -> str:
    return os.environ.get("DATABASE_PATH", DEFAULT_DATABASE_PATH)


def connect(db_path: str | None = None) -> sqlite3.Connection:
    path = db_path if db_path is not None else get_database_path()
    parent = Path(path).resolve().parent
    parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_SQL)
    conn.commit()
