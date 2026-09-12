# WORKFLOW
## Research Workflow & Human Approval Gates

**Version:** 0.1  
**Status:** Draft

---

## 1. Workflow principle

Hệ thống là **bán tự động**.

Không có luồng:
> User nhập seed → AI tự chạy toàn bộ → trả chiến lược.

Luồng đúng:
> Collect → Show Evidence → Human Review → Approved Package → AI Analysis → Human Review → Next Stage.

---

## 2. Global state model

```text
DRAFT
↓
SCOPED
↓
COLLECTING
↓
DATA_VALIDATION
↓
DATA_REVIEW
↓
DATA_APPROVED
↓
ANALYZING
↓
ANALYSIS_REVIEW
↓
STAGE_APPROVED
↓
NEXT_STAGE
```

Terminal:
- COMPLETED
- CANCELLED
- BLOCKED

---

## 3. Transition authority

### Machine may automatically
- DRAFT → SCOPED sau khi scope hợp lệ
- SCOPED → COLLECTING
- COLLECTING → DATA_VALIDATION
- DATA_VALIDATION → DATA_REVIEW nếu quality threshold pass
- DATA_APPROVED → ANALYZING
- ANALYZING → ANALYSIS_REVIEW

### Human approval required
- DATA_REVIEW → DATA_APPROVED
- ANALYSIS_REVIEW → STAGE_APPROVED
- STAGE_APPROVED → NEXT_STAGE nếu stage gated

AI không được gọi approval transition trực tiếp.

---

## 4. Research modes

### Discovery Mode
Start: MARKET

### Deep Research Mode
Start: CATEGORY/NICHE dựa trên seed

### Customer-first Mode
Start: CUSTOMER

### Keyword-first Mode
Start: SEARCH_DEMAND

Mọi mode cuối cùng hội tụ về canonical stages.

---

## 5. Canonical stages

### Stage 0 — Scope
Input:
- mode
- market
- locale
- time window
- platforms
- seed/customer/category nếu có

Output: `SCOPE_PACKAGE`

Human Gate: Yes

### Stage 1 — Market Radar
Goal: tìm ngành/category đáng đi sâu.

Collect:
- category-level commerce
- broad search signals
- broad content signals

Output: `MARKET_PACKAGE`

Human actions:
- select categories
- reject noisy categories
- add note
- request more data

### Stage 2 — Category / Niche Discovery
Goal: phân rã category thành niches/micro-niches.

Output: `NICHE_PACKAGE`

Must contain:
- selected niches
- evidence
- metrics
- confidence
- exclusions

### Stage 3 — Customer Intelligence
Goal: xác định customer segments và need structure.

AI may propose:
- segment
- JTBD
- pain
- desire
- anxiety
- trigger
- buying criteria

User có thể:
- rename
- merge
- split
- reject
- add manual segment

Output: `CUSTOMER_PACKAGE`

### Stage 4 — Search Demand
Goal: kiểm chứng customer needs bằng search data.

Collect:
- keywords
- related terms
- cross-platform signals
- trends
- intent

Output: `DEMAND_PACKAGE`

Contains:
- approved keyword clusters
- search signals
- buyer intent
- search confidence

### Stage 5 — Product / Commerce
Goal: tìm product categories và candidate products.

Output: `PRODUCT_PACKAGE`

Contains:
- product categories
- candidate products
- price bands
- sales momentum
- competition
- data confidence

### Stage 6 — Content Intelligence
Goal: tìm content demand, creator patterns và outliers.

Output: `CONTENT_PACKAGE`

### Stage 7 — Content Gap
Goal: ghép Customer + Search + Commerce + Content.

Output: `CONTENT_GAP_PACKAGE`

Contains:
- gap hypotheses
- supporting evidence
- content supply
- demand signals
- positioning candidates

### Stage 8 — Affiliate Economics
Goal: mô phỏng economics.

Output: `AFFILIATE_PACKAGE`

Must use actual/imported commission khi có.

Scenarios:
- LOW
- BASE
- HIGH

### Stage 9 — Strategy
Goal: tạo chiến lược final.

Output: `STRATEGY_PACKAGE`

Contains:
- beachhead customer
- entry problem
- positioning
- product portfolio
- keyword clusters
- content pillars
- traffic/trust/bridge/money plan
- test plan
- risks
- unresolved hypotheses

---

## 6. Human gate actions

### APPROVE
Đóng version hiện tại và cho phép stage sau.

### REJECT
Không cho stage sau chạy.

### EDIT
User sửa selection/cluster/notes.

### RESEARCH_MORE
Tạo sub-scope mới và quay lại collection.

### GO_BACK
Quay về stage trước, không xóa version cũ.

---

## 7. Research More loop

```text
ANALYSIS_REVIEW
↓
User: RESEARCH_MORE
↓
Create child ResearchScope
↓
COLLECTING
↓
DATA_REVIEW
↓
ANALYSIS_REVIEW
↓
User: APPROVE
```

Không overwrite scope cũ.

---

## 8. Approved dataset rule

Stage sau chỉ được đọc:
- approved records,
- pinned evidence,
- user notes,
- approved hypotheses,
- deterministic metrics thuộc stage package.

Rejected records không được AI stage sau tự lấy lại.

---

## 9. Versioning rule

Mỗi lần user thay đổi selection quan trọng, package version tăng.

Ví dụ:
CUSTOMER_PACKAGE_V1 → user split segment → CUSTOMER_PACKAGE_V2

V1 vẫn tồn tại để audit.

---

## 10. Blocking conditions

Stage BLOCKED nếu:
- source health quá thấp,
- data quality fail,
- required field thiếu,
- coverage dưới threshold,
- connector lỗi và không có fallback,
- dependency chưa approved.

UI phải hiển thị lý do block.

---

## 11. Confidence gates

Threshold chỉ là configurable heuristic, ví dụ:
- >= 0.75: normal
- 0.5–0.75: warning
- < 0.5: require user confirmation
- < 0.3: không eligible cho automatic recommendation

Formula/threshold phải versioned.

---

## 12. Workflow audit log

Mọi action lưu:
- actor
- action
- timestamp
- project
- stage
- old_state
- new_state
- reason
- object refs

AI action có actor type = AI.

---

## 13. Stage package minimum schema

```json
{
  "project_id": "...",
  "stage": "CUSTOMER",
  "version": 2,
  "parent_package_id": "...",
  "status": "APPROVED",
  "selected_entities": [],
  "metrics": {},
  "evidence_ids": [],
  "user_note_ids": [],
  "claims": [],
  "confidence": 0.82,
  "coverage": 0.76,
  "freshness": {},
  "approved_by": "...",
  "approved_at": "..."
}
```

---

## 14. Example workflow

User starts: “Máy làm sữa hạt”.

### Scope
Vietnam / Shopee / 90 days / YouTube + Google + TikTok nếu có.

### Niche
AI proposes:
- gia đình nhỏ
- dễ vệ sinh
- ít ồn
- dưới 2 triệu

User rejects “ít ồn”; approves “dễ vệ sinh” và “gia đình nhỏ”.

### Customer
AI proposes “Phụ nữ 28–45 chăm sóc bữa ăn gia đình”.

User edits thành “Người chăm sóc bữa ăn gia đình 25–45, không giới hạn giới tính”.

### Search
Tool thấy cluster “dễ vệ sinh / tự vệ sinh / ít bám cặn” tăng.

### Product
Tool surfaces candidate products; user loại sản phẩm bảo hành yếu.

### Content
Outlier cho thấy topic “vệ sinh máy” có demand nhưng supply chưa cao.

### Strategy
Positioning: “Healthy kitchen đơn giản, thực dụng, ít tốn công cho gia đình bận.”

---

## 15. Workflow Definition of Done

1. Không bypass required gate bằng UI/API.
2. Stage sau không đọc rejected evidence.
3. Research More tạo scope/version mới.
4. Go Back không mất lịch sử.
5. Mọi package có version.
6. Mọi transition có audit log.
7. AI crash không làm mất workflow state.
8. Connector retry không tạo duplicate package.
