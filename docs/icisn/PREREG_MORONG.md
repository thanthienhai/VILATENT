# PREREG_MORONG — đăng ký trước các phép kiểm soát nội dung bộ nhớ trên P1 (WP1) và hai điều kiện đọc cả bài (WP2-T4)

Trạng thái: **KHÓA bằng SHA-256 (`PREREG_MORONG.sha256`) ngày 2026-11-17, trước mọi lượt đọc của reader với các điều kiện `zero`, `swap`, `shuf` (đầy đủ P1), `full` và `bm25_x2` (đầy đủ P1).** Mọi sai khác sau khóa phải ghi là "lệch khỏi đăng ký". `PREREG_LONGCTX.md` (đã khóa) không bị sửa; tài liệu này chỉ **thêm** phân tích.

Cơ sở: người dùng ra lệnh chạy trên mọi GPU (2026-11-17). Người dùng **chưa trả lời riêng** các mục quyết định §7 của `DE_XUAT_MO_RONG.md`; các lựa chọn dưới đây là **mặc định đã khuyến nghị ở đó** (biên tương đương Δ = 3 điểm; chỉ P1; P3 chưa dựng, chưa chạy). Người dùng có thể đổi trước khi số được xem; sau khóa mọi thay đổi ghi là "lệch".

## 0. Những gì đã nhìn thấy trước khi khóa (khai báo)
1. Kết quả L1–L4 trên P1 và P2 (điều kiện nguyên vẹn bm25, phobert, prompt-f2/f8, M, ME, router): đã xem, đã báo cáo. Vì vậy phép kiểm **tương đương** của §3 (L1, L2 với Δ) là **phân tích bổ sung trên dữ liệu đã xem**; biên Δ được cố định ở đây, không phụ thuộc vào số quan sát.
2. **Thử nghiệm điều khiển 21 câu** (hoán đổi bộ nhớ `swap=0`, M và ME, ở 32k và 64k trên 21 câu của P1): đã xem. 21 câu này **thuộc** P1. Mọi phân tích C1–C2 báo cáo thêm **bản bỏ 21 câu đó** (độ nhạy).
3. Đóng sách (`none`) trên P1 và P2: F1 12,4 và 10,6; mô tả, không thuộc họ kiểm định nào.
4. Kiểm toán dữ liệu (`RA_SOAT_DU_LIEU.md`): BM25 top-1 70,0% so với 71,9% trên ViQuAD-Long; 19 cụm; 22 câu ở 16k chỉ có n_docs = 1; vị trí lẫn với độ khó câu hỏi; 234/533 câu thiếu từ khóa tiêu đề. Đã biết trước khi khóa.

## 1. Dữ liệu
Chỉ **P1** (`data/icisn/longctx_p1.jsonl`, 533 câu, 19 bài đích, SHA-256 trong `data/icisn/SHA256SUMS.txt`). Không dùng P2 cho các kiểm định này. Không chọn tập con theo kết quả.

## 2. Điều kiện (4× như PREREG_LONGCTX, cùng checkpoint, không huấn luyện lại, không chọn lại siêu tham số)
- **Nguyên vẹn (đã có):** `vilatent_m`, `vilatent_me_f2`, `prompt_bm25_f2`, `phobert`.
- **Kiểm soát bộ nhớ (mới):** M và ME mỗi cái với `zero=1` (vector bộ nhớ trong = 0), `swap=0` (mỗi câu đọc bộ nhớ của bài khác), `shuf=0` (cùng vector, đảo thứ tự ngẫu nhiên). Một seed cho mỗi phép kiểm soát (seed 0) — ghi là hạn chế.
- **Đọc cả bài và BM25 gấp đôi (mới):** `full` và `bm25_x2` trên P1 đầy đủ, chạy trên Kaggle T4 (fp16) vì 1080 Ti không đủ bộ nhớ cho `full` ở 64k. Khác phần cứng với các điều kiện còn lại (1080 Ti, fp16): **ghi là lệch phần cứng**; không so độ trễ giữa hai loại GPU; điểm F1 vẫn so được (cùng fp16, cùng mã; không đảm bảo trùng từng bit).
- Chi tiết thực thi (không đổi kết quả mong đợi): 1080 Ti dùng `VILATENT_MAX_CHUNKS=8`, `VILATENT_CHUNK_SDPA=1`, `--batch-size 4`; T4 dùng `VILATENT_SDPA_CHUNK=512` cho `full`. `--skip-existing`, chạy tiếp được sau gián đoạn.

## 3. Giả thuyết và phép kiểm (bootstrap theo bài đích, 10.000 lần, seed 0; một phía; Holm trong họ 2 phép cho F1 và riêng cho ACC-LLM, α = 0,05)
- **C1.** `M nguyên vẹn − M swap > 0`: bộ nhớ M mang nội dung riêng của bài.
- **C2.** `ME nguyên vẹn − ME swap > 0`: phần bộ nhớ trong ME còn đóng góp khi đã có câu BM25.
- Họ Holm: {C1, C2} cho F1; {C1, C2} cho ACC-LLM (người chấm chính DeepSeek-V4.1-Flash, prompt khóa `docs/icisn/judge_prompt.json`). **Đạt** chỉ khi cả F1 lẫn ACC-LLM có p hiệu chỉnh < 0,05.
- **Thứ yếu, không vào Holm:** `nguyên vẹn − zero` và `nguyên vẹn − shuf` cho M và ME; C1–C2 theo độ dài (16k/32k/64k) và vị trí; bản bỏ 21 câu đã xem; ME so với `full` và `bm25_x2` theo độ dài (mô tả, khoảng tin cậy 95%).
- **Tương đương (bổ sung, trên dữ liệu đã xem):** với L1 (ME − prompt-f2) và L2 (ME − PhoBERT): khoảng tin cậy 90% theo bài (bootstrap, 10.000, seed 0). Chỉ khi khoảng nằm trọn trong (−Δ, +Δ) mới được viết "tương đương trong biên Δ"; Δ = **3 điểm F1** và **3 điểm ACC-LLM**. Nếu khoảng vượt biên thì viết "chưa phát hiện khác biệt lớn hơn khoảng tin cậy này", không viết "bằng nhau".

## 4. Diễn giải đã nêu trước
- C1 hoặc C2 không đạt: viết "ở P1, với 19 bài, chưa phát hiện phụ thuộc vào nội dung bộ nhớ lớn hơn khoảng tin cậy"; **không** viết rằng bộ nhớ "không mang nội dung". Kèm khoảng tin cậy.
- C1 đạt, C2 không đạt: nội dung bộ nhớ có ích khi đứng một mình; khi đã có câu BM25 phần đóng góp không được chứng minh.
- `zero` hoặc `shuf` ≈ nguyên vẹn nhưng `swap` thấp hơn: ưu tiên diễn giải "bộ nhớ mang thông tin theo bài nhưng không theo từng vector" và ghi rõ là suy đoán; chỉ khẳng định điều các phép kiểm trực tiếp hỗ trợ.
- Không viết từ P1 bất kỳ kết luận nào về văn bản tự nhiên dài; P1 là tổng hợp.

## 5. Đe dọa tính hợp lệ (ghi trong bài)
Ba hạn chế P1 đã đo (BM25 top-1 70,0%: nhiễu dễ cho bộ chọn câu; 19 cụm: khoảng tin cậy rộng; vị trí lẫn độ khó); 22 câu ở 16k chỉ có một tài liệu; một seed cho mỗi phép kiểm soát; một reader; lệch phần cứng của `full`/`bm25_x2`; 21 câu đã xem; tương đương là phân tích bổ sung.

## 6. Thứ tự
Khóa/băm → đồng bộ mã → chạy reader (nền, `--skip-existing`) → chấm bằng API (ACC-LLM) → script số liệu `scripts/icisn/morong_numbers.py` → báo cáo `KET_QUA_MORONG.md` → cập nhật bài. Thứ tự này không đổi theo số quan sát.
