# Bruno — API Collection

API endpoint documentation for the **my-playground** file-upload API.

## Prerequisites

Install [Bruno](https://www.usebruno.com/) (desktop app or CLI).

## Structure

```
bruno/
├── bruno.json              # Collection metadata
├── health.bru              # GET  /health — liveness probe
├── upload.bru              # POST /upload — file upload
└── environments/
    ├── local.json          # http://localhost:8000
    └── production.json     # Your deployed App Service URL
```

## Usage

### Desktop app

1. Open Bruno and click **Open Collection**.
2. Select this `bruno/` directory.
3. Choose the **local** environment for local development or **production** for
   the deployed API.
4. Run requests individually or use the **Run Collection** button.

### CLI

```bash
# Install the Bruno CLI
npm install -g @usebruno/cli

# Run all requests against the local environment
cd bruno
bru run --env local

# Run against production
bru run --env production
```

## Environments

| Variable | Description |
|----------|-------------|
| `baseUrl` | Base URL of the FastAPI backend (no trailing slash) |

Update `environments/production.json` with your deployed App Service URL, or
set `BACKEND_URL` in your shell and reference it via `{{BACKEND_URL}}`.

> **Never** hard-code URLs or tokens directly in `.bru` files — always use
> environment variables.
