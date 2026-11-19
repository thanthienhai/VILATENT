# PREREG_LONGCTX — đăng ký trước pha ngữ cảnh rất dài (ViQuAD-XL, DỰ THẢO, CHƯA KHÓA)

Trạng thái: **ĐÃ DUYỆT (người dùng, 2026-11-10: L1–L4, chỉ 4×) và KHÓA bằng SHA-256**. (Điều kiện khóa: chỉ khóa (băm SHA-256 vào `PREREG_LONGCTX.sha256`) sau khi người dùng đồng ý nội dung này, và **trước** mọi lượt đọc của reader trên `data/icisn/longctx_p1.jsonl` và `longctx_p2.jsonl`. Mọi sai khác sau khóa phải ghi là "lệch khỏi đăng ký".)

**Dữ liệu đã dựng khi khóa:** P1 = 533 câu (19 bài đích, trung vị 17.219/35.249/67.453 token); P2 = 500 câu giữ lại trên 624 cửa sổ (78 bài Wikipedia, chồng lấn 8-gram trung vị 0,42, min 0,13; 174 câu có đáp án xuất hiện nhiều lần; trung vị ~10,7k âm tiết/bài). `full` chỉ chạy nếu vừa bộ nhớ 1080 Ti; ô thiếu được ghi rõ.

## 0. Bối cảnh
- Mục đích: ViQuAD-Long (trung vị 4.470 token) và XQuAD-vi-Long (~1.000 token) chưa thật sự dài. Pha này kiểm hai kết luận của bài ở ngữ cảnh 16k–64k token.
- Đã biết trước khi khóa (không dùng dữ liệu mới): RQ1 trên ViQuAD-Long 4× không đạt (ME hòa prompt học được); ME không nhanh hơn đọc cả bài ở ViQuAD-Long.
- Chưa có lượt đọc reader nào trên dữ liệu pha này. Đã xem: mẫu 3 ví dụ P1 và 12 cửa sổ P2 (chỉ để duyệt dữ liệu).

## 1. Dữ liệu (khóa, SHA-256 ghi trong `data/icisn/SHA256SUMS.txt` sau khi dựng)
**P1 (tổng hợp có điều khiển, thành phần chính).** `scripts/icisn/build_longctx.py`: bài đích là 19 bài kiểm thử ViQuAD; nhiễu là 66 bài sạch (18 bài kiểm thử khác, 48 bài XQuAD-vi); Wikipedia vi dài bị loại vì 74% đã nằm trong kho giai đoạn 1 (`scripts/icisn/longctx_overlap.py`). Tối đa 32 câu hỏi mỗi bài đích, mỗi câu một ô trong 18 ô (độ dài 16k/32k/64k token mục tiêu × vị trí bài đích đầu/giữa/cuối × nhiễu ngẫu nhiên/gần chủ đề theo TF-IDF); loại câu có đáp án vàng nguyên văn trong bài nhiễu. Seed 0. Số câu hỏi thực: ghi trong `SHA256SUMS`/báo cáo (dự kiến 533).
**P2 (tài liệu dài tự nhiên, thăm dò).** `scripts/icisn/gen_longctx_questions.py --full`: bài Wikipedia vi dài (>= 5.000 âm tiết) có chồng lấn 8-gram < 50% với kho giai đoạn 1; câu hỏi sinh bởi Qwen3.8-27B trên cửa sổ 12 câu, đáp án trích nguyên văn, kiểm bởi DeepSeek-V4.1-Flash (F1 >= 0,8); chấp nhận đáp án xuất hiện nhiều lần. **Có nhiễm bẩn một phần (mọi bài chung >= 13% 8-gram với kho GĐ1)**; mọi kết quả P2 gắn nhãn thăm dò, không vào họ Holm.

## 2. Điều kiện đọc (chỉ 4×, k(4) tính theo độ dài thực của ngữ cảnh)
bm25, bm25_x2, phobert, prompt-f2 (`prompt_bm25_f2`), prompt-f8 (thăm dò), M (`vilatent_m`, f=1), ME (`vilatent_me_f2`), router (suy ra, như bài chính), full (nếu vừa bộ nhớ của GPU: ghi rõ ô nào thiếu, không bỏ chọn lọc). Reader fp16 trên GTX 1080 Ti, cùng checkpoint như bài chính, không huấn luyện lại, không chọn lại siêu tham số.

## 3. Giả thuyết (P1; bootstrap ghép cặp theo bài đích, 10.000 lần, seed 0)
- **L1.** ME − prompt-f2 > 0 (một phía): RQ1 ở ngữ cảnh rất dài.
- **L2.** ME − PhoBERT > 0 (một phía): PhoBERT là bộ nén cứng tốt nhất trong bài chính.
- **L3.** [ME − PhoBERT ở 64k] − [ME − PhoBERT ở 16k] > 0 (một phía): lợi thế so với nén cứng tăng theo độ dài.
- **L4.** router − M > 0 (một phía).
Họ Holm: 4 kiểm định, một họ cho F1 và một họ cho ACC-LLM (người chấm chính DeepSeek-V4.1-Flash, prompt khóa trong `docs/icisn/judge_prompt.json`), α = 0,05. **Đạt** chỉ khi cả F1 lẫn ACC-LLM có p hiệu chỉnh < 0,05 theo đúng chiều.
**Thứ yếu, không vào họ Holm:** mọi điều kiện theo vị trí (đầu/giữa/cuối) và độ khó nhiễu; ME so với full ở độ dài mà full chạy được; prompt-f8; P2 (L1–L2 trên P2, bootstrap theo bài; kèm bản loại bài có chồng lấn >= 40%); độ trễ mỗi câu hỏi theo độ dài cho bm25, ME, M, prompt, full (đo trên cùng GPU, nêu rõ không so với H100).

## 4. Diễn giải đã nêu trước
- L1 không đạt: bài ghi rằng ở ngữ cảnh rất dài ME vẫn không hơn prompt; L1 đạt: ghi kết quả kèm giới hạn "tổng hợp".
- L3 không đạt: không được viết rằng bộ nhớ có lợi thế riêng ở văn bản dài hơn.
- Không viết kết luận về văn bản "tự nhiên rất dài" từ P1; chỉ P2 (thăm dò, có nhiễm bẩn) nói về tài liệu tự nhiên.

## 5. Đe dọa tính hợp lệ (ghi trong bài)
- P1 tổng hợp: bài nhiễu khác chủ đề (biến thể "gần chủ đề" chỉ gần hơn trong kho 66 bài), dễ cho bộ chọn câu; chỉ 19 bài đích, một seed huấn luyện, một reader.
- Mốc 16k bị vượt (trung vị 17,2k token) vì bài đích dài nhất đã ~17k token.
- P2: đã nhiễm bẩn một phần; câu hỏi do Qwen3.8-27B (cùng họ reader và người chấm phụ); câu hỏi sinh tự động, chưa có người soát đủ lớn; đáp án nhiều lần xuất hiện có thể mơ hồ.
- fp16 trên 1080 Ti; không đo thời gian so với H100; không có tuyên bố tiết kiệm.

## 6. Thứ tự
Duyệt → khóa/băm → chạy reader (nền, `--skip-existing`) → chấm bằng API → `confirm_numbers`-tương tự cho pha này → cập nhật bài.
