# Trust Trash — Modular Starter

A starter monorepo for **Trust Trash**, a Unified Data Intelligence Platform.

This repository establishes architectural boundaries and development entry points. It is **not** a complete implementation of universal search, connector synchronization, lakehouse processing, or AI pipelines.

## Architecture

- **Frontend:** Next.js App Router (`apps/web`)
- **Backend:** FastAPI with layered domain modules (`backend/src/trust_trash`)
- **Execution:** independent worker entry points (`backend/src/trust_trash/workers`)
- **Extension points:** connector SDK and processor SDK
- **Infrastructure:** Docker Compose for local PostgreSQL; optional OpenSearch and Redis profiles
- **Architecture records:** `docs/architecture` and `docs/adr`

The backend follows a **modular monolith** approach. Each domain module has Presentation, Application, Domain, and Infrastructure boundaries. Workers can be deployed separately while reusing the same application and domain packages. Extract a module into a microservice only when independent scaling, deployment, or fault isolation justifies it.

## Repository layout

```text
apps/                  Web UI and browser-extension starter
backend/               FastAPI backend and Python domain modules
contracts/             Cross-boundary schemas and event examples
docs/                  Product and architecture documentation
infra/                 Local development infrastructure
orchestration/         Dagster integration placeholder
scripts/               Local developer scripts
```

## Quick start — backend

Requirements: Python 3.12+ and `pip` (or use `uv`).

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
uvicorn trust_trash.bootstrap.app:app --reload
```

Open `http://localhost:8000/docs` and `http://localhost:8000/api/v1/health`.

## Quick start — infrastructure

```bash
cp .env.example .env
docker compose -f infra/compose/docker-compose.yml up -d postgres
```

Optional services:

```bash
docker compose -f infra/compose/docker-compose.yml --profile search up -d
# Prometheus/Grafana/Loki placeholders are under infra/monitoring.
```

OpenSearch and Redis are development dependencies here. Do not expose them publicly or reuse the local security configuration in production.

## Quick start — frontend

```bash
cd apps/web
npm install
npm run dev
```

## Development checks

```bash
cd backend
pytest
ruff check src tests
```

## Current implementation status

Implemented:
- FastAPI application bootstrap and health endpoint
- Configuration via environment variables
- Example Universal Resource and Search contracts
- Connector and Processor base contracts
- Domain-module scaffolds and router registration pattern
- Worker process entry points (idle placeholders)
- Basic backend smoke test

Not implemented yet:
- Real connector integrations or credential vault
- Search planner, OpenSearch indexing, Trino federation
- Ingestion queue, retries, CDC, streaming
- Data Lake / Warehouse pipelines
- OCR, NLP, CV or model inference
- Production authentication, authorization and tenant isolation

See `docs/architecture/implementation-status.md` before treating a placeholder as production functionality.
