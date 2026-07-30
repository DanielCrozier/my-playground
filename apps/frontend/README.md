# apps/frontend — React File Upload SPA

A minimal React 18 single-page application that lets users upload a file to the
FastAPI backend.  Served from an **Azure Static Web App**.

## Tech stack

| Tool | Purpose |
|------|---------|
| [React 18](https://react.dev/) | UI framework |
| [TypeScript](https://www.typescriptlang.org/) (strict) | Type safety |
| [Vite](https://vitejs.dev/) | Dev server & bundler |
| [Jest](https://jestjs.io/) + [React Testing Library](https://testing-library.com/) | Unit tests |
| [ESLint](https://eslint.org/) + [@typescript-eslint](https://typescript-eslint.io/) | Linting |

## Quick start

```bash
cd apps/frontend
npm install
npm run dev       # http://localhost:5173  (hot-module reload)
npm test          # Jest unit tests (single run)
npm run lint      # ESLint
npm run build     # Production bundle → dist/
```

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_BASE_URL` | `""` (same origin) | Base URL of the FastAPI backend |

Create a `.env.local` file (git-ignored) for local development:

```env
VITE_API_BASE_URL=http://localhost:8000
```

In the Azure Static Web App configuration set `VITE_API_BASE_URL` to your App
Service URL, or configure a
[proxy route](https://learn.microsoft.com/en-us/azure/static-web-apps/configuration#routing)
in `staticwebapp.config.json` to forward `/upload` to the backend.

## Project structure

```
src/
├── api/
│   └── upload.ts          # uploadFile() helper — POST /upload
├── components/
│   └── FileUpload.tsx      # File picker + upload form
├── __tests__/
│   ├── FileUpload.test.tsx # Component tests (React Testing Library)
│   └── upload.test.ts      # API helper unit tests
├── App.tsx
└── main.tsx
```

## Testing

```bash
npm test                      # watch mode
npm test -- --watchAll=false  # single run (CI)
```

## Linting

```bash
npm run lint          # report issues
npm run lint -- --fix # auto-fix where possible
```
