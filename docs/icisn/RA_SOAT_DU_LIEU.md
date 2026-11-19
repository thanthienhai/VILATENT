# Rà soát dữ liệu pha ngữ cảnh rất dài (P1 ViQuAD-XL, P2 Wikipedia dài) — 2026-11-17

Phạm vi: chỉ đọc dữ liệu và kết quả đã có; **không đổi** `PREREG_LONGCTX.md` (băm khớp), không đổi dữ liệu, không chạy lại điều kiện nào
trong họ L1–L4. Mọi số dưới đây đều tái lập được bằng `scripts/icisn/audit/*.py` (đầu ra: `results/icisn/audit/*.txt`).
Cách chạy: từ thư mục gốc repo, `python -I -X utf8 scripts/icisn/audit/<tên>.py`.

## 1. Kết luận

- **Toàn vẹn: đạt.** Dữ liệu và kết quả đã chạy không có lỗi cơ học.
- **Giá trị suy luận: hạn chế, đã đo được hạn chế đó.** P1 không làm truy hồi từ vựng khó hơn; chỉ 19 cụm bài; theo vị trí và theo độ dài là so sánh giữa các câu hỏi khác nhau
  (lẫn độ khó). P2 nhiễm bẩn vừa phải và chưa có người kiểm câu hỏi.
- **Hệ quả cho bài:** kết quả âm của L1–L3 chỉ được ghi là "không phát hiện chênh lệch lớn hơn ≈ 3 điểm F1 trên P1", không phải "tương đương"
  (xem §3.2). Các phân tích theo vị trí của P1 không được diễn giải như hiệu ứng "lạc ở giữa" (§3.4).
- **Hệ quả cho đề xuất chạy mới:** WP1 (đối chứng nội dung) chạy được trên P1 hiện có; **muốn nói gì về ngữ cảnh dài thì cần bộ dữ liệu mới khó hơn (P3, §5)**;
  cần thêm mốc đóng sách (đang chạy) và một lượt kiểm câu hỏi.

## 2. Điều đã kiểm và đạt

| Kiểm tra | Kết quả |
| --- | --- |
| Băm `longctx_p1.jsonl`, `longctx_p2.jsonl`, `xquad_vi_long.jsonl` | Khớp `SHA256SUMS.txt`, ở máy local **và** gpu1080 |
| Băm `PREREG_LONGCTX.md` | `OK` theo `PREREG_LONGCTX.sha256` |
| Kết quả: số dòng mỗi điều kiện | P1: 6 điều kiện × 533; P2: 6 × 500; không trùng id, không thiếu, không thừa, không dự đoán rỗng |
| Nguồn ViQuAD-Long `s0`/`s1` | Hai nửa rời nhau: 10 + 9 bài = 19 bài, 1.341 + 1.312 câu, không trùng id; ngữ cảnh là cả bài; mọi đáp án vàng nằm trong ngữ cảnh |
| P1: số dòng, id, câu hỏi | 533 id duy nhất, 533 câu hỏi duy nhất; 19 bài, 24–31 câu mỗi bài |
| P1: cân bằng ô | 18 ô (độ dài × vị trí × nhiễu), 25–33 câu mỗi ô; độ dài 183/174/176; vị trí 176/181/176 |
| P1: đáp án trong ngữ cảnh | 533/533 có đáp án vàng nguyên văn (NFC, không phân biệt hoa thường) |
| P1: nhãn vị trí khớp thực tế | Vị trí đáp án (tỉ lệ ký tự) trung vị 0,04 / 0,43 / 0,95 cho đầu / giữa / cuối |
| P1: độ dài thực | Trung vị 17.219 / 35.158 / 67.453 token cho mốc 16k / 32k / 64k; không câu nào vượt mục tiêu quá 25% |
| Nén có phủ toàn bộ ngữ cảnh | Trung bình 40.203 token, tỉ lệ nén thực 3,99 (M) và 4,00 (ME); `VILATENT_MAX_CHUNKS=8` chỉ giới hạn số khối **mỗi lượt viết** (`vilatent/model.py`), không cắt ngữ cảnh |
| Rò rỉ: 19 bài đích với ViQuAD | Chồng lấn 8-gram tối đa 0,9% (train), 0% (dev, gate, select); không bài nào ≥ 10% |
| Rò rỉ: XQuAD-vi (nhiễu) | G0.4: 0/240 đoạn ≥ 50% với ViQuAD; 6/240 ≥ 50% với kho giai đoạn 1 (không ảnh hưởng đáp án vì đã loại câu có đáp án trong nhiễu) |
| Rò rỉ: 19 bài đích với kho giai đoạn 1 (346.752 tài liệu) | 19/19 bài có ≥ 1 8-gram chung nhưng **tối đa 2,9%, trung bình 1,3%, không bài nào ≥ 10%** (`results/icisn/audit/audit_overlap.txt`) |
| Rò rỉ: tiêu đề bài đích | 0 tiêu đề trùng với `viquad_train` và `viquad_dev` |

## 3. Điểm yếu đã đo được

### 3.1 P1: thêm bài nhiễu gần như không làm truy hồi từ vựng khó hơn

BM25 theo đoạn (k1 = 1,2, b = 0,75), hạng của đoạn chứa đáp án vàng, **cùng 533 câu hỏi**:

| Ngữ cảnh | Đúng ở hạng 1 | Trong top-10 | Số đoạn mỗi ngữ cảnh (trung vị) |
| --- | ---: | ---: | ---: |
| Chỉ bài đích (ViQuAD-Long gốc) | 71,9% | 96,6% | — |
| P1 (bài đích + 66 bài nhiễu) | **70,0%** | **95,5%** | 164 |
| P1, nhiễu ngẫu nhiên / gần chủ đề | 72,8% / 67,0% | 96,3% / 94,6% | |
| P1 theo độ dài 16k / 32k / 64k | 66,1% / 73,6% / 70,5% | 95,6% / 96,6% / 94,3% | |
| P2 (Wikipedia dài, câu hỏi sinh bằng LLM) | 67,0% | 84,4% | 156 |

Nghĩa là P1 kiểm khả năng **bỏ qua phần đệm không liên quan**, không kiểm khả năng chọn giữa nội dung dễ nhầm. Điều này khớp với việc F1 của
BM25 gần như không đổi theo độ dài (59,7 → 59,3 → 59,2) và là lời giải thích chính cho việc L3 không thể đạt bằng dữ liệu này.
Đây chính là mối đe dọa "dễ cho bộ chọn câu" đã ghi trong PREREG_LONGCTX §5, nay có số đo.

### 3.2 Chỉ 19 cụm bài: độ chính xác thống kê thấp

Bootstrap theo bài (10.000 lần, seed 0) trên chênh lệch F1 ghép cặp, từ kết quả đã chạy:

| Phép so | Chênh lệch | CI 95% | Nửa độ rộng | Số cụm |
| --- | ---: | --- | ---: | ---: |
| P1 ME − prompt-f2 | −0,90 | [−3,45; +1,85] | 2,65 | 19 |
| P1 ME − PhoBERT | +1,97 | [−1,29; +5,04] | 3,16 | 19 |
| P2 ME − prompt-f2 (thăm dò) | −3,39 | [−5,54; −1,24] | 2,15 | 78 |
| P2 ME − PhoBERT (thăm dò) | +2,63 | [+0,12; +5,05] | 2,47 | 78 |

Độ lệch chuẩn giữa các bài của chênh lệch là 5,8–6,8 điểm. Để nửa độ rộng ≈ 2 điểm cần khoảng 35–47 bài đích; ≈ 3 điểm cần 15–21.
**Hệ quả:** "không đạt" ở P1 nghĩa là "không phát hiện chênh lệch lớn hơn ≈ 3 điểm", không phải tương đương. Ngưỡng tương đương cho các phép đối chứng
mới (WP1) không nên nhỏ hơn ≈ 3 điểm F1 nếu chỉ dùng P1.

### 3.3 P1: 16k không phải ngữ cảnh có nhiễu ở mọi câu

22/183 câu ở mốc 16k (12%) có `n_docs = 1`: bài đích đã ≥ 16k token nên không có nhiễu và nhãn vị trí vô nghĩa; 66 câu (36%) có ≤ 2 bài. Mốc 16k
thực chất lẫn "bài dài đơn" với "bài đích + nhiễu". Không có ô 32k/64k nào như vậy (≥ 2 và ≥ 5 bài).

### 3.4 P1: vị trí (và độ dài) lẫn với độ khó của câu hỏi

Mỗi câu hỏi chỉ nhận một ô, nên hiệu ứng vị trí và độ dài là so sánh **giữa các câu hỏi khác nhau** (≈ 1,5 câu mỗi ô mỗi bài). Phép đo chỉ ra hệ quả:
BM25 chọn câu không biết vị trí, nhưng đúng ở hạng 1 là 75,6% (đầu), **61,3% (giữa)**, 73,3% (cuối). F1 của BM25 giữa − đầu = −6,9 [−15,2; +1,7 theo bài] và
PhoBERT, ME, prompt đều thấp ở "giữa". Phần lớn (không loại được hết) chênh lệch này là độ khó của các câu rơi vào ô "giữa", không phải hiệu ứng vị trí của reader.
**Các phân tích thứ yếu theo vị trí/độ dài của PREREG_LONGCTX không được diễn giải như hiệu ứng "lạc ở giữa" hay "suy giảm theo độ dài".**

### 3.5 P1: câu hỏi chưa chắc tự đủ nghĩa trong một ngữ cảnh gồm nhiều bài

- 234/533 (44%) câu hỏi không chứa từ nào của tiêu đề bài đích; 33 câu có từ chỉ định ("này", "đó", "ấy"…).
- Ví dụ: "Khi gặp Hoàng đế, người ta phải làm gì?"; "Các bài hát dễ lan truyền hơn nhờ phát minh ra thứ gì?"; "Điều gì đã xảy ra khi tiến hành mở rộng hơn nữa các ngôi đền?".
- Bộ lọc duy nhất là "đáp án vàng không xuất hiện nguyên văn trong bài nhiễu"; chưa ai kiểm một câu có đáp án khác, đúng, ở bài nhiễu hay không.
- Trần đo được: lấy tốt nhất trong 6 điều kiện, F1 trung bình chỉ 81,7; **21 câu (3,9%) bằng 0 ở cả 6 điều kiện**, 39 câu (7,3%) có tốt nhất < 20.
  Đây là cận trên cho tỉ lệ câu có lỗi hoặc cực khó, chưa phân biệt được hai khả năng.
- **Chưa kiểm:** không có người hay LLM nào đã đánh giá "tự đủ nghĩa / đáp án duy nhất" cho P1. (Đề xuất kiểm ở WP0b, không đo trên P1 bằng điều kiện nào đã khóa.)

### 3.6 P2: các giới hạn đã đo

| Mục | Số đo |
| --- | --- |
| Dòng / câu hỏi duy nhất / bài | 500 / 494 / 78 (3–8 câu mỗi bài) |
| Đáp án nguyên văn trong ngữ cảnh | 488/500; **12 câu không khớp nguyên văn** (cửa sổ sinh ghép câu bằng dấu cách, bài gốc có xuống dòng); F1 theo token không bị ảnh hưởng nhiều nhưng ghi nhãn |
| Đáp án xuất hiện nhiều lần trong bài | 174/500 (≥ 5 lần: 80) |
| Độ dài tài liệu | Trung vị 10.671 âm tiết, tối đa 34.894; trung bình **15.899 token** (Qwen3.5, `mean_context_tokens`): **bằng mốc thấp nhất của P1 (16k), không có ô 32k-64k** |
| Chồng lấn 8-gram với kho giai đoạn 1 | Trung vị 0,42, nhỏ nhất 0,13; **292/500 câu thuộc bài ≥ 0,40**: bộ viết đã được huấn luyện nén phần lớn các bài này |
| Trùng từ câu hỏi ↔ câu chứa đáp án | 0,58 (P2) so với 0,48 (P1): câu hỏi sinh từ cửa sổ nên dễ cho BM25 |
| Kiểm câu hỏi | Bởi DeepSeek-V4.1-Flash trên **cửa sổ 12 câu**, không phải cả bài; không có người kiểm |
| Truy hồi BM25 theo đoạn | hạng 1: 67,0%; top-10: 84,4% (khó hơn P1 ở top-10) |

P2 vẫn chỉ nên là thăm dò, như đã ghi.

## 4. Điều chưa đo (đang đo hoặc cần làm)

1. **Mốc đóng sách** (reader không có ngữ cảnh), đã đo ngày 2026-11-17 trên 1080 Ti, fp16, mô tả, không vào họ kiểm định nào (`results/icisn_pilot/closed_book/`):
   P1 F1 **12,4** (EM 1,7; n = 533); P2 F1 **10,6** (EM 1,2; n = 500). Reader tự trả lời được rất ít, kể cả ở P2 (Wikipedia), nên điểm của các điều kiện (43-64 ở P1, 59-85 ở P2) đến từ ngữ cảnh,
   không phải từ kiến thức sẵn có. **Đóng sách không loại được nhiễm bẩn mức bộ viết** (P2 chồng lấn 8-gram với kho giai đoạn 1), chỉ loại được việc reader thuộc sẵn đáp án.
2. Ô `full` và `bm25_x2` của P1/P2: bị bỏ trên 1080 Ti (lệch khỏi đăng ký); không có mốc "đọc hết" nên không biết ME mất bao nhiêu so với đọc cả bài.
3. fp16 (1080 Ti) so với bf16 (H100) ở ngữ cảnh ~40k token: G0.2 chỉ kiểm 200 câu ở ngữ cảnh ngắn, chưa kiểm 40k.
4. Kiểm "tự đủ nghĩa / đáp án duy nhất" cho P1 và kiểm câu hỏi P2 trên cả bài.
5. Lượt pilot đối chứng tráo bộ nhớ đã để lộ F1 mô tả trên 21 câu P1 mỗi độ dài (xem `DE_XUAT_MO_RONG.md` mục 3, WP1): các câu này vẫn nằm trong tập sẽ đo.

## 5. Bộ dữ liệu mới đề xuất: P3 (nhiễu khó, không chạy reader khi dựng)

Mục tiêu: một bộ mà việc thêm ngữ cảnh **thật sự** làm khó việc chọn câu, để L1–L3 có ý nghĩa ở độ dài lớn. Dựng hoàn toàn bằng CPU và API, **không có reader nào đọc trước khi khóa**.

- Câu hỏi và bài đích: lấy lại 19 bài ViQuAD-test (sạch với bộ viết, §2); câu hỏi từ `viquad_long_test_*` (2.653 câu) hoặc P1; chỉ giữ câu qua bước kiểm tự đủ nghĩa (WP0b).
- Nhiễu: **đoạn** (không phải cả bài) có điểm BM25 cao nhất với câu hỏi trong kho bài khác (19 bài test khác + 48 bài XQuAD-vi, có thể thêm Wikipedia vi vì nhiễu rò rỉ không ảnh hưởng tính đúng của đáp án; cần ghi rõ), loại đoạn chứa đáp án vàng (khớp không dấu, chuẩn hóa số) và loại đoạn mà người chấm LLM cho là cũng trả lời được câu hỏi (kiểm top-5 nhiễu mỗi câu).
- Thiết kế **trong cùng câu hỏi**: mỗi câu hỏi xuất hiện ở nhiều độ dài và nhiều vị trí (ví dụ một tập con 150–200 câu × 3 độ dài × 3 vị trí) để tách độ khó câu hỏi khỏi độ dài/vị trí.
- Tiêu chí chấp nhận **khóa trước khi chạy reader**: BM25 hạng 1 theo đoạn ≤ 55% (so với 70,0% ở P1) và tụt rõ theo độ dài; số câu đạt tự đủ nghĩa ≥ 85% sau kiểm; mốc 16k không có câu `n_docs = 1`.
- Quy mô: ≥ 35 cụm bài (để nửa độ rộng ≈ 2 điểm) hoặc nêu rõ độ rộng nhận được. Với chỉ 19 bài đích ViQuAD-test thì chỉ đạt ≈ ±3; thêm bài đích từ nguồn sạch khác (XQuAD-vi 48 bài, dài ~1,1k token, ghép thành ngữ cảnh dài) là phương án để tăng số cụm.
- Đây là dữ liệu và đăng ký **mới**; không đổi L1–L4.

## 6. Việc phải làm trước khi xin H100 (không cần H100)

| Mã | Việc | Tài nguyên |
| --- | --- | --- |
| WP0a | Mốc đóng sách P1/P2 | **Đã xong** (1080 Ti, ≈ 48 phút; F1 12,4 và 10,6) |
| WP0b | Kiểm "tự đủ nghĩa / đáp án duy nhất" của P1 (533 câu) và của P2 trên cả bài (500 câu); mẫu 100 câu cho người kiểm | API (≈ 1.000–3.000 lời gọi) + 3–5 giờ người |
| WP0c | Dựng và khóa P3 (CPU + API), tiêu chí chấp nhận ở §5 | 1–3 ngày công, GPU 0 |
| WP0d | `PREREG_MORONG.md` (WP1, ngưỡng tương đương) | 0,5 ngày công |
| WP0e | `full`/`bm25_x2` ở P1 trên 2 T4 (đã đo thời gian) | ≈ 9 giờ mỗi T4, Kaggle |
| WP1 (P1) | Đối chứng nội dung zero/swap/shuf cho M và ME trên P1 | 2 × 1080 Ti, ≈ 9 giờ mỗi GPU |
