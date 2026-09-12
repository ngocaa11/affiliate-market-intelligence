# PRODUCT VISION
## Shopee Affiliate Market Intelligence System

**Version:** 0.1  
**Status:** Draft for implementation  
**Primary owner:** Product / Business  
**Technical co-owner:** Engineering / Data  
**Last updated:** 2026-09-12

---

## 1. Product statement

Shopee Affiliate Market Intelligence System là một công cụ **bán tự động** giúp người làm Shopee Affiliate nghiên cứu thị trường từ rộng đến hẹp, nhìn thấy dữ liệu gốc, tự đánh giá và điều chỉnh hướng nghiên cứu trước khi AI phân tích tiếp.

Hệ thống không nhằm “tự động chọn sản phẩm hot” hoặc “để AI quyết định thay người dùng”.

Mục tiêu là tạo một quy trình nghiên cứu có kiểm soát:

> **Thị trường → Ngành → Ngách → Micro-niche → Khách hàng → Nhu cầu/Pain → Search Demand → Commerce Demand → Content Demand → Sản phẩm → Content Gap → Positioning → Chiến lược nội dung → Kế hoạch AFF**

Máy thu thập và tính toán.  
AI tổ chức, diễn giải và đề xuất giả thuyết.  
Người dùng kiểm tra, điều chỉnh và quyết định.

---

## 2. North Star

> **Phát hiện sớm khoảng thị trường còn có thể chiếm lĩnh, nơi nhu cầu khách hàng đang tăng, có sản phẩm Shopee phù hợp để kiếm tiền Affiliate và lượng nội dung cạnh tranh chưa phản ánh hết nhu cầu thực.**

Hệ thống phải giúp người dùng đi từ:

> “Tôi chưa biết nên làm ngách nào”

đến:

> “Tôi chọn nhóm khách hàng X, giải quyết vấn đề Y, bằng nhóm sản phẩm Z, ưu tiên sản phẩm A/B/C, với positioning P và content gap Q; đây là kế hoạch test nội dung và kinh tế Affiliate tương ứng.”

---

## 3. Product philosophy

### 3.1 Customer-first

Không bắt đầu từ “sản phẩm nào bán chạy nhất”.

Bắt đầu từ:
- Ai đang mua?
- Họ đang gặp vấn đề gì?
- Nhu cầu nào đang tăng?
- Họ đang tìm gì?
- Họ đang xem gì?
- Họ đang mua gì?
- Điều gì khiến họ do dự?
- Khoảng nội dung nào chưa được phục vụ tốt?

### 3.2 Data-first

Mọi phân tích phải dựa trên dữ liệu đã được thu thập, kiểm tra và chấp thuận. AI không được tự điền số thiếu.

### 3.3 Human-in-the-loop

Mỗi giai đoạn nghiên cứu quan trọng đều có điểm dừng để người dùng:
- xem dữ liệu,
- pin dữ liệu quan trọng,
- loại dữ liệu nhiễu,
- sửa cluster,
- thêm ghi chú,
- yêu cầu research thêm,
- phê duyệt trước khi đi tiếp.

### 3.4 Explainable by design

Mọi kết luận quan trọng phải trả lời được:
- dữ liệu từ đâu,
- dữ liệu lúc nào,
- phương pháp tính gì,
- độ tin cậy bao nhiêu,
- evidence nào hỗ trợ claim,
- đây là FACT, INFERENCE hay HYPOTHESIS.

---

## 4. Problem being solved

Người làm Affiliate thường gặp 7 vấn đề:
1. Chọn ngách dựa vào cảm tính hoặc trend ngắn hạn.
2. Chỉ nhìn sản phẩm bán chạy mà không hiểu khách hàng.
3. Chỉ nhìn search volume hoặc view mà không kiểm chứng bằng sales.
4. Không phân biệt trend thật với hype do một creator/sản phẩm/event.
5. Khó ghép dữ liệu từ Shopee, Google, YouTube, TikTok và nguồn bên thứ ba.
6. Không biết content gap thực sự nằm ở đâu.
7. Dùng AI theo kiểu “hãy phân tích ngách này”, dẫn đến kết luận thiếu bằng chứng hoặc quá tự tin.

Sản phẩm này giải quyết các vấn đề trên bằng workflow nghiên cứu có cấu trúc và kiểm soát.

---

## 5. Core research hierarchy

### Level 1 — Market Radar
Quét rộng, nhẹ, không đào sâu mọi SKU.

Output:
- ngành tăng trưởng,
- ngành suy giảm,
- search momentum,
- sales momentum,
- content momentum,
- seller/SKU growth,
- freshness/confidence.

### Level 2 — Category Opportunity
Chọn ngành/subcategory đáng đi sâu.

### Level 3 — Niche / Micro-niche Finder
Phân rã ngành thành ngách và micro-niche có thể phục vụ bằng content + Affiliate.

### Level 4 — Customer Intelligence
Xác định:
- segment,
- JTBD,
- pain,
- desire,
- anxiety,
- trigger,
- buying criteria,
- usage context.

### Level 5 — Search / Demand Intelligence
Hiểu người dùng đang quan tâm tăng hay giảm.

### Level 6 — Commerce Intelligence
Xác nhận nhu cầu thực bằng dữ liệu sản phẩm, shop, giá, sold, review, rating, phân khúc giá và các chỉ số thị trường.

### Level 7 — Content Intelligence
Hiểu người dùng đang xem gì, creator nào đang thắng, video nào là outlier và topic nào đang tăng.

### Level 8 — Opportunity Synthesis
Xác định:
- market opportunity,
- customer opportunity,
- product opportunity,
- content opportunity.

### Level 9 — Strategy Builder
Tạo positioning, content pillars, funnel, product portfolio và test plan.

---

## 6. Supported entry modes

### Discovery Mode
Người dùng chưa biết nên làm ngách nào. Hệ thống bắt đầu từ Market Radar.

### Deep Research Mode
Người dùng nhập seed như “máy làm sữa hạt”, “máy massage chân”.

### Customer-first Mode
Người dùng nhập nhóm khách hàng hoặc pain, hệ thống suy ra need clusters → product categories → content opportunities.

### Keyword-first Mode
Người dùng nhập keyword và hệ thống mở rộng ra keyword → intent → need cluster → customer → product → content. Keyword-first không được phép bỏ qua customer validation.

---

## 7. Three signal model

Mọi cơ hội phải được đánh giá từ tối thiểu ba tín hiệu:

### SEARCH
Người dùng đang tìm gì?

### CONTENT
Người dùng đang xem gì?

### COMMERCE
Người dùng đang mua gì?

Tín hiệu mạnh nhất là khi cả ba cùng xác nhận một hướng:

> Search ↑ + Content ↑ + Sales ↑

Hệ thống phải phân biệt:
- Search ↑, Content ↑, Sales → : early interest / hype risk.
- Search ↑, Sales ↑, Content thấp: content gap tốt.
- Sales ↑, Search thấp: mature/commercial demand.
- Search ↓, Content ↓, Sales ↓: declining.

---

## 8. Main product modules

1. Market Radar
2. Category Explorer
3. Niche Finder
4. Customer Intelligence
5. Search Interest Engine
6. Keyword & Intent Engine
7. Commerce Intelligence
8. Product Radar
9. Content Intelligence
10. Outlier Engine
11. Competition Engine
12. Trend Engine
13. Content Gap Engine
14. Product × Content Matching
15. Affiliate Economics
16. Opportunity Scoring
17. Strategy Builder
18. Research Workspace
19. Human Approval Gates
20. Evidence & Audit System

---

## 9. Research Workspace

Research Workspace là trung tâm UX của hệ thống.

Mỗi stage phải hiển thị:
- dữ liệu gốc hoặc normalized data,
- nguồn,
- timestamp,
- confidence,
- freshness,
- biểu đồ,
- bảng,
- sample evidence,
- AI observation,
- user notes.

Người dùng có thể:
- **PIN**
- **REJECT**
- **EDIT**
- **ADD NOTE**
- **COMPARE**
- **RESEARCH MORE**
- **APPROVE**
- **GO BACK**

AI không được tự chuyển stage khi stage yêu cầu approval.

---

## 10. Required final outputs

Một project hoàn chỉnh phải có tối thiểu:

### Market conclusion
- trạng thái thị trường,
- structural growth / breakout / mature / hype / declining,
- confidence.

### Beachhead customer
- segment ưu tiên,
- JTBD,
- pain,
- trigger,
- buying criteria.

### Niche / micro-niche
- ngách ưu tiên,
- lý do,
- rủi ro.

### Search opportunity
- keyword clusters,
- buyer intent,
- trend.

### Product opportunity
- product categories,
- candidate products,
- price bands,
- competition,
- affiliate fit.

### Content opportunity
- content gaps,
- outlier patterns,
- topics,
- angles,
- positioning gap.

### Affiliate economics
- low / base / high scenario,
- assumptions.

### Strategy
- positioning,
- pillars,
- traffic/trust/bridge/money content,
- 30-day test plan.

---

## 11. Non-goals

V1 không nhằm:
- crawl toàn bộ Shopee real-time,
- tự động đặt đơn,
- tự động đăng nội dung,
- tự động chi tiền quảng cáo,
- tự quyết định đầu tư,
- bypass CAPTCHA/anti-bot,
- lấy dữ liệu private không được phép,
- thay thế judgment của người dùng.

---

## 12. Success criteria

1. Người dùng đi từ broad market đến strategy trong một project.
2. Mỗi stage có dữ liệu đọc được và decision gate rõ ràng.
3. Mọi claim của AI trace được về evidence.
4. Người dùng sửa hướng research mà không phá project.
5. Hệ thống phân biệt FACT / INFERENCE / HYPOTHESIS.
6. Tool không phụ thuộc một nguồn duy nhất.
7. Một connector hỏng không làm toàn hệ thống hỏng.
8. Score hiển thị cùng confidence, coverage và freshness.
9. Output cuối chuyển thành kế hoạch Affiliate thực thi được.

---

## 13. Long-term vision

Phiên bản cuối hướng đến một “AI Affiliate Research Director” bán tự động.

**Machine collects.  
Machine calculates.  
AI organizes & interprets.  
Human judges.  
System executes the next approved research step.**
