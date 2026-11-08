from __future__ import annotations

import re
from datetime import datetime, timezone
from urllib.parse import urlparse

from fastapi import HTTPException

ALIAS_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")
MAX_URL_LENGTH = 2048
MIN_ALIAS_LENGTH = 3
MAX_ALIAS_LENGTH = 32
RESERVED_ALIASES = frozenset({"api", "health", "docs", "openapi.json", "redoc"})
ALLOWED_SCHEMES = frozenset({"http", "https"})


def validate_url(url: str) -> str:
    if not isinstance(url, str) or not url.strip():
        raise HTTPException(status_code=400, detail="URL is required")

    cleaned = url.strip()
    if len(cleaned) > MAX_URL_LENGTH:
        raise HTTPException(status_code=400, detail="URL exceeds maximum length of 2048")

    parsed = urlparse(cleaned)
    scheme = (parsed.scheme or "").lower()
    if scheme not in ALLOWED_SCHEMES:
        raise HTTPException(
            status_code=400,
            detail="URL scheme must be http or https",
        )
    if not parsed.netloc:
        raise HTTPException(status_code=400, detail="URL must include a network location")

    return cleaned


def validate_alias(alias: str | None) -> str | None:
    if alias is None:
        return None

    if not isinstance(alias, str):
        raise HTTPException(status_code=400, detail="Alias must be a string")

    cleaned = alias.strip()
    if not cleaned:
        raise HTTPException(status_code=400, detail="Alias cannot be empty")

    if len(cleaned) < MIN_ALIAS_LENGTH or len(cleaned) > MAX_ALIAS_LENGTH:
        raise HTTPException(
            status_code=400,
            detail="Alias must be between 3 and 32 characters",
        )

    if not ALIAS_PATTERN.fullmatch(cleaned):
        raise HTTPException(
            status_code=400,
            detail="Alias may only contain letters, digits, underscores, and hyphens",
        )

    if cleaned.lower() in RESERVED_ALIASES:
        raise HTTPException(status_code=400, detail="Alias is reserved")

    return cleaned


def validate_expires_at(expires_at: datetime | None) -> str | None:
    if expires_at is None:
        return None

    if expires_at.tzinfo is None:
        raise HTTPException(
            status_code=400,
            detail="expires_at must be timezone-aware",
        )

    now = datetime.now(timezone.utc)
    aware = expires_at.astimezone(timezone.utc)
    if aware <= now:
        raise HTTPException(
            status_code=400,
            detail="expires_at must be in the future",
        )

    return aware.isoformat().replace("+00:00", "Z")
