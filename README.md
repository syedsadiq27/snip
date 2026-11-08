# URL Shortener

Production-quality URL shortener built with FastAPI and SQLite.

## Requirements

- Python 3.11+

## Install

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Optional environment variable:

- `DATABASE_PATH` — SQLite database file path (default: `./data/shortener.db`)

## API

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/links` | Create a short link |
| `GET` | `/{alias}` | Redirect to the original URL |
| `GET` | `/api/links/{alias}` | Link stats |
| `GET` | `/health` | Health check |

### Create link

```bash
curl -X POST http://localhost:8000/api/links \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com","alias":"ex","expires_at":null}'
```

Response `201`:

```json
{
  "alias": "ex",
  "short_url": "http://localhost:8000/ex",
  "original_url": "https://example.com",
  "created_at": "2026-01-01T00:00:00Z",
  "expires_at": null,
  "visit_count": 0
}
```

## Test

```bash
pytest -q
```
