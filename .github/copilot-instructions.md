# GitHub Copilot Instructions

## Project overview

This is a monorepo for a minimal Azure-hosted **file-upload** application.

| Package | Technology | Purpose |
|---------|-----------|---------|
| `apps/frontend` | React 18 · TypeScript · Vite · Jest · ESLint | SPA served from Azure Static Web App |
| `apps/backend` | FastAPI · Python 3.12 · uv · ruff · pyright (strict) · pytest | API hosted on Azure App Service |
| `infra` | Terraform ≥ 1.8 (azurerm provider) | Provisions Azure resources |
| `bruno` | Bruno | API endpoint documentation |

## Architecture

```
Browser
  │  POST /upload  (multipart/form-data)
  ▼
Azure Static Web App  ──proxy──►  Azure App Service  (FastAPI)
                                         │
                                  stream to blob
                                         │
                                  Azure Blob Storage
                                  (Key Vault secret for conn string)
```

## Security

* **Secrets are never committed.** Use `.env` locally (git-ignored) or
  Azure Key Vault references in App Service Application Settings for production.
* The `AZURE_STORAGE_CONNECTION_STRING` environment variable must be set at
  runtime; the application will refuse to start without it.
* CORS is restricted to the Static Web App origin in production; any origin is
  allowed in development (`ALLOW_ORIGINS=*`).
* Uploaded files are validated for size and content-type before streaming.

## Development conventions

### General
* Follow the principle of least privilege – minimal permissions in Azure RBAC.
* All generated code must have tests.
* Keep secrets out of source control at all costs.

### Python (apps/backend)
* Package manager: **uv** (`uv sync`, `uv add`, `uv run`).
* Linter: **ruff** – run `uv run ruff check .` and `uv run ruff format .`.
* Type checker: **pyright** in **strict** mode – run `uv run pyright`.
* Tests: **pytest** – run `uv run pytest`.
* Project layout: `src/` layout with `src/main.py` as the entrypoint.
* Never use `Any` in type annotations unless absolutely unavoidable and
  documented with a comment.

### TypeScript / React (apps/frontend)
* Use **TypeScript strict mode** (`"strict": true` in tsconfig).
* Linter: **ESLint** with `@typescript-eslint/parser` and
  `plugin:@typescript-eslint/recommended` – run `npm run lint`.
* Tests: **Jest** + React Testing Library – run `npm test`.
* State: local React state only (no global state library) unless complexity grows.
* Components live in `src/components/`; API calls in `src/api/`.

### Terraform (infra)
* All resources are tagged with `environment`, `project`, and `managed_by=terraform`.
* Remote state should be configured before production use (see `infra/README.md`).
* Never hard-code secrets; pass them via `TF_VAR_*` or reference Key Vault.
* Run `terraform fmt -recursive` before committing.
* Run `terraform validate` before proposing changes.

### Bruno (bruno)
* Document every API endpoint.
* Use environment variables (`{{baseUrl}}`, `{{bearerToken}}`) – never hard-code URLs or tokens.

## Linting / testing quick reference

```bash
# Backend
cd apps/backend
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest

# Frontend
cd apps/frontend
npm run lint
npm test -- --watchAll=false

# Infra
cd infra
terraform fmt -recursive -check
terraform validate
```
