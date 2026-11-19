# CHUAN_BI — Giai đoạn 2: chuẩn bị mốc mới (chưa chạy reader trên test hay XQuAD-vi)

Ngày: 2026-11-08. Reader trên **test ViQuAD** và **XQuAD-vi**: chưa chạy lần nào. Reader chỉ chạy trên tập **select**
(chọn biến thể prompt tóm tắt; kiểm khói 40 câu cho bge-m3 và Sum+E). Mọi đầu ra mới nằm trong `data/icisn/`,
`results/icisn/`, `docs/icisn/`; `results/paper/` không bị ghi.

## 2.1 Tóm tắt không theo câu hỏi (Sum)

- Người viết: DeepSeek-V4.1-Flash, nhiệt độ 0, tắt thinking, **một lời gọi cho mỗi tài liệu**, prompt không có câu hỏi.
  Đầu vào là văn bản gốc (đoạn hoặc cả bài); độ dài mục tiêu theo từng tài liệu: ~1,3 × k(4) token của reader, quy ra số "từ"
  (âm tiết) theo tỉ lệ token/âm tiết của chính tài liệu. Tóm tắt **không** bị cắt khi sinh; khi đọc, `Summary` cắt ở token thứ
  k(r) của reader Qwen3.5-2B (k(r) = Σ⌈nᵢ/r⌉, cùng khối 512 token như mọi mốc khác; `vilatent/baselines.py`).
  Một tóm tắt viết ở mục tiêu 4× được cắt đầu cho 8× và 16× (người dùng đồng ý 2026-11-07).
- Ba biến thể prompt (`docs/icisn/summary_prompts.json`, SHA-256 trong `data/icisn/SHA256SUMS.txt`): v1 "giữ tên riêng, số liệu,
  sự kiện chính", v2 "dày thông tin, ưu tiên thực thể/số liệu/quan hệ", v3 "theo thứ tự nội dung, mỗi ý một câu".
- **Một thăm dò trước khi chọn (chỉ trên `viquad_long_select`, 6 bài, không dùng test):** bản đầu của prompt chỉ nói "khoảng N từ"
  và DeepSeek viết dài gấp 1,5–3,4 lần mục tiêu (có bài gần bằng văn bản gốc). Tôi thêm cụm "GIỚI HẠN CỨNG: tối đa N từ … bằng
  khoảng p% văn bản gốc" vào cả ba biến thể và nâng biên độ 1,15 → 1,3; kết quả thăm dò bị xóa, không lưu số F1.
- **Chọn biến thể chỉ trên select** (Sum ở 4×, ViQuAD select: 621 câu đoạn đơn + 621 câu Long, 1080 Ti, fp16):

| Biến thể | F1 đoạn đơn | F1 Long | F1 trung bình |
|---|---|---|---|
| v1 | 32,90 | 26,58 | **29,74** |
| v2 | 33,54 | 25,69 | 29,62 |
| v3 | 32,07 | 25,93 | 29,00 |

  Quy tắc chọn (đặt trước khi chạy): F1 trung bình cao nhất của hai thiết lập; hòa thì biến thể số nhỏ hơn. **Chọn v1.**
  Lý do trung thực: chênh lệch ≤ 0,7 F1 trên 621 câu từ 6 bài, không kiểm định; chọn v1 theo quy tắc, **không** phải vì v1 rõ ràng
  hơn. Theo EM thì v2 thắng ở đoạn đơn (14,3) và v3 thắng ở Long (11,3): lựa chọn không bền theo độ đo. Số liệu: `results/icisn/select/sum_choice.json`.
- Tóm tắt cuối (v1) đã sinh cho: ViQuAD test (557 đoạn đơn + 19 bài Long) và XQuAD-vi (240 đoạn + 48 bài):
  `data/icisn/summaries/final_viquad_test_v1.json`, `final_xquad_v1.json`. **Khóa:** SHA-256 các file này, của prompt và của
  quyết định chọn ghi trong `data/icisn/SHA256SUMS.txt`; không đổi sau giai đoạn này.
- Mức lấp đầy ngân sách của tóm tắt (token tóm tắt so với k(r); `results/icisn/summary_coverage.json`):

| Tập | Số tài liệu | Token tài liệu (trung bình) | Token tóm tắt (trung bình) | Tóm tắt ngắn hơn k(4) | Mức lấp đầy k(4) / k(8) / k(16) |
|---|---|---|---|---|---|
| ViQuAD test, đoạn đơn | 557 | 210 | 89 | 0,4% | 1,00 / 1,00 / 1,00 |
| ViQuAD test, Long | 19 | 6 191 | 1 437 | **36,8%** | **0,82** / 0,94 / 0,96 |
| XQuAD-vi, đoạn đơn | 240 | 213 | 89 | 1,3% | 1,00 / 1,00 / 1,00 |
| XQuAD-vi, Long | 48 | 1 068 | 545 | 2,1% | 1,00 / 1,00 / 1,00 |

  **Điểm yếu của Sum ở ViQuAD-Long 4×:** 7/19 bài có tóm tắt ngắn hơn ngân sách (trung bình dùng 82% ngân sách), nên Sum ở đó bị
  thiệt so với M. Khi phân tích H-S1/H-S2 phải nêu hạn chế này và báo thêm tỉ lệ dùng ngân sách. 3/576 tóm tắt chạm giới hạn đầu ra 6 000 token.

## 2.2 Hai điều kiện mới dựa trên Sum (cài đặt và kiểm thử)

- `Summary` (tên điều kiện `sum_<tag>`): toàn bộ ngân sách k(r) dành cho tóm tắt (đối ứng với M).
- `SummaryPlusE` (`sumE_<tag>_f<f>`): f = 2 như ME. k(r·f) token đầu của tóm tắt **thay vào đúng phần ngân sách của memory**, rồi
  các câu BM25 y hệt ME (cùng bộ chọn, `configs/bm25.json`, ngân sách k(r) − k(r·f)); tổng ≤ k(r) (kiểm bằng đếm token sau khi nối;
  nếu nối làm vượt thì bớt dần ngân sách BM25). Khác ME ở chỗ đây là **văn bản** đưa vào cửa sổ, không phải memory mềm.
- Mã: `vilatent/baselines.py` (lớp `Summary`, `SummaryPlusE`), `scripts/evaluate.py` (cú pháp `--methods sum:<tag>:<file.json>`,
  `sumE:<tag>:<file.json>,f=2`), `tests/test_icisn.py` (2 test: cắt đúng ngân sách; Sum+E ≤ ngân sách và chứa đoạn BM25 có đáp án).
  Kiểm khói trên 40 câu select: Sum+E dùng trung bình 50,1 token, trong ngân sách 4×.

## 2.3 Mốc bge-m3 chọn câu cùng ngân sách

- `BAAI/bge-m3`, bản `5617a9f61b028005a4858fdac845db406aefb181` (tải ngày 2026-11-08 trên gpu1080), embedding dense (vector CLS chuẩn hóa),
  fp16, tối đa 512 token; điểm = cosine(câu hỏi, câu). Tách câu và đóng gói **y hệt PhoBERT** (`pack_sentences`, không áp luật
  "điểm > 0" như BM25). Mốc so sánh duy nhất, không quảng bá thành phương pháp. Kiểm khói 40 câu select: F1 36,4 (BM25 36,0 trên cùng 40 câu).

## 2.4 Dữ liệu XQuAD-vi

- Nguồn: `github.com/google-deepmind/xquad`, `xquad.vi.json`, CC BY-SA 4.0 (xem `G0_KIEM_KE.md` §0.4). 48 bài, 240 đoạn, 1190 câu; không câu nào bị loại
  (đáp án đều nằm nguyên văn trong đoạn sau NFC).
- `data/icisn/xquad_vi_single.jsonl` (đoạn đơn) và `xquad_vi_long.jsonl` (ghép theo bài, dựng bằng cùng `vilatent.data.long_rows` như ViQuAD-Long:
  các đoạn của bài theo thứ tự file, nối bằng dòng trống). SHA-256: `b01e230e…6f5d` và `fb1a2c4d…fa8d`; sidecar `.meta.json`.
- **Khác biệt quan trọng so với ViQuAD-Long:** bài XQuAD chỉ ~5 đoạn, dài trung vị **1 015 token** (khoảng 581–2 552), trong khi bài
  ViQuAD-Long test trung bình 6 191 token (câu hỏi có trọng số: ~9 700). XQuAD-vi-Long vì thế là phép thử "đa đoạn ngắn", **không** thay được ViQuAD-Long cho kết luận về văn bản rất dài.
- Chồng lấn corpus stage 1: 6/240 đoạn trùng ≥ 50% 8-gram (xem G0). Đề xuất phân tích độ nhạy loại 6 đoạn này (người dùng đồng ý 2026-11-07); danh sách đoạn
  và quy tắc loại sẽ ghi vào PREREG_CONFIRM trước khi chạy reader.

## 2.5 Prompt học được ở f tốt nhất của chính nó

- Prompt chỉ khác ME ở nội dung memory; trong bài chính nó đọc ở f = 2 (f* của ME). Chọn f tốt nhất của prompt **trên select, đoạn đơn**,
  bằng các lượt đọc có sẵn trong `results/paper/select/single` (không chạy lại gì, không huấn luyện lại; `scripts/choose_f.py:best_factor`;
  quy tắc: f ≥ 2 có F1 select cao nhất, hòa thì f nhỏ hơn):

| r | F1 select của prompt theo f | f tốt nhất của prompt | f* của ME |
|---|---|---|---|
| 4 | f=2: 40,8; f=4: 47,7; **f=8: 51,3** | **8** | 2 |
| 8 | f=2: 29,8; **f=4: 35,2** | **4** | 2 |
| 16 | **f=2: 23,6** | 2 | 2 |

  Quyết định này áp cho cả hai thiết lập (đoạn đơn và Long) và cả XQuAD-vi. Ở select Long, f = 2 là tốt nhất ở mọi r (61,8; 62,0; 59,1), nên f tốt nhất của đoạn đơn
  có thể **không** tối ưu cho Long; đó là hệ quả của quy tắc "chọn trên đoạn đơn" đã nêu.
- **Ý nghĩa:** ở đoạn đơn, prompt ở f = 8 (4×) đạt 51,3 so với ME f = 2 đạt 55,9 trên select (khoảng cách thu hẹp từ ~15 xuống ~5 F1). So sánh
  ME − prompt ở bài chính (f = 2, +23,2 F1 ở đoạn đơn 4× trên test) vì vậy **thổi phồng** lợi thế của memory do prompt bị đặt ở f không tối ưu; cần báo cả hai.
- Lượt đọc test cần chạy mới (Giai đoạn 4): `prompt_bm25_f8_r4`, `prompt_bm25_f4_r8` (r = 16 dùng f = 2 đã có) trên ViQuAD đoạn đơn; trên XQuAD-vi: cả f = 2 và f tốt nhất ở cả hai thiết lập.

## Đã dùng ở Giai đoạn 2

- GPU 1080 Ti (GPU1, dùng chung): ~36 phút chạy Sum 3 biến thể × 2 tập select + vài phút kiểm khói bge-m3/Sum+E. Long select tốn ~10,5 phút/biến thể/621 câu (~1 s/câu).
- API (DeepSeek-V4.1-Flash): ~1 280 lời gọi tóm tắt (393 select, 576 test ViQuAD, 288 XQuAD-vi, 12 thăm dò) ≈ 1,2 triệu token vào, 0,3 triệu token ra; 0 lời gọi chấm.
- Phát hiện: DeepSeek 150 lời gọi/phút, Qwen3.8-27B 100 lời gọi/phút (ảnh hưởng ước lượng giờ ở Giai đoạn 4: chấm ~80 000 dự đoán mới tốn ≥ 9 giờ API).

## Việc còn lại trước Giai đoạn 3

- Chờ người dùng đồng ý trước khi viết và khóa `PREREG_CONFIRM.md`.
- Cần người dùng quyết: (a) số lượt đọc/độ đo cụ thể và quy tắc loại 6 đoạn (xem báo cáo); (b) có chạy lại ô Long G0 trên 1080 Ti không (hiện còn ~7,5 GB trống mỗi card).
