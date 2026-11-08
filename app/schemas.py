from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class CreateLinkRequest(BaseModel):
    url: str = Field(..., min_length=1)
    alias: str | None = None
    expires_at: datetime | None = None


class LinkResponse(BaseModel):
    alias: str
    short_url: str
    original_url: str
    created_at: str
    expires_at: str | None
    visit_count: int


class LinkStatsResponse(LinkResponse):
    expired: bool


class HealthResponse(BaseModel):
    status: str
