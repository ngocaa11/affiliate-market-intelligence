# Shopee Affiliate Market Intelligence

An evidence-first, human-gated research workspace for Shopee Affiliate market intelligence. V1 is a modular monolith with a FastAPI API, Next.js web app, PostgreSQL, Redis, and MinIO.

## Phase A quick start

1. Copy configuration: `cp .env.example .env` and replace local secrets.
2. Start the stack: `docker compose up --build`.
3. Open the workspace at <http://localhost:3000> and API docs at <http://localhost:8000/docs>.

The API container runs `alembic upgrade head` before startup. PostgreSQL is the primary database; Redis and MinIO are provisioned now for Phase B data pipelines.

## Local development

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
export DATABASE_URL=sqlite:///./local.sqlite3
alembic upgrade head
uvicorn app.main:app --app-dir apps/api --reload
```

In another terminal:

```bash
cd apps/web
npm install
npm run dev
```

## Verification

```bash
pytest
ruff check .
cd apps/web && npm test && npm run build
```

See `docs/IMPLEMENTATION_PLAN.md` for the complete phased plan and `docs/BUILD_STATUS.md` for the living milestone checklist.
