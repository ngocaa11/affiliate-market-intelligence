# ARCHITECTURE
## Shopee Affiliate Market Intelligence System

**Version:** 0.1  
**Architecture style:** Modular monolith first, service-ready later

---

## 1. Architectural principles

1. API-first, connector-based ingestion.
2. Immutable raw data.
3. Deterministic calculations before AI.
4. Human approval before high-impact transitions.
5. Evidence-bound AI.
6. Replaceable connectors.
7. Versioned research artifacts.
8. Fail closed on bad data.
9. Modular monolith for V1.
10. Scale only where real bottlenecks appear.

---

## 2. High-level architecture

```text
USER
 │
 ▼
WEB APP / RESEARCH WORKSPACE
 │
 ▼
APPLICATION API
 │
 ├──────────────► WORKFLOW ENGINE
 │                    ├── Human Gates
 │                    ├── Stage Packages
 │                    └── Versioning
 │
 ├──────────────► ANALYTICS ENGINE
 │                    ├── Metrics
 │                    ├── Scores
 │                    └── Forecasts
 │
 ├──────────────► AI INTELLIGENCE ENGINE
 │                    ├── Classification
 │                    ├── Clustering
 │                    ├── Interpretation
 │                    └── Hypothesis generation
 │
 └──────────────► DATA ACCESS LAYER
                      │
             ┌────────┼─────────┐
             ▼        ▼         ▼
         Postgres   Object    Redis
                    Storage
                      ▲
                      │
                DATA PIPELINE
                      ▲
             ┌────────┼─────────────┐
             ▼        ▼             ▼
          Shopee   Search        Content
         Connector Connectors    Connectors
```

---

## 3. Recommended technology stack

### Frontend
- Next.js / React / TypeScript
- TanStack Query
- ECharts hoặc Recharts
- shadcn/ui hoặc tương đương

### Backend
- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic

### Data
- PostgreSQL
- MinIO local / S3-compatible production
- Redis

### Workflow
- Prefect cho data jobs
- application state machine cho research workflow
- LangGraph chỉ cho AI/HITL subflows khi cần

### Crawling
- Official APIs first
- HTTP clients
- Crawlee / Playwright nơi phù hợp và được phép

### Testing
- Pytest
- Playwright E2E
- Vitest/Jest frontend

### Deployment
- Docker Compose first
- Kubernetes chỉ khi có nhu cầu thật

---

## 4. Repository layout

```text
affiliate-market-intelligence/
├── apps/
│   ├── web/
│   └── api/
├── modules/
│   ├── research/
│   ├── workflow/
│   ├── evidence/
│   ├── market/
│   ├── customer/
│   ├── search/
│   ├── commerce/
│   ├── content/
│   ├── affiliate/
│   ├── analytics/
│   ├── intelligence/
│   └── strategy/
├── connectors/
│   ├── shopee/
│   ├── youtube/
│   ├── tiktok/
│   ├── google/
│   └── providers/
├── workers/
├── infrastructure/
│   ├── docker/
│   ├── prefect/
│   └── migrations/
├── tests/
├── docs/
└── docker-compose.yml
```

---

## 5. Modular monolith first

V1 không nên bắt đầu bằng microservices vì workflow và data contracts còn thay đổi. Boundaries vẫn phải rõ để sau này tách collectors, analytics, AI workers hoặc snapshot processing mà không viết lại domain logic.

---

## 6. Connector architecture

Mỗi source implement cùng contract:

```python
class Connector:
    def discover(self, scope): ...
    def collect(self, request): ...
    def store_raw(self, raw_payload): ...
    def parse(self, raw_payload): ...
    def validate(self, parsed): ...
    def normalize(self, validated): ...
    def health_check(self): ...
```

Analytics không được phụ thuộc trực tiếp vào HTML/API response riêng của platform.

Priority:
1. Official API
2. User-authorized source
3. Licensed provider
4. Public data
5. Public browser collection nơi được phép

---

## 7. Raw data layer

Path convention:

```text
/raw/{source}/{yyyy}/{mm}/{dd}/{run_id}/{object_id}.json
```

Metadata Postgres:
- source_run_id
- request scope
- fetch time
- parser version
- checksum
- raw path
- status

Raw payload không được AI sửa.

---

## 8. Normalization layer

Mục tiêu:
- source-specific schema → canonical schema,
- giữ lineage,
- không mất raw fields quan trọng,
- đánh dấu estimated fields.

Mọi mapping phải versioned.

---

## 9. Snapshot architecture

Entity biến động phải có snapshot:
- product
- shop
- keyword
- content
- creator
- commission
- market/category

Không update-in-place lịch sử.

---

## 10. Deterministic analytics engine

Mọi phép tính số phải nằm ở code:
- growth_7d/30d/90d
- velocity
- acceleration
- outlier_ratio
- seller_growth
- sales_breadth
- winner_concentration
- revenue_density
- search_momentum
- content_momentum

LLM không tự tính thay backend nếu backend có thể tính.

---

## 11. AI intelligence engine

AI dùng cho:
- semantic classification,
- topic clustering,
- intent classification,
- pain/JTBD hypothesis,
- content angle extraction,
- explanation,
- synthesis.

AI không dùng để:
- bịa volume/GMV,
- sửa raw data,
- merge entity confidence thấp,
- tự duyệt workflow.

---

## 12. Evidence engine

Mọi claim quan trọng liên kết evidence.

Claim type:
- FACT
- INFERENCE
- HYPOTHESIS

Evidence types:
- metric
- snapshot
- keyword signal
- outlier
- user note
- provider record

---

## 13. Workflow engine

Workflow state nằm trong database, không nằm riêng trong memory của agent.

Transition chỉ hợp lệ nếu preconditions pass. Approval API chỉ được user hoặc policy engine gọi, không phải AI.

---

## 14. Stage packages

Mỗi stage tạo package immutable/versioned:

- MARKET_PACKAGE
- NICHE_PACKAGE
- CUSTOMER_PACKAGE
- DEMAND_PACKAGE
- PRODUCT_PACKAGE
- CONTENT_PACKAGE
- CONTENT_GAP_PACKAGE
- AFFILIATE_PACKAGE
- STRATEGY_PACKAGE

Stage sau chỉ đọc package đã approved.

---

## 15. Human-in-the-loop UI

Research Workspace gồm ba vùng logic:

### Evidence panel
Data, source, timestamp, source links.

### Analysis panel
Charts, metrics, AI observations.

### Decision panel
Pin, reject, note, research more, approve.

Mọi action có audit log.

---

## 16. Data quality pipeline

```text
COLLECT
↓
RAW STORED
↓
SCHEMA VALIDATION
↓
SEMANTIC VALIDATION
↓
ANOMALY CHECK
↓
NORMALIZE
↓
SNAPSHOT
↓
AVAILABLE FOR RESEARCH
```

Validation fail:
- record không vào score,
- raw vẫn giữ,
- có reason,
- có thể reparse/retry.

---

## 17. Fail-closed rules

Ví dụ cumulative sold giảm 80%:
- mark anomaly,
- exclude from growth,
- preserve evidence,
- không coi là negative sales.

Missing field không tự biến thành 0.

---

## 18. Entity resolution

Canonical entities:
- product
- brand
- shop
- creator
- keyword cluster
- customer segment

Matching sử dụng:
1. exact identifiers
2. brand/model rules
3. normalized text
4. attributes
5. model-assisted similarity

Confidence thấp → human review.

---

## 19. Security boundaries

- secrets trong secret manager/env,
- không lưu cookies/token plaintext,
- AI query layer read-only,
- writes qua application service,
- audit approval,
- ghi access/licensing mode cho từng source.

---

## 20. Observability

Connector metrics:
- last_success
- success_rate
- latency
- error_rate
- records_collected
- schema_drift
- freshness
- cost estimate

Workflow metrics:
- current stage
- pending gate
- blocked reason
- last run
- source health

---

## 21. Scaling path

### V1
Postgres + MinIO + Redis + single API + worker + Prefect + Docker Compose.

### V2
Separate collection workers, managed object storage, read replicas, queues, materialized aggregations.

### V3
Chỉ thêm ClickHouse/warehouse khi benchmark chứng minh Postgres không đủ.

---

## 22. Architecture Definition of Done

1. Thay connector không phải sửa analytics.
2. Raw data được giữ.
3. Snapshot có lineage.
4. AI chỉ đọc approved evidence package.
5. Workflow transition có preconditions.
6. User decision được audit.
7. Claim trace được evidence.
8. Bad data không âm thầm đi vào score.
9. Có thể replay parser trên raw.
10. Có test cho contracts quan trọng.
