# DATA CONTRACT
## Data Collection, Normalization, Quality & Evidence

**Version:** 0.1  
**Status:** Draft

---

## 1. Purpose

Data Contract quy định cách hệ thống:
- thu thập,
- lưu raw,
- parse,
- validate,
- normalize,
- snapshot,
- tính derived metrics,
- đánh dấu estimate,
- quản lý lineage,
- chuyển dữ liệu thành evidence.

Mục tiêu là ngăn data drift và AI sử dụng dữ liệu không rõ nguồn.

---

## 2. Source priority

Ưu tiên dữ liệu:
1. Official API
2. User-authorized first-party data
3. Licensed commercial provider
4. Public platform data
5. Public crawler nơi được phép
6. Derived estimate

Mỗi field phải có source metadata.

---

## 3. Universal source metadata

Mọi normalized record phải có:

```text
source_id
source_type
source_run_id
captured_at
parser_version
normalizer_version
raw_object_id
confidence
estimated
```

Optional:
- licensing notes
- freshness SLA

---

## 4. Raw data contract

Raw data:
- immutable,
- checksum protected,
- never modified by AI,
- retained để reparse.

Required metadata:

```text
raw_object_id
source_run_id
object_path
content_type
checksum
captured_at
request_fingerprint
```

---

## 5. Snapshot contract

Mọi object biến động theo thời gian phải snapshot.

Không update lịch sử in-place.

Snapshot key logic:

```text
(entity_id, observed_at, source_id)
```

Snapshot phải idempotent trong cùng request fingerprint.

---

## 6. Product snapshot contract

Minimum:

```text
listing_id
observed_at
list_price
current_price
estimated_effective_price
cumulative_sold
rating
review_count
stock_state
shop_id
source_id
confidence
anomaly_status
```

Unknown khác 0. Nếu không biết stock, dùng NULL/UNKNOWN.

---

## 7. Keyword snapshot contract

```text
keyword_id
platform
observed_at
search_index
rank
related_terms_count
source_id
metric_type
confidence
```

`metric_type` bắt buộc:
- ABSOLUTE_VOLUME
- NORMALIZED_INDEX
- RANK_PROXY
- TREND_PROXY
- UNKNOWN

Không hiển thị proxy như absolute volume.

---

## 8. Content snapshot contract

```text
content_id
observed_at
views
likes
comments
shares
saves
source_id
confidence
```

Unavailable metric = NULL.

---

## 9. Commission contract

```text
affiliate_product_id
observed_at
commission_rate
commission_fixed
currency
eligibility
source_id
confidence
```

Commission phải snapshot vì có thể thay đổi.

---

## 10. Canonical currency

Internal calculation currency: VND.

Nếu source khác currency:
- giữ original amount,
- lưu FX source,
- lưu normalized_vnd.

Không overwrite original.

---

## 11. Price semantics

Phân biệt:
- list_price
- current_price
- voucher_price
- flash_sale_price
- estimated_effective_price

Nếu không đủ dữ liệu voucher, `estimated_effective_price` có thể NULL.

GMV estimate phải ghi rõ price field sử dụng.

---

## 12. Sold semantics

`cumulative_sold` là tổng tích lũy nếu source cung cấp.

Derived:

```text
sold_delta = current_cumulative_sold - previous_cumulative_sold
```

Nếu delta âm:
- không mặc định negative sales,
- mark anomaly,
- exclude until resolved.

---

## 13. Derived metric contract

Mỗi metric derived phải có:

```text
metric_name
formula_version
input_refs
value
computed_at
confidence
```

Ví dụ `OUTLIER_RATIO_V1`.

Không thay formula âm thầm.

---

## 14. Estimated data contract

Mọi estimate phải có:

```text
estimated = true
estimation_method
assumptions
formula_version
confidence
```

Ví dụ estimated GMV:

```text
sold_delta * estimated_effective_price
```

Nếu effective price không đáng tin, confidence giảm.

---

## 15. Confidence model

Confidence là internal trust indicator, không mặc định là xác suất thống kê.

Components có thể gồm:
- source reliability
- freshness
- completeness
- cross-source agreement
- anomaly state
- sample coverage

Formula phải versioned.

---

## 16. Coverage model

Coverage đo phạm vi dữ liệu.

Ví dụ:
- % active listings captured
- % keyword cluster terms observed
- % candidate creators captured

Score cao nhưng coverage thấp phải cảnh báo.

---

## 17. Freshness model

Mỗi data type có SLA riêng, configurable.

Ví dụ:
- product price: 24h
- sold: 24h
- keyword: 7d
- YouTube views: 24h
- commission: 24h

Stale data không tự xóa; downstream confidence giảm.

---

## 18. Data quality rules

### Schema rules
- type correct
- required fields
- enum valid

### Semantic rules
- price >= 0
- rating range valid
- counts >= 0
- timestamp hợp lệ

### Temporal rules
- impossible jump detection
- cumulative reset detection

### Identity rules
- duplicate listing
- conflicting platform IDs

---

## 19. Anomaly severity

- INFO
- WARNING
- ERROR
- BLOCKING

BLOCKING record không đi vào score.

---

## 20. Schema drift policy

Nếu source field biến mất hoặc đổi type:
- connector health warning,
- parser fail closed,
- không silent coercion,
- raw retained,
- tạo schema drift incident.

Missing không biến thành 0.

---

## 21. Product identity contract

Canonical match fields:
- platform listing ID
- brand
- model
- normalized title
- attributes
- shop/seller info

Match result:

```text
canonical_product_id
match_method
confidence
review_required
```

Nếu review_required=true, merge chưa được coi là FACT.

---

## 22. Evidence contract

```json
{
  "id": "EVID-001",
  "type": "KEYWORD_SIGNAL",
  "entity_ref": "KWCLUSTER-12",
  "summary": "Cluster 'dễ vệ sinh' tăng 34% trong 90 ngày",
  "source_refs": ["SRC-001"],
  "captured_at": "...",
  "confidence": 0.83,
  "freshness_status": "FRESH"
}
```

Evidence phải mở được về nguồn hoặc record hỗ trợ.

---

## 23. Claim contract

```json
{
  "id": "CLAIM-001",
  "type": "INFERENCE",
  "text": "Nhu cầu ưu tiên tính dễ vệ sinh đang tăng.",
  "evidence_ids": ["EVID-001", "EVID-014", "EVID-028"],
  "confidence": 0.79
}
```

Không có evidence → không được type FACT.

---

## 24. Data access rules for AI

AI không truy cập raw DB tự do.

Luồng:

```text
Database
↓
Deterministic query
↓
Evidence Pack
↓
AI
```

Evidence pack phải có:
- ids
- values
- source metadata
- confidence
- freshness
- approved user notes

---

## 25. Import contract

User có thể import:
- Shopee Affiliate reports
- CSV
- XLSX

Pipeline:

```text
upload
↓
schema mapping
↓
preview
↓
user confirmation
↓
normalize
↓
store
```

Không auto-ingest file không xác định schema.

---

## 26. Data retention

V1 default recommendation:
- raw: 90+ days configurable
- snapshots: long-term
- audit: long-term
- AI prompts/outputs: versioned per project
- cache: short-lived

---

## 27. Privacy & secrets

Không lưu trong evidence:
- passwords
- auth tokens
- private cookies
- secrets

Secrets nằm trong secret manager/environment store.

---

## 28. Data Contract Definition of Done

1. Mọi normalized record trace về raw object.
2. Unknown không bị biến thành 0.
3. Estimate có flag và method.
4. Derived metric có formula version.
5. Snapshot không overwrite lịch sử.
6. Bad data có anomaly state.
7. AI chỉ nhận evidence pack.
8. Claim trace được evidence.
9. Confidence, coverage, freshness đi xuyên suốt.
10. Source drift không âm thầm phá analytics.
