# Backend – FastAPI

FastAPI service that accepts multipart file uploads and streams them to
**Azure Blob Storage**.

## Technology

| Tool | Purpose |
|------|---------|
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework |
| [uv](https://docs.astral.sh/uv/) | Package / venv management |
| [ruff](https://docs.astral.sh/ruff/) | Linting & formatting |
| [pyright](https://github.com/microsoft/pyright) | Static type checking (strict) |
| [pytest](https://pytest.org/) | Testing |
| [azure-storage-blob](https://pypi.org/project/azure-storage-blob/) | Azure SDK |

## Project layout

```
apps/backend/
├── src/
│   ├── __init__.py
│   ├── config.py          # Pydantic-settings configuration
│   ├── main.py            # App factory & CORS setup
│   ├── storage.py         # Azure Blob Storage client helper
│   └── routers/
│       ├── __init__.py
│       └── upload.py      # POST /upload endpoint
├── tests/
│   ├── conftest.py        # Shared fixtures
│   ├── test_config.py
│   ├── test_health.py
│   └── test_upload.py
├── .env.example
└── pyproject.toml
```

## Quick start

```bash
# 1. Install dependencies
uv sync --extra dev

# 2. Set up environment
cp .env.example .env
#    Edit .env and fill in AZURE_STORAGE_CONNECTION_STRING

# 3. Run the dev server
uv run uvicorn src.main:app --reload
#    API available at http://localhost:8000
#    Docs at          http://localhost:8000/docs
```

## API

### `POST /upload`

Accepts a `multipart/form-data` request with a single `file` field.

**Allowed content types:** `image/jpeg`, `image/png`, `image/gif`, `image/webp`,
`application/pdf`, `text/plain`, `text/csv`

**Maximum file size:** 10 MB (configurable via `MAX_UPLOAD_SIZE_BYTES`)

**Response (201):**

```json
{ "blob_name": "<uuid>-<original-filename>" }
```

## Development

```bash
# Lint
uv run ruff check .
uv run ruff format --check .

# Type-check
uv run pyright

# Test (with coverage)
uv run pytest

# Auto-fix lint issues
uv run ruff check --fix .
uv run ruff format .
```

## Configuration

All configuration is read from environment variables (or `.env`).

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AZURE_STORAGE_CONNECTION_STRING` | ✅ | — | Azure Storage connection string |
| `AZURE_STORAGE_CONTAINER_NAME` | | `uploads` | Blob container name |
| `ALLOW_ORIGINS` | | `http://localhost:5173` | Comma-separated CORS origins |
| `MAX_UPLOAD_SIZE_BYTES` | | `10485760` | Max upload size in bytes |

## Secrets management

* **Local:** copy `.env.example` → `.env`, fill in values. Never commit `.env`.
* **Production:** configure `AZURE_STORAGE_CONNECTION_STRING` in App Service
  Application Settings using an Azure Key Vault reference:
  `@Microsoft.KeyVault(SecretUri=https://<vault>.vault.azure.net/secrets/<name>/)`
