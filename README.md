# my-playground — Azure File Upload Monorepo

A monorepo demonstrating a minimal file-upload workflow hosted on Azure.  
It contains a **React** frontend, a **FastAPI** backend, **Terraform** infrastructure,
and **Bruno** API documentation.

## Repository layout

```
.
├── apps/
│   ├── frontend/   # React + TypeScript (Vite, Jest, ESLint)
│   └── backend/    # FastAPI (uv, ruff, pyright strict, pytest)
├── infra/          # Terraform – Azure (Storage, Static Web App, App Service)
├── bruno/          # Bruno API collection
└── .github/        # GitHub Copilot instructions
```

## Quick start

### Prerequisites

| Tool | Version |
|------|---------|
| Node.js | ≥ 20 |
| Python | ≥ 3.12 |
| [uv](https://docs.astral.sh/uv/) | ≥ 0.4 |
| [Terraform](https://developer.hashicorp.com/terraform) | ≥ 1.8 |
| [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/) | ≥ 2.60 |

### 1 – Frontend

```bash
cd apps/frontend
npm install
npm run dev          # http://localhost:5173
npm test             # Jest unit tests
npm run lint         # ESLint
```

### 2 – Backend

```bash
cd apps/backend
uv sync              # installs deps into .venv
uv run uvicorn src.main:app --reload   # http://localhost:8000
uv run pytest        # run tests
uv run ruff check .  # lint
uv run pyright       # type-check
```

### 3 – Infrastructure

```bash
cd infra
cp terraform.tfvars.example terraform.tfvars   # fill in your values
terraform init
terraform plan
terraform apply
```

## Architecture

```
Browser
  │  POST /upload (multipart/form-data)
  ▼
Azure App Service (FastAPI)
  │  stream bytes
  ▼
Azure Blob Storage Container
```

The React SPA is served from an **Azure Static Web App**.  
Secrets (storage connection strings, SAS tokens) are stored in **Azure Key Vault**
and surfaced to App Service via Key Vault references in Application Settings.  
They are never committed to source control.

## Secrets management

* Local development: create `apps/backend/.env` (git-ignored) and set
  `AZURE_STORAGE_CONNECTION_STRING`.
* CI / production: store the secret in **Azure Key Vault** and reference it via
  `@Microsoft.KeyVault(...)` in App Service configuration, or inject it as a
  GitHub Actions secret.

## Contributing

See the README in each package for package-specific guidance.
