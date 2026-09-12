# AGENTS.md

## Project

Shopee Affiliate Market Intelligence System.

This is a semi-automated market research platform for Shopee Affiliate.

## Source of Truth

Before implementing any feature, read and follow:

1. docs/PRODUCT_VISION.md
2. docs/ARCHITECTURE.md
3. docs/DOMAIN_MODEL.md
4. docs/WORKFLOW.md
5. docs/DATA_CONTRACT.md
6. docs/AI_RULES.md

If code conflicts with these documents, the documents win.

Do not silently reinterpret product requirements.

## Core Rules

1. Data before AI.
2. Deterministic calculations before LLM analysis.
3. Raw source data is immutable.
4. No evidence = no factual AI claim.
5. Human approval is mandatory at configured workflow gates.
6. AI must never automatically approve workflow stages.
7. Missing data must remain missing.
8. Estimated data must be explicitly marked as estimated.
9. Every important claim must be traceable to evidence.
10. Do not implement anti-bot bypass, CAPTCHA bypass, credential farming, or unauthorized access.

## Development Method

For every task:

1. Read relevant docs.
2. Inspect existing code.
3. Write an implementation plan.
4. List files to modify.
5. Implement only the approved scope.
6. Add tests.
7. Run tests.
8. Report:
   - files changed
   - database changes
   - tests run
   - known limitations
   - remaining risks

Do not refactor unrelated modules unless required.

## Architecture

Use a modular monolith for V1.

Frontend:
Next.js + React + TypeScript.

Backend:
Python + FastAPI + Pydantic + SQLAlchemy + Alembic.

Primary database:
PostgreSQL.

Cache:
Redis.

Raw object storage:
MinIO / S3 compatible.

## Important

Do not build the complete application in one task.

Implement the system incrementally by approved milestones.