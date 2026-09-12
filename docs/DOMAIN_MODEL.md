# DOMAIN MODEL
## Shopee Affiliate Market Intelligence System

**Version:** 0.1  
**Status:** Draft domain model

---

## 1. Purpose

Tài liệu này định nghĩa ngôn ngữ nghiệp vụ dùng xuyên suốt codebase để Product, Data, Backend, Frontend và AI dùng cùng terminology.

Hệ thống chia thành 10 domain:
1. Research
2. Source & Data Lineage
3. Market
4. Customer
5. Search
6. Commerce
7. Content
8. Affiliate
9. Intelligence
10. Strategy

---

# 2. Research domain

## ResearchProject
Đại diện một phiên nghiên cứu có mục tiêu rõ.

Fields chính:
- id
- name
- mode
- objective
- market
- locale
- time_horizon
- status
- created_by
- created_at
- updated_at

Mode:
- DISCOVERY
- DEEP_RESEARCH
- CUSTOMER_FIRST
- KEYWORD_FIRST

## ResearchScope
Phạm vi hiện tại:
- category_ids
- seed_keywords
- customer hypotheses
- platforms
- date window
- geography
- max results

Scope phải versioned.

## ResearchStage
Các stage chuẩn:
- SCOPE
- MARKET
- CATEGORY
- NICHE
- CUSTOMER
- SEARCH_DEMAND
- PRODUCT
- CONTENT
- CONTENT_GAP
- AFF_ECONOMICS
- STRATEGY

## ResearchDecision
Types:
- APPROVE
- REJECT
- EDIT
- RESEARCH_MORE
- GO_BACK

## StagePackage
Output versioned của một stage đã approved.

Fields:
- id
- project_id
- stage
- version
- parent_package_id
- payload
- evidence_ids
- user_note_ids
- confidence
- approved_by
- approved_at

---

# 3. Source & lineage domain

## DataSource
Examples:
- SHOPEE_PUBLIC
- SHOPEE_AFFILIATE_IMPORT
- YOUTUBE_API
- GOOGLE_TRENDS
- TIKTOK
- METRIC
- YOUNET

Fields:
- id
- name
- source_type
- legal_access_mode
- update_frequency
- reliability_tier
- enabled

## SourceRun
Một lần thu thập.

Fields:
- id
- data_source_id
- connector_version
- started_at
- finished_at
- status
- request_scope
- records_raw
- records_valid
- records_rejected
- error_summary

## RawObject
Tham chiếu payload gốc.

Fields:
- id
- source_run_id
- object_path
- checksum
- mime_type
- captured_at

## DataQualityResult
- record_type
- record_id
- rule
- severity
- status
- observed_value
- message

---

# 4. Market domain

## Category
Cây ngành hàng chuẩn hóa.

Fields:
- id
- parent_id
- canonical_name
- platform_category_refs
- level

## Niche
Một vùng nhu cầu/market hẹp hơn category. Không bắt buộc trùng category platform.

## MicroNiche
Một phân đoạn đủ cụ thể để phục vụ bằng content + product.

Ví dụ:
“Máy làm sữa hạt dễ vệ sinh cho gia đình nhỏ.”

## MarketSnapshot
Metrics có thể gồm:
- estimated_gmv
- units_sold
- active_products
- active_sellers
- median_price
- seller_growth
- product_growth
- concentration
- confidence

---

# 5. Customer domain

## CustomerSegment
Một nhóm khách hàng có nhu cầu/hành vi đủ khác biệt.

Fields:
- id
- name
- description
- demographic_notes
- behavioral_notes
- evidence_ids
- confidence

## JTBD
- customer_segment_id
- job_statement
- context
- desired_outcome
- evidence_ids

## CustomerProblem
- id
- segment_id
- name
- description
- urgency
- frequency
- evidence_ids

## Desire
Kết quả khách hàng muốn đạt.

## Anxiety
Điều khiến khách hàng do dự.

## BuyingTrigger
Tác nhân kích hoạt research hoặc mua hàng.

## BuyingCriterion
Tiêu chí quyết định như giá, bảo hành, dễ dùng, hiệu quả, thương hiệu, dung tích, độ ồn.

---

# 6. Search domain

## Keyword
Canonical keyword.

Fields:
- id
- text
- locale
- normalized_text

## KeywordPlatformRef
Representation của keyword trên từng platform.

## KeywordSnapshot
- keyword_id
- platform
- observed_at
- search_index
- rank
- related_terms_count
- source
- confidence

`search_index` có thể là normalized/proxy metric, không mặc định absolute volume.

## KeywordCluster
Nhóm keyword cùng nhu cầu.

Ví dụ cluster “máy dễ vệ sinh” gồm:
- máy sữa hạt dễ rửa
- máy tự vệ sinh
- máy không bám cặn

## SearchIntent
Enum:
- INFORMATIONAL
- PROBLEM
- SOLUTION
- COMMERCIAL
- COMPARISON
- TRANSACTIONAL

## SearchSignal
Derived metrics:
- growth_7d
- growth_30d
- growth_90d
- velocity
- acceleration
- breadth
- cross_platform_confirmation
- buyer_intent_score

---

# 7. Commerce domain

## Brand
Canonical brand.

## Shop
- platform
- platform_shop_id
- canonical_name
- mall_status
- rating
- follower_count
- source

## Product
Canonical product.

Fields:
- id
- brand_id
- canonical_name
- model
- category_id
- product_type
- attributes
- identity_confidence

## ProductListing
Một listing cụ thể trên platform/shop.

Fields:
- platform
- platform_product_id
- shop_id
- product_id
- title
- url
- status

Một Product có thể có nhiều ProductListing.

## ProductVariant
Variant thuộc listing.

## ProductSnapshot
- listing_id
- observed_at
- list_price
- current_price
- estimated_effective_price
- cumulative_sold
- rating
- review_count
- stock_state
- source
- confidence
- anomaly_status

## CommerceSignal
Derived:
- sold_delta
- sales_velocity
- growth
- price_trend
- review_velocity
- sales_breadth
- winner_concentration
- revenue_density

---

# 8. Content domain

## Creator
- platform
- platform_creator_id
- name
- follower_count
- category_tags

## ContentItem
- id
- platform
- platform_content_id
- creator_id
- title
- text
- published_at
- url

## ContentSnapshot
- observed_at
- views
- likes
- comments
- shares
- saves nếu có

## ContentTopic
Semantic topic.

## ContentAngle
Ví dụ:
- cảnh báo
- so sánh
- review
- lỗi thường gặp
- before/after
- myth-busting
- gift angle

## Outlier
- content_id
- baseline_method
- baseline_value
- observed_value
- outlier_ratio
- confidence

## ContentSignal
- content_growth
- view_velocity
- creator_growth
- outlier_count
- topic_breadth
- content_supply

---

# 9. Affiliate domain

## AffiliateProduct
Liên kết ProductListing với điều kiện Affiliate.

## CommissionSnapshot
- affiliate_product_id
- observed_at
- commission_rate
- commission_fixed
- eligibility_notes
- source

## AffiliatePerformance
Dữ liệu user import/authorize:
- impressions
- clicks
- orders
- approved_orders
- cancelled_orders
- commission
- conversion_rate

## RevenueScenario
LOW / BASE / HIGH.

Fields:
- assumptions
- projected_clicks
- projected_orders
- projected_commission
- confidence

---

# 10. Intelligence domain

## Evidence
Types:
- METRIC
- PRODUCT
- KEYWORD
- CONTENT
- USER_NOTE
- SOURCE_RECORD
- CHART
- EXTERNAL_PROVIDER

Fields:
- id
- project_id
- evidence_type
- entity_ref
- summary
- source_ref
- captured_at
- confidence
- freshness

## Claim
ClaimType:
- FACT
- INFERENCE
- HYPOTHESIS

Fields:
- id
- text
- claim_type
- evidence_ids
- confidence
- model_version
- prompt_version

## Hypothesis
Status:
- OPEN
- ACCEPTED
- REJECTED
- NEED_MORE_RESEARCH

## OpportunityScore
Là ranking heuristic, không phải probability.

Fields:
- object_type
- object_id
- score
- components
- confidence
- coverage
- formula_version

---

# 11. Strategy domain

## Positioning
- target_customer
- entry_problem
- promise
- differentiation
- evidence_ids

## ContentPillar
Trụ cột nội dung.

## ContentIdea
- pillar
- funnel_stage
- topic
- keyword_cluster
- target_problem
- mapped_products
- priority

FunnelStage:
- TRAFFIC
- TRUST
- BRIDGE
- MONEY

## StrategyPlan
- positioning
- customer_package
- product_package
- content_gap_package
- affiliate_scenarios
- test_plan
- version

---

# 12. Canonical relationships

```text
ResearchProject
 ├── ResearchStage
 ├── StagePackage
 ├── Evidence
 └── ResearchDecision

Category
 └── Niche
      └── MicroNiche

CustomerSegment
 ├── JTBD
 ├── CustomerProblem
 ├── Desire
 ├── Anxiety
 └── BuyingTrigger

KeywordCluster
 └── Keyword
      └── KeywordSnapshot

Product
 └── ProductListing
      ├── ProductVariant
      ├── ProductSnapshot
      └── CommissionSnapshot

Creator
 └── ContentItem
      └── ContentSnapshot

Evidence
 └── Claim
      └── Hypothesis

Approved Stage Packages
 └── StrategyPlan
```

---

# 13. Semantic rules

1. `Product` khác `ProductListing`.
2. `Category` khác `Niche`.
3. `Keyword` khác `KeywordCluster`.
4. `SearchIndex` không mặc định absolute volume.
5. `EstimatedGMV` phải gắn estimated flag.
6. `Claim` không phải raw data.
7. `OpportunityScore` không phải forecast.
8. Forecast phải có assumptions.
9. AI analysis không được trở thành source.
10. User note có thể là evidence nhưng phải ghi rõ USER_NOTE.

---

# 14. Domain Definition of Done

- Một object có một tên chuẩn duy nhất.
- Database schema map được về các entity này.
- API payload dùng cùng terminology.
- Prompt AI dùng cùng terminology.
- UI label không mâu thuẫn backend.
- Mọi stage output biểu diễn được bằng domain entities đã định nghĩa.
