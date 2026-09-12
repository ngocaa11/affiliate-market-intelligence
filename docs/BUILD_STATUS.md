# Build Status

Allowed states: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETE`.

This checklist is updated after implementation and verification. A milestone is `COMPLETE` only when its acceptance criteria and relevant automated checks pass.

## Phase A — Foundation

- [ ] **BLOCKED — A1:** Repository/application skeleton and environment configuration — implemented; runtime verification awaits dependency installation because package registries return HTTP 403 in this environment
- [ ] **BLOCKED — A2:** PostgreSQL, Redis, MinIO, domain models and migrations — implemented; PostgreSQL migration execution awaits runtime dependencies/container images
- [ ] **BLOCKED — A3:** Research Project and versioned Research Scope — implemented; API tests are written but cannot import unavailable FastAPI/SQLAlchemy packages
- [ ] **BLOCKED — A4:** Workflow state machine, human approval gates and stage packages — implemented; API tests are written but cannot import unavailable FastAPI/SQLAlchemy packages
- [ ] **BLOCKED — A5:** Evidence system and audit log — implemented; API tests are written but cannot import unavailable FastAPI/SQLAlchemy packages
- [ ] **BLOCKED — A6:** Research Workspace UI — implemented; build, unit tests, and required screenshot await unavailable npm dependencies

## Phase B — Data

- [ ] **NOT_STARTED — B1:** Immutable raw storage, SourceRun and lineage
- [ ] **NOT_STARTED — B2:** Validation, anomaly handling and schema drift
- [ ] **NOT_STARTED — B3:** Connector framework and source health monitoring
- [ ] **NOT_STARTED — B4:** Shopee/import connector and commerce snapshots
- [ ] **NOT_STARTED — B5:** Search, YouTube and legitimate TikTok connector architecture
- [ ] **NOT_STARTED — B6:** Data workspace integration

## Phase C — Analytics and intelligence

- [ ] **NOT_STARTED — C1:** Deterministic metric framework
- [ ] **NOT_STARTED — C2:** Growth, velocity, acceleration, breadth, concentration, density, momentum and outliers
- [ ] **NOT_STARTED — C3:** Customer intelligence, keyword clustering and buyer intent
- [ ] **NOT_STARTED — C4:** Category/niche engines, identity resolution, Product Radar, Content Intelligence and Content Gap
- [ ] **NOT_STARTED — C5:** Search × Content × Commerce correlation

## Phase D — Evidence-bound AI

- [ ] **NOT_STARTED — D1:** Evidence Pack builder
- [ ] **NOT_STARTED — D2:** Evidence-bound structured AI analysis
- [ ] **NOT_STARTED — D3:** FACT / INFERENCE / HYPOTHESIS and `INSUFFICIENT_DATA` policy guard
- [ ] **NOT_STARTED — D4:** Research-more recommendations and hallucination guard tests

## Phase E — Affiliate and strategy

- [ ] **NOT_STARTED — E1:** Commission model and import
- [ ] **NOT_STARTED — E2:** Affiliate Economics and LOW / BASE / HIGH forecasts
- [ ] **NOT_STARTED — E3:** Product × Content matching
- [ ] **NOT_STARTED — E4:** Beachhead Customer, Positioning, Content Pillars and Strategy Builder
- [ ] **NOT_STARTED — E5:** Traffic, Trust, Bridge and Money content plus 30-day test plan

## Phase F — Product completion

- [ ] **NOT_STARTED — F1:** Dashboard polish, confidence/coverage/freshness and drill-down UX
- [ ] **NOT_STARTED — F2:** Error states, empty states and end-to-end workflow testing
- [ ] **NOT_STARTED — F3:** Security review
- [ ] **NOT_STARTED — F4:** Documentation and local deployment
- [ ] **NOT_STARTED — F5:** Production deployment guide and final acceptance

## Current checkpoint

Phase A implementation is present, and static Python checks pass. Checkpoint A is not yet reached because this environment cannot download the declared Python or npm dependencies, so runtime, migration, frontend build, and screenshot verification remain blocked. No later phase has started.
