# Implementation Plan

**Status:** Approved execution plan  
**Architecture:** V1 modular monolith  
**Source of truth:** `PRODUCT_VISION.md`, `ARCHITECTURE.md`, `DOMAIN_MODEL.md`, `WORKFLOW.md`, `DATA_CONTRACT.md`, and `AI_RULES.md`

## 1. Delivery principles

- Preserve raw payloads and historical snapshots; never infer a missing value as zero.
- Keep platform collection behind versioned connector contracts and canonical records.
- Run deterministic validation and analytics before constructing evidence packs for AI.
- Persist workflow state, immutable package versions, evidence references, decisions, and audit events.
- Require a human actor at every configured approval gate; AI may never approve a stage.
- Clearly expose source, confidence, coverage, freshness, estimation, and anomaly status.
- Use mock/fixture connectors only when explicitly labelled `MOCK`; unavailable legitimate sources remain `NOT_CONFIGURED`.

## 2. Epics and modules

| Epic | Modules | Outcome |
|---|---|---|
| A. Foundation | `research`, `workflow`, `evidence`, API, web workspace, infrastructure | Projects, versioned scopes, gated stages, evidence actions, packages, auditability |
| B. Data platform | `source`, `lineage`, connector SDK, raw object storage, validation, snapshots, source health | Replaceable and observable collection-to-snapshot pipelines |
| C. Analytics | `market`, `customer`, `search`, `commerce`, `content`, `analytics` | Versioned deterministic metrics and opportunity intelligence |
| D. Evidence-bound AI | `intelligence`, evidence packs, policy guard, prompt/run registry | Structured FACT/INFERENCE/HYPOTHESIS analysis without unsupported claims |
| E. Affiliate strategy | `affiliate`, matching, forecasting, `strategy` | Economics scenarios, positioning, content system, and a 30-day test plan |
| F. Product completion | dashboards, drill-downs, security, deployment, operations | Tested, documented local and production-ready product |

## 3. Milestones, dependencies, and acceptance criteria

### Phase A — Foundation

1. **A1 Application skeleton and environment**
   - Dependencies: none.
   - Deliverables: FastAPI app, Next.js app, typed settings, Docker Compose for PostgreSQL/Redis/MinIO, health endpoint.
   - Acceptance: apps start with documented commands; secrets are environment-only; health check reports service identity.
2. **A2 Foundation domain and migration**
   - Dependencies: A1.
   - Deliverables: SQLAlchemy entities and Alembic baseline for projects, scopes, workflow, stage packages, evidence, notes, decisions, and audit events.
   - Acceptance: schema upgrades from an empty database; scope and package histories are append-only/versioned.
3. **A3 Research project and scope API**
   - Dependencies: A2.
   - Deliverables: create/list/read project APIs; versioned scope creation/read APIs; four entry modes.
   - Acceptance: invalid mode inputs fail; every project begins in persisted `DRAFT`; scope changes produce a new version.
4. **A4 Workflow, human gates, and stage packages**
   - Dependencies: A2–A3.
   - Deliverables: canonical state machine, mode-specific stage sequence, transition preconditions, package versioning, approval/rejection/research-more/go-back decisions.
   - Acceptance: machine and human transition authority is enforced; AI approval is rejected; subsequent stages only receive approved packages; all decisions are audited.
5. **A5 Evidence and audit system**
   - Dependencies: A2–A4.
   - Deliverables: traceable evidence records, pin/reject/note actions, actor-aware immutable audit events.
   - Acceptance: evidence contains source/timestamp/confidence/freshness; rejected evidence cannot enter approved packages; actions remain traceable.
6. **A6 Research Workspace UI**
   - Dependencies: A3–A5.
   - Deliverables: project creation/list, three-panel workspace, status/stage display, evidence inspection and human decision controls.
   - Acceptance: a user can create a project, inspect source metadata, pin/reject/note evidence, and operate an eligible human gate; empty/error/loading states are visible.

### Phase B — Data

1. **B1 Raw storage and lineage** — Depends on A2; immutable S3 objects, checksums, SourceRun metadata, idempotent request fingerprints.
2. **B2 Quality and anomaly pipeline** — Depends on B1; schema/semantic/temporal validation, fail-closed blocking, drift incidents.
3. **B3 Connector framework and source health** — Depends on B1–B2; common discover/collect/store/parse/validate/normalize/health contract and telemetry.
4. **B4 Commerce connectors and snapshots** — Depends on B3; legitimate Shopee/import path plus clearly marked fixtures; category/shop/product snapshots.
5. **B5 Search and content connectors** — Depends on B3; keyword/search abstraction, YouTube API connector, and TikTok `NOT_CONFIGURED` unless legitimate access exists.
6. **B6 Data workspace integration** — Depends on B4–B5; raw/normalized drill-down, quality incidents, freshness and source health.

Acceptance: every normalized record traces to an immutable raw object; missing values remain null; mock and unavailable connectors are unmistakably labelled; a connector failure is isolated.

### Phase C — Analytics and intelligence

1. **C1 Metric framework** — Versioned formulas and input references.
2. **C2 Market/search/commerce metrics** — Growth, velocity, acceleration, breadth, concentration, density, momentum, and outliers.
3. **C3 Customer/keyword intelligence** — Evidence-linked segments, JTBD/problem structures, keyword clusters and buyer intent.
4. **C4 Opportunity engines** — Category, niche/micro-niche, identity resolution, Product Radar, Content Intelligence and Content Gap.
5. **C5 Three-signal synthesis** — Search × Content × Commerce correlation with confidence, coverage and freshness.

Acceptance: results are reproducible from recorded inputs/formula versions; blocking anomalies are excluded; scores are identified as heuristics rather than probabilities.

### Phase D — Evidence-bound AI

1. **D1 Evidence Pack builder** — Approved-package-only, read-only AI context with a stable hash.
2. **D2 Structured analysis service** — Required observations/claims/unknowns/risks/recommendations schema and run versioning.
3. **D3 Policy guard** — Evidence enforcement, claim classification, conflict and insufficient-data behavior.
4. **D4 Hallucination suite** — Missing, single-outlier, proxy, conflicting-source, rejected-hypothesis, and estimated-GMV cases.

Acceptance: every FACT cites evidence; missing inputs yield `INSUFFICIENT_DATA`; AI cannot mutate approval state; model/prompt/evidence-pack versions are retained.

### Phase E — Affiliate and strategy

1. **E1 Commission import/snapshots** — Actual or user-imported commission with lineage.
2. **E2 Affiliate Economics** — Deterministic LOW/BASE/HIGH forecasts with explicit assumptions.
3. **E3 Product × Content matching** — Customer, commerce, competition, content and commission-aware fit.
4. **E4 Strategy Builder** — Beachhead customer, positioning, pillars, traffic/trust/bridge/money content, and a 30-day plan.

Acceptance: forecast math is code-owned; unknown commission remains unknown; all recommendations trace to approved evidence and display risks.

### Phase F — Product completion

1. **F1 UX completion** — Dashboard polish, confidence/coverage/freshness, source/evidence drill-downs, empty and error states.
2. **F2 End-to-end and security** — Complete workflow E2E, authorization boundaries, secret/privacy and dependency review.
3. **F3 Operations and documentation** — Local deployment, backups, observability, runbooks and production guide.

Acceptance: all 18 completion journeys work; automated suites pass; non-technical local setup and production operations are documented.

## 4. Database entities

### Foundation

- `research_projects`, `research_scopes`, `research_workflows`
- `stage_packages`, `research_decisions`
- `evidence`, `evidence_actions`, `user_notes`, `audit_events`

### Data and analytics

- `data_sources`, `source_runs`, `raw_objects`, `data_quality_results`, `schema_drift_incidents`
- `categories`, `niches`, `micro_niches`, `market_snapshots`
- `shops`, `brands`, `products`, `product_listings`, `product_snapshots`
- `keywords`, `keyword_platform_refs`, `keyword_snapshots`, `keyword_clusters`, `search_signals`
- `creators`, `content_items`, `content_snapshots`, `content_topics`, `content_signals`, `outliers`
- `derived_metrics`, `opportunity_scores`, `identity_matches`

### AI, affiliate, and strategy

- `claims`, `hypotheses`, `evidence_packs`, `ai_runs`
- `affiliate_products`, `commission_snapshots`, `affiliate_performance`, `revenue_scenarios`
- `positionings`, `content_pillars`, `content_ideas`, `strategy_plans`

All mutable market facts use snapshots rather than historical updates. JSON payloads preserve flexible domain artifacts, while indexed relational columns enforce identity, state, lineage, and gate invariants.

## 5. API surface

- `/api/v1/health`
- `/api/v1/projects` and `/api/v1/projects/{project_id}`
- `/api/v1/projects/{project_id}/scopes`
- `/api/v1/projects/{project_id}/workflow`, `/machine-transitions`, and `/decisions`
- `/api/v1/projects/{project_id}/packages`
- `/api/v1/projects/{project_id}/evidence` and `/evidence/{evidence_id}/actions`
- `/api/v1/projects/{project_id}/notes` and `/audit`
- Phase B: sources, runs, imports, raw records, quality incidents, snapshots and health
- Phase C: metrics, signals, radar, opportunities and correlations
- Phase D: evidence packs and analyses
- Phase E: commissions, forecasts, matching and strategy plans

Mutations use application services, actor identity, validation, transactions, and audit logging. AI-facing endpoints never expose approval mutations.

## 6. Frontend screens

1. Project dashboard and creation flow with four modes.
2. Research Workspace with Evidence, Analysis, and Decision panels.
3. Scope and source configuration.
4. Market/Category/Niche explorers.
5. Customer, Search, Commerce, Product Radar, Content and Content Gap views.
6. Affiliate Economics and Strategy Builder.
7. Source health, data-quality and raw/normalized drill-down views.
8. Audit timeline, package history and evidence drill-down.

## 7. Data pipelines and connector architecture

Pipeline: `COLLECT → RAW STORED → SCHEMA VALIDATION → SEMANTIC VALIDATION → ANOMALY CHECK → NORMALIZE → SNAPSHOT → EVIDENCE/METRICS`.

Each connector implements `discover`, `collect`, `store_raw`, `parse`, `validate`, `normalize`, and `health_check`. Connector manifests record access mode, status (`READY`, `MOCK`, `NOT_CONFIGURED`, `DEGRADED`), version, schema/normalizer versions, freshness SLA and licensing notes. Canonical normalization output isolates analytics from platform-specific APIs or HTML.

## 8. Test strategy

- Backend unit tests: state transitions, authority, versioning, immutability, evidence eligibility, actor/audit behavior.
- Contract tests: source metadata, missing/estimated fields, snapshot idempotency, metric formulas and claim citations.
- API integration tests: project-to-approved-stage journeys and invalid/bypass attempts.
- Migration tests: upgrade from empty PostgreSQL and schema/model consistency.
- Connector tests: recorded fixtures without fabricated production status; drift and partial-failure cases.
- Frontend tests: components, accessible actions, status/error/empty states.
- Playwright E2E: four entry modes and complete gated workflow.
- Security checks: authorization, secret leakage, unsafe object access, dependency/static analysis.

## 9. Major risks and documented ambiguities

- Shopee and TikTok availability, licensing, rate limits and fields vary by geography/provider. No production connector will be called ready without legitimate access and verified contracts.
- The source documents define transition authority but not authentication/roles. V1 will require explicit actor headers and reject AI approval; production authorization roles are a security-completion dependency.
- The precise stage reached after `STAGE_APPROVED → NEXT_STAGE` differs by entry mode. The workflow will use explicit, tested mode-specific sequences that converge on canonical stages without skipping the required Scope gate.
- Confidence thresholds are examples, not fixed business policy. Store formula/policy versions and make thresholds configurable.
- Retention defaults and production topology depend on expected volume and compliance needs; preserve configurable defaults and document operational choices.
- PostgreSQL JSON and constraints can differ from lightweight test databases; migration verification must run against PostgreSQL in integration/CI.

## 10. Checkpoints

- **Checkpoint A:** Phase A complete and passing.
- **Checkpoint B:** Phase B complete and passing.
- **Checkpoint C:** Phases C and D complete and passing.
- **Checkpoint D:** Phases E and F complete; full application acceptance complete.

