from __future__ import annotations

import sqlite3
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.db import connect, init_db
from app.schemas import (
    CreateLinkRequest,
    HealthResponse,
    LinkResponse,
    LinkStatsResponse,
)
from app import service


def get_connection() -> sqlite3.Connection:
    conn = connect()
    try:
        yield conn
    finally:
        conn.close()


DbConn = Annotated[sqlite3.Connection, Depends(get_connection)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = connect()
    try:
        init_db(conn)
    finally:
        conn.close()
    yield


app = FastAPI(title="URL Shortener", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def request_base_url(request: Request) -> str:
    return str(request.base_url).rstrip("/")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/api/links", response_model=LinkResponse, status_code=201)
def create_link(
    payload: CreateLinkRequest,
    request: Request,
    conn: DbConn,
) -> LinkResponse:
    data = service.create_link(
        conn,
        url=payload.url,
        alias=payload.alias,
        expires_at=payload.expires_at,
        base_url=request_base_url(request),
    )
    return LinkResponse(**data)


@app.get("/api/links/{alias}", response_model=LinkStatsResponse)
def link_stats(alias: str, request: Request, conn: DbConn) -> LinkStatsResponse:
    data = service.get_stats(conn, alias, request_base_url(request))
    if data is None:
        raise HTTPException(status_code=404, detail="Link not found")
    return LinkStatsResponse(**data)


@app.get("/{alias}")
def redirect_alias(alias: str, conn: DbConn) -> RedirectResponse:
    row = service.record_visit(conn, alias)
    if row is None:
        existing = service.get_link_by_alias(conn, alias)
        if existing is not None and service.is_expired(existing["expires_at"]):
            raise HTTPException(status_code=404, detail="Link expired")
        raise HTTPException(status_code=404, detail="Link not found")
    return RedirectResponse(url=row["original_url"], status_code=307)
