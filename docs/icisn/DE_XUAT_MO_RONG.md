# Đề xuất giai đoạn mở rộng ViLatent (ICISN 2027) và nhu cầu tài nguyên

Ngày soạn: 2026-11-16; **bản 2: 2026-11-17, sau khi rà soát dữ liệu** (`RA_SOAT_DU_LIEU.md`). Trạng thái: **bản nháp để chủ đề tài duyệt**,
chưa khóa. Chưa có lượt chạy thật nào của WP1–WP8. Đã chạy: ba lượt pilot đo thời gian (T4, 1080 Ti) và mốc đóng sách mô tả (mục 3, WP0a).
Con số thời gian lấy từ `REPORT_VILATENT_2910.md` (lượt H100 28-29/10/2026) và từ ba pilot (T4: `full`, `bm25_x2` ở 16k/32k/64k; 1080 Ti: tráo bộ nhớ ở 32k/64k).
Mọi con số còn lại là **ước lượng**, có ghi cơ sở và khoảng sai số; **chưa có số đo H100 nào trên dữ liệu 16k-64k**, nên cần một lượt thử 0,5 GPU-giờ trước khi cam kết.

**Đổi so với bản 1:** (i) thêm WP0 (sửa dữ liệu, không cần H100); (ii) dữ liệu P1 hợp lệ về cơ học nhưng không làm truy hồi khó hơn, nên bài toán "ngữ cảnh dài"
cần bộ mới **P3**; (iii) WP1 chạy trước trên 1080 Ti (không cần H100) và dùng P1 + XQuAD-vi thay vì tập select 6 bài; (iv) tách đề nghị H100 làm hai pha; (v) số GPU-giờ tăng do P3.

## 0. Tóm tắt một trang

**Vấn đề.** Kết quả đã khóa (PREREG_LONGCTX, 16k-64k, Qwen3.5-2B, một seed) cho thấy bộ nhớ mềm + BM25 (ME) không hơn prompt học
được ở cùng ngân sách (L1, L2, L3 không đạt; L4 đạt nhưng tầm thường). Bài sẽ là một **phát hiện có kiểm soát**. Phát hiện này
hiện còn năm chỗ hở mà người phản biện sẽ hỏi: (a) chưa rõ bộ nhớ có mang nội dung tài liệu trong ME hay chỉ BM25 làm việc,
(b) chỉ một reader và một seed, (c) các ô `full` và `bm25_x2` bị bỏ do hết bộ nhớ trên 1080 Ti và số liệu fp16 so với bf16,
(d) chưa đo độ trễ và VRAM theo độ dài, (e) judge LLM chưa có phép kiểm độ dao động và độ đồng thuận với người, và, **từ lượt rà soát dữ liệu**,
(f) P1 không làm truy hồi từ vựng khó hơn (BM25 đúng ở hạng 1: 70,0% có 66 bài nhiễu so với 71,9% chỉ có bài đích), chỉ có 19 cụm bài (CI ±2,7 đến ±3,2 điểm F1),
hiệu ứng vị trí và độ dài lẫn với độ khó của câu hỏi, và chưa có mốc đóng sách.

**Đề xuất.** Ba mức xin tài nguyên, mỗi mức chứa mức trước. Số mới (bản 2) gồm cả đánh giá trên P3 (WP0c, mục 3):

| Mức | Nội dung | GPU-giờ H100 (thấp-cao) | Cộng 1,5× dự phòng | Thời gian lịch (ước) |
| --- | --- | ---: | ---: | --- |
| **A. Tối thiểu** (không huấn luyện) | WP1 trên P3, WP2 (ô bị bỏ, bf16), đánh giá trên P3, WP6 đo độ trễ, WP7 phép đo judge | 6,5-20,5 | **10-31** | 4-7 ngày |
| **B. Khuyến nghị** | A + WP3 seed thứ hai + WP4 reader Transformer thuần thứ hai (kèm đánh giá trên P3) | 24,5-58,5 | **37-88** | 2-3 tuần |
| **C. Mở rộng** | B + WP5 cải tiến công thức huấn luyện bộ ghi + WP6b thử vLLM + WP8 bộ văn bản dài tự nhiên | 35,5-80,5 | **53-121** | 4-5 tuần |

Biên độ rộng hơn bản 1 vì phần lớn thời gian đọc trên P3 chưa đo được trên H100 (0,25-1 giờ mỗi điều kiện mỗi 1.350 ngữ cảnh; `full` 1-2,5 giờ).

**Hai pha xin H100 (mức B).** Pha 1: huấn luyện và đánh giá chuẩn của WP3 (seed hai) và WP4 (reader hai), ≈ 16-32 GPU-giờ, ×1,5 = **24-48**.
Phần này **không phụ thuộc** vào việc P3 có đạt hay không và có thể xin ngay. Pha 2: phần còn lại (WP1 trên P3, WP2, đánh giá trên P3 cho cả bốn hệ, WP6),
≈ 8,5-26,5 GPU-giờ, ×1,5 = **13-40**; **chỉ xin sau giai đoạn 0** (mục 5), khi P3 đã qua tiêu chí chấp nhận và WP1 trên P1 đã cho tín hiệu,
nếu không đó là giờ GPU đọc trên dữ liệu chưa đủ tốt. Hai pha cộng lại bằng mức B (37-88).

Khuyến nghị: **xin mức B theo hai pha**. Mức A trả lời được câu hỏi (a), (c), (d), (e), (f) nhưng không trả lời (b), mà (b) là điểm yếu bị
đánh vào đầu tiên. Mức C chỉ nên xin nếu B xong sớm và kết quả B mở ra câu hỏi mới.

**Điều không thay đổi:** các giả thuyết L1-L4 đã khóa trong `PREREG_LONGCTX.md`. Mọi thí nghiệm dưới đây là phần đăng ký mới
(`PREREG_MORONG.md`, cần viết và khóa hash trước khi chạy), và đều không dùng để đảo kết luận L1-L4.

## 1. Ràng buộc chung (nhắc lại từ quy tắc đã đặt)

- Khóa giả thuyết, ngưỡng, quy tắc router, prompt tóm tắt và prompt judge trước khi xem số của tập tương ứng; không đổi sau đó.
- Không chọn biến thể tốt nhất trên test hay XQuAD-vi. Không dùng LLM 27B làm reader.
- Không ghi vào `results/paper/`. Đầu ra mới: `results/icisn_ext/`, `docs/icisn/`, `data/icisn/`.
- Mọi lệch khỏi đăng ký ghi thành "lệch khỏi đăng ký". Phân tích thêm sau khi thấy số ghi nhãn **thăm dò**.
- Không viết khẳng định tiết kiệm thời gian; độ trễ báo thuần số đo.
- Máy chạy phải ở một commit sạch (mọi `.meta.json` ghi `git_commit`; lượt trước đã vướng điều này).

## 2. Cơ sở ước lượng

### 2.1 Số đã đo trên H100 (lượt 28-29/10/2026, Qwen3.5-2B, bf16, `REPORT_VILATENT_2910.md`)

| Việc | Thời gian đo | GPU | Suy ra |
| --- | --- | --- | --- |
| Smoke test | 32 phút 11 giây | 1 | |
| `stage1` 5000 bước | 56 phút 52 giây | 1 | 0,68 giây/bước |
| `stage2` mem + prompt, mỗi bên 4000 bước | 72 phút 43 giây (hai tiến trình song song) | 2 | 1,09 giây/bước; ≈ 2,4 GPU-giờ cho cả hai |
| `stage2_frozen` 4000 bước | 49 phút 39 giây | 1 | 0,75 giây/bước |
| Logit thầy (`teacher`) | 37 phút 40 giây | 2 | ≈ 1,25 GPU-giờ |
| Mốc cứng (`baselines`) | 28 phút 15 giây | 1 | |
| `eval_select`, `choose`, `eval_gate`, `decide` | ≈ 42 phút | 2 | ≈ 1,4 GPU-giờ |
| `signal` | 18 phút 7 giây | 1 | |
| Ô `full` trên test (2653 câu, ≈ 9,7k token/prompt) | 821 giây | 1 | ≈ 0,31 giây/câu |
| Viết bộ nhớ ME, batch 1 (lượt thử 26/10) | 506 ms cho ≈ 7,9k token | 1 | ≈ 6,4 ms/1k token |
| Bộ nhớ đỉnh khi huấn luyện, batch 32 (lượt thử) | 7,9 GB | 1 | |

### 2.2 Giả định dùng để ngoại suy (cần hiệu chỉnh)

- Đọc một câu hỏi ở P1 (16k-64k, trung bình ≈ 37k token): 0,5-2 giây mỗi câu mỗi điều kiện trên H100 (ngoại suy từ 0,31 giây/câu
  ở 9,7k token và 6,4 ms/1k token của bộ ghi; ô `full` ở 64k nặng hơn, tính 2-5 giây).
- Huấn luyện reader cỡ 4B: gấp khoảng 2 lần thời gian bước của cỡ 2B (chưa đo).
- Đánh giá test đầy đủ: 1,5-3 giờ trên 2 GPU theo `DU_THAO_NGHIEN_CUU.md` mục 10 (ước lượng, chưa đo).
- Hệ số dự phòng 1,5× theo thói quen ngưỡng báo lại ở `G0_KIEM_KE.md` mục 0.5.

## 3. Các gói công việc

### WP0. Sửa dữ liệu trước khi xin H100 (không cần H100; điểm yếu f)

Chi tiết số đo ở `RA_SOAT_DU_LIEU.md`. Bốn việc, đều dùng GPU rảnh, API hoặc con người:

- **WP0a. Mốc đóng sách** (reader không có ngữ cảnh) cho P1 và P2. **Đã xong** trên 1080 Ti: F1 12,4 (P1) và 10,6 (P2), EM < 2% (`results/icisn_pilot/closed_book/`). Mô tả, không vào họ kiểm định nào.
- **WP0b. Kiểm "tự đủ nghĩa / đáp án duy nhất"** cho 533 câu P1 và kiểm câu hỏi P2 **trên cả bài** (bản gốc chỉ kiểm trên cửa sổ 12 câu). Người chấm LLM chính (prompt khóa trước khi chạy,
  **không cho thấy dự đoán của bất kỳ điều kiện nào**) cộng mẫu 100 câu có người kiểm. Kết quả chỉ dùng để (1) mô tả chất lượng dữ liệu, (2) định nghĩa trước một **tập con sạch** làm phân tích độ nhạy
  (thứ yếu, ghi nhãn thăm dò vì kết quả điều kiện trên P1 đã được xem). Không loại câu khỏi phân tích chính.
- **WP0c. Dựng và khóa P3** (nhiễu khó; mục 5 của `RA_SOAT_DU_LIEU.md`). Tiêu chí chấp nhận **chỉ dùng truy hồi từ vựng, không dùng reader**: BM25 hạng 1 theo đoạn ≤ 55%;
  ≥ 85% câu đạt kiểm tự đủ nghĩa; mốc 16k không có ngữ cảnh một bài. Thiết kế trong cùng câu hỏi (mỗi câu ở nhiều độ dài/vị trí) để tách độ khó khỏi độ dài/vị trí.
  Ước 1-3 ngày công, không GPU. Nếu P3 không đạt tiêu chí thì **không chạy reader trên P3** và bài ghi giới hạn của P1.
- **WP0d. `PREREG_MORONG.md`**: WP1 (H-C1, H-C2, ngưỡng), phép đo trên P3, tập con sạch. Khóa băm trước khi chạy WP1 chính thức.

### WP1. Đối chứng nội dung cho bộ nhớ (điểm yếu a)

**Câu hỏi.** Bộ nhớ có mang thông tin của chính tài liệu, hay mô hình chỉ học cách dùng một đầu vào bất kỳ? Trong ME, bộ nhớ
đóng góp gì ngoài các câu BM25?

**Lý do.** Một mức giảm khi đặt bộ nhớ về 0 không chứng minh bộ nhớ có ích (đối chứng nội dung trong 2610.19373: đặt hằng số vẫn
đạt một phần lợi ích). Hiện bài mới *suy ra* "điểm của ME đến từ BM25"; cần đo trực tiếp.

**Thiết kế (chỉ suy luận, dùng checkpoint hiện có, không huấn luyện lại).**
- Điều kiện cho cả M và ME ở 4×, đã cài và có test trong `vilatent/evaluate.py` và `scripts/evaluate.py` (chưa commit): **`zero=1`** (giữ vector đầu và cuối, đặt các vector giữa về 0),
  **`swap=<seed>`** (tráo bằng bộ nhớ của bài khác, bài có ít nhất bấy nhiêu vector), **`shuf=<seed>`** (giữ vector đầu và cuối, hoán vị ngẫu nhiên các vector giữa). Cùng với "nguyên vẹn" là 4 trạng thái.
- Mốc neo: đóng sách (WP0a). Phép kiểm Δ-logit: xác nhận bộ nhớ thật sự làm đổi đầu ra (đề phòng lỗi âm thầm kiểu 2609.04434).
- **Dữ liệu (đổi so với bản 1):** P1 (533 câu, 19 cụm) là chính. **Không dùng** ViQuAD-Long select (621 câu nhưng chỉ 6 bài và đã dùng để chọn f\* và Sum). Nguồn phụ để tăng số cụm:
  XQuAD-vi-long (1.190 câu, 48 bài, ≈ 800 âm tiết, sạch với ViQuAD, 6/240 đoạn chồng lấn ≥ 50% với kho giai đoạn 1). Với P3, chỉ chạy nguyên vẹn và tráo.
  P2 làm phụ (thăm dò).
- **Ngưỡng tương đương `[CẦN QUYẾT]`, khuyến nghị dựa trên số đo:** nửa độ rộng CI 95% hiện có ở P1 là 2,7-3,2 điểm F1 (`RA_SOAT_DU_LIEU.md` §3.2). Một ngưỡng nhỏ hơn 3 điểm
  thì P1 không thể chứng minh "tương đương" dù không có chênh lệch thật. Đề xuất **Δ = 3 điểm F1 và 3 điểm ACC-LLM** (kiểm TOST hai phía, CI 90% theo bài); nếu muốn Δ = 2 cần ≥ 35 cụm,
  tức phải gộp thêm cụm từ XQuAD-vi hoặc P3. Quyết định này phải khóa **trước** khi chạy WP1 chính thức.
- **Lưu ý khóa trước (peek):** pilot 21 câu mỗi độ dài đã cho F1 mô tả (M 66,6→14,7 ở 32k, 36,7→16,9 ở 64k; ME f2 71,6→69,8 và 53,3→51,5). Các câu này nằm trong tập sẽ đo. `PREREG_MORONG.md`
  phải nêu H-C1 và H-C2 là giả thuyết có trước pilot (pilot chỉ để đo thời gian) và ghi rủi ro "forking paths".
- Phân tích không tốn GPU: F1 theo vị trí đáp án so với ranh giới khối của bộ ghi (chẩn đoán "mất ở biên", 2412.17483), và tỉ lệ
  `aie` (đáp án có nguyên văn trong bằng chứng) theo độ dài.

**Giả thuyết đề xuất khóa trước khi chạy** (cần chủ đề tài duyệt, ngưỡng tương đương `[CẦN QUYẾT]`):
- H-C1: F1 và ACC-LLM của M nguyên vẹn lớn hơn M bị tráo bộ nhớ (một phía, Holm theo hai độ đo).
- H-C2: F1 và ACC-LLM của ME nguyên vẹn lớn hơn ME bị tráo bộ nhớ.
- Cách đọc: nếu H-C2 không đạt, bài ghi "trong ME, bộ nhớ không đóng góp phát hiện được ngoài bằng chứng BM25" (kèm cận khoảng
  tin cậy); nếu đạt, bài ghi mức đóng góp.

**Tài nguyên.**
- **Giai đoạn 0, không cần H100:** P1, 2 điều kiện (M, ME) × 3 đối chứng (zero, swap, shuf) = 6 ô; đã đo trên 1080 Ti ≈ 2,7-3,1 giờ mỗi ô → **≈ 17-19 giờ GPU, chia hai 1080 Ti ≈ 9 giờ mỗi GPU**
  (bộ nhớ đỉnh 6,8 GB ở 32k, 9,0 GB ở 64k). XQuAD-vi-long ngắn (≈ 1k token): vài giờ cho cả bộ. (6 ô × 2,7-3,1 giờ = 16-19 giờ; chia hai GPU ≈ 8-9,5 giờ.)
- **H100:** WP1 trên P3 (nguyên vẹn + tráo, M và ME, tập con trong-cùng-câu-hỏi ≈ 1.350 ngữ cảnh) **1-4 GPU-giờ**. Nếu 1080 Ti không rảnh, P1 chạy trên H100 mất 1,5-4 GPU-giờ.
Không cần gọi API ngoài chấm lại ngoài người chấm chính đã khóa (nhiều bộ ba trùng sẽ được cache).

### WP2. Hoàn tất các ô bị bỏ và lặp lại P1/P2 trên bf16 (điểm yếu c, một phần)

**Lý do.** Ngữ cảnh rất dài đã chạy trên 1080 Ti, fp16, với attention chia khối, bộ ghi 8 khối mỗi lượt, và thiếu hai ô
(`bm25_x2`, `full`) vì hết bộ nhớ. Đây là các lệch khỏi đăng ký đã ghi. Chạy lại trên H100 bf16 loại gần hết các lệch này.

**Thiết kế.**
- Chạy lại cả 6 điều kiện đã có (bm25, phobert, prompt_f2, prompt_f8, M, ME) cho P1 và P2, cộng `bm25_x2` và `full`.
- Giữ nguyên dữ liệu và hash (`data/icisn/longctx_p1.jsonl`, `longctx_p2.jsonl`), nguyên prompt judge đã khóa. Dùng chính
  `scripts/icisn/run_longctx.sh` (bỏ cờ attention chia khối vì H100 có flash/fla).
- So khớp kết quả với bản 1080 Ti theo `id` (độ chênh F1 và tỉ lệ dự đoán trùng), như `G0_KIEM_KE.md` mục 0.2.
- Ô `full` ở 64k: dùng cơ chế nhúng lười đã sửa trong `vilatent/evaluate.py` (bản cũ cần ≈ 105 GB nếu nhúng hết trước).

**Tài nguyên.** 8 điều kiện × 1.033 câu × 1-5 giây ≈ **3-7 GPU-giờ H100**. Bộ nhớ host ≥ 64 GB.
Chấm judge lại: ≈ 3.148 bộ ba đã có trong cache; chỉ phát sinh cho `full` và `bm25_x2` (≈ 1.000-2.000 bộ ba).

**Phần có thể làm trước trên GPU miễn phí (đã đo bằng pilot).** `full` và `bm25_x2` của P1 chạy được trên Kaggle T4 (fp16, attention chia khối): `full` ≈ 17 / 54 / 190 giây mỗi câu ở
16k / 32k / 64k (đỉnh 8,2 / 11,8 / 13,1-13,9 GB), `bm25_x2` ≈ 7 / 20 / 78 giây; ngoại suy P1 ≈ 12 giờ cho `full` và ≈ 5,2 giờ cho `bm25_x2`, chia hai T4 ≈ 9 giờ mỗi T4. Ô `full` ở 64k cần
nhúng lười (đã cài) và núm kích thước khối attention `VILATENT_SDPA_CHUNK` (chưa đưa vào repo). Kết quả T4 (fp16) vẫn là lệch khỏi đăng ký so với bf16; H100 dùng để đối chiếu, không thay thế.

### WP3. Seed huấn luyện thứ hai (điểm yếu b)

**Lý do.** Một seed không cho biết chênh lệch giữa hai lần huấn luyện có lớn bằng chênh lệch giữa các phương pháp hay không.
`RUN_CO_BAN.md` đã yêu cầu hỏi chủ đề tài trước khi thêm seed; đây là đề xuất đó.

**Thiết kế.** Cùng cấu hình bậc Cơ bản, seed khác: `stage1`, `stage2` (mem và prompt). Dùng lại logit thầy và bộ chọn PhoBERT
(không phụ thuộc seed của bộ ghi). Đánh giá trên select/gate như quy trình cũ (f\* chọn trên select, test đọc một lần), rồi P1/P2.
Ghi seed vào mọi `.meta.json`.

**Tài nguyên.**

| Phần | GPU-giờ |
| --- | ---: |
| `stage1` (0,95) + `stage2` mem và prompt (2,4) | ≈ 3,4 |
| Đánh giá select/gate/chọn f\* | ≈ 1,4 |
| Test đọc một lần (ME, prompt, M, mốc) | 1-3 |
| P1/P2 cho ba điều kiện của seed mới | 1-2 |
| **Tổng** | **≈ 6-10** |

Tiêu chí: báo ΔF1 và khoảng tin cậy giữa hai seed cho L1 và L2; nếu dấu của L1 đổi giữa hai seed, bài phải hạ "ME không hơn
prompt" xuống "không ổn định theo seed".

### WP4. Reader thứ hai, Transformer thuần (điểm yếu b, và kiểm giả thuyết kiến trúc)

**Lý do.** Reader hiện tại (Qwen3.5-2B) là mô hình lai Gated DeltaNet xen attention. Công bố 2609.04434 báo rằng truy xuất chính xác
trên Qwen3.5 chỉ sống qua phần attention. Nếu bộ nhớ mềm yếu một phần vì kiến trúc reader, một reader Transformer thuần sẽ cho ME
và M khác đi. Một thí nghiệm trả lời hai câu: kết luận có đúng với reader khác không, và kiến trúc có đóng vai trò không.

**Thiết kế.**
- Một reader dày đặc cỡ 1,7-4B tiếng Việt chấp nhận được (ví dụ họ Qwen3 dày đặc; **cần kiểm tra** kích thước, giấy phép và chất
  lượng tiếng Việt trước khi chọn; không dùng LLM 27B). Chọn một reader, khóa trước khi chạy, không chọn lại theo kết quả.
- Làm lại: logit thầy cho reader mới, `stage1`, `stage2` (mem, prompt), mốc cứng, đánh giá select/gate/test, P1.
- Mức tùy chọn (chỉ khi dư giờ): reader lai cùng họ cỡ 4B (Qwen3.5-4B) để tách ảnh hưởng của cỡ khỏi kiến trúc.
- Việc mã: thêm cấu hình reader (`configs/readers/`), kiểm tương thích của bộ ghi bản sao L lớp với reader mới, bổ sung test.
  **Ước 1-3 ngày công**, chưa kiểm tra mã nên chưa chắc.

**Tài nguyên (cỡ 4B, giả định bước gấp ~2×; cỡ 1,7B gần như bằng cỡ 2B).**

| Phần | GPU-giờ (1,7B) | GPU-giờ (4B) |
| --- | ---: | ---: |
| Logit thầy | 1,3 | 2,5 |
| `stage1` + `stage2` | 3,4 | 6-7 |
| Mốc cứng | 0,5 | 1 |
| Đánh giá select/gate | 1,4 | 2,8 |
| Test + P1 | 3-5 | 5-8 |
| **Tổng** | **≈ 10** | **≈ 17-22** |

Bộ nhớ GPU: 80 GB đủ cho cả hai cỡ; riêng huấn luyện 4B cần kiểm batch.

### WP5. Cải tiến công thức huấn luyện bộ ghi (mức C; điểm yếu a)

**Lý do.** Hai công trình gần nhất chỉ ra cách làm giảm nút thắt: tự mã hóa mịn và trọng số theo mức phụ thuộc (2412.17483, tăng
mạnh ở bài nhớ chính xác), và chưng cất chỉ trên câu mà thầy trả lời đúng (2609.05152). Repo đã có logit thầy.

**Thiết kế.** Ba biến thể ở stage 2 mem, so với bản gốc trên cùng select/gate, một seed: (i) thêm loss tự mã hóa mịn, (ii) chưng
cất chỉ trên câu thầy đúng, (iii) đối chứng đơn giản: gộp trung bình (mean-pooling), trích dẫn trong 2611.16384 và 2609.05152, tôi
chưa mở trực tiếp bài gốc. Ba biến thể khóa trước; chọn bằng select; test và P1 đọc một lần. Kết quả nào cũng dùng được: nếu không biến
thể nào cứu được ME, kết luận âm càng mạnh; nếu có, cần đăng ký lại câu hỏi và nêu rõ đây là phần mở rộng.

**Tài nguyên.** Mỗi biến thể: huấn luyện 1,2-2 GPU-giờ, select/gate 0,7, P1 0,5-1 → **7-12 GPU-giờ** cho ba biến thể.
Việc mã: 3-5 ngày công.

### WP6. Đo độ trễ và VRAM theo độ dài (điểm yếu d)

**Thiết kế.** HF trên H100, batch 1 và batch tăng dần: thông lượng và độ trễ từng giai đoạn (viết bộ nhớ, tiền điền, sinh), VRAM
đỉnh, ở 16k, 32k, 64k, cho full, bm25, phobert, prompt, M, ME. Báo cáo thuần số đo. Nhắc: số đo hiện có
(506 ms cho 7,9k token) chỉ ở đoạn đơn.

**WP6b (tùy chọn, mức C).** Thử đường vLLM `--enable-prompt-embeds` với Qwen3.5-2B: gửi vài chục mẫu, so đáp án với pipeline HF.
Chưa xác minh được vLLM hỗ trợ trường này cho mô hình lai Qwen3.5; cần thử thật. Cần GPU từ Volta trở lên (1080 Ti không đủ,
cần kiểm tra thêm).

**Tài nguyên.** WP6: **0,5-1,5 GPU-giờ**. WP6b: 1-3 GPU-giờ và 1-2 ngày công.

### WP7. Phép đo judge và thống kê (điểm yếu e; không tốn GPU)

- Chấm lại ba lần trên P1/P2 để đo dao động trong cùng một judge (bài 2609.33044 báo judge ghim phiên bản vẫn dao động).
  Số bộ ba duy nhất 3.148 → thêm ≈ 6.300 lời gọi.
- Mẫu có nhãn tay phân tầng, 200-300 mục, để tính độ đồng thuận người-máy (kappa và phần trăm). **Cần người chấm**: ước 1-2 phút
  mỗi mục → 4-10 giờ cho một người; hai người thì gấp đôi. Cần chủ đề tài quyết định ai chấm.
- Bootstrap theo cụm bài đích (đã dùng) và khoảng tin cậy được hiệu chỉnh khi mẫu nhỏ (2609.35815, chỉ đọc tóm tắt).
- Gọi API: chỉ judge chính DeepSeek-V4.1-Flash, theo cache hiện có. Tổng lời gọi mới cho mức B ≈ 20.000-40.000 (WP1-WP4), phần lớn
  lời chấm ngắn.

### WP-P3. Đánh giá trên P3 (mức A; điểm yếu f)

**Điều kiện thực hiện:** chỉ khi P3 đã qua tiêu chí chấp nhận ở WP0c và băm đã khóa.
**Thiết kế.** Tập con trong-cùng-câu-hỏi: 150 câu × 3 độ dài × 3 vị trí = 1.350 ngữ cảnh. Điều kiện: bm25, bm25_x2, phobert, prompt-f2, prompt-f8, M, ME, full, đóng sách. Giả thuyết L1-L3
được **đăng ký lại** (không phải thay L1-L4 đã khóa) trong `PREREG_MORONG.md`, thêm hiệu ứng vị trí và độ dài đo **trong cùng câu hỏi** (hiệu ghép cặp theo câu rồi theo bài).
**Tài nguyên (ước, chưa đo H100 trên dữ liệu này).** 8 điều kiện không-full × 1.350 × 0,5-2 giây ≈ 1,5-6 GPU-giờ, `full` 0,75-2 giờ: **2-8 GPU-giờ**; mỗi hệ huấn luyện mới (seed hai, reader hai)
thêm 3 điều kiện ≈ 1-3 GPU-giờ. Chấm judge: ≈ 1.350 × 9 = 12.000 bộ ba.

### WP8. Bộ văn bản dài tự nhiên và sạch (mức C; điểm yếu về P1 tổng hợp, P2 nhiễm)

**Lý do.** P1 là dữ liệu ghép, P2 đã nhiễm một phần; chưa có kết luận nào trên văn bản dài tự nhiên và sạch. (P3 khắc phục độ khó của nhiễu nhưng vẫn là dữ liệu ghép; WP8 là bản tự nhiên.)

**Thiết kế.** Chọn nguồn văn bản dài tiếng Việt ngoài kho stage-1 và ngoài tiền huấn luyện nghi ngờ (cần nguồn có giấy phép và
mốc thời gian rõ; **chưa chọn nguồn**), sinh câu hỏi bằng LLM, người kiểm 300-500 câu, đo trùng 8-gram, khóa hash.

**Tài nguyên.** Sinh câu hỏi 1-3 GPU-giờ (mô hình sinh, không dùng làm reader; tham chiếu: lượt iCOMM 27B trước mất 3 giờ 17 phút
cho 19.983 đoạn), đánh giá các điều kiện 2-4 GPU-giờ, người kiểm 8-12 giờ (1,5 phút/câu), 1-2 tuần tìm và làm sạch nguồn.
**Tổng GPU: 3-7.** Rủi ro cao nhất về thời gian trong cả đề xuất.

## 4. Tổng hợp tài nguyên

| Gói | GPU-giờ (thấp-cao) | Mức A | Mức B | Mức C |
| --- | ---: | :---: | :---: | :---: |
| WP0 sửa dữ liệu (đóng sách, kiểm câu hỏi, dựng P3) | 0 H100 (1080 Ti, API, người) | giai đoạn 0 | giai đoạn 0 | giai đoạn 0 |
| WP1 đối chứng nội dung, phần trên P3 (P1 chạy ở giai đoạn 0) | 1-4 | x | x | x |
| WP2 ô bị bỏ, lặp bf16 | 3-7 | x | x | x |
| WP-P3 đánh giá trên P3 (hệ gốc) | 2-8 | x | x | x |
| WP6 độ trễ và VRAM (HF) | 0,5-1,5 | x | x | x |
| WP7 judge và thống kê | 0 (API + người) | x | x | x |
| WP3 seed thứ hai (kèm P1/P2) | 6-10 | | x | x |
| WP4 reader Transformer thuần | 10-22 | | x | x |
| WP-P3 cho hệ seed hai và reader hai | 2-6 | | x | x |
| WP5 công thức bộ ghi | 7-12 | | | x |
| WP6b thử vLLM | 1-3 | | | x |
| WP8 bộ văn bản dài tự nhiên | 3-7 | | | x |
| **Tổng H100** | | **6,5-20,5** | **24,5-58,5** | **35,5-80,5** |

Giai đoạn 0 (không H100, ước theo số đo pilot): 2 × 1080 Ti ≈ 9 giờ mỗi GPU cho WP1 trên P1; 2 × T4 ≈ 9 giờ mỗi T4 cho `full`/`bm25_x2` của P1 (một phiên Kaggle ≤ 12 giờ,
cần mở lại phiên và đồng bộ mã mới); đóng sách đã xong (≈ 48 phút trên 1080 Ti); WP0b-WP0c bằng API và CPU.

Phần cứng đề nghị: 2 × H100 80 GB cùng máy, bf16 (một H100 chạy được nhưng thời gian gần gấp đôi). Môi trường như lượt trước:
`transformers` 5.16.1, `flash-linear-attention`, `causal-conv1d` (build với `TORCH_CUDA_ARCH_LIST=9.0`), Python ≥ 3.10.
CPU ≥ 8 lõi, RAM ≥ 64 GB (P1 giữ bộ nhớ trên host), đĩa ≥ 150 GB (cache Hugging Face ≈ 30 GB, dữ liệu vài GB, mỗi checkpoint
≈ 1 GB, logit thầy của reader mới chưa biết kích thước), truy cập Hugging Face Hub để tải mô hình.
Con người: một người vận hành cụm theo runbook (như lượt trước), chủ đề tài viết mã và bài, và người chấm tay (WP7).

## 5. Lịch đề xuất (ngày lịch, đã tính gỡ lỗi và chờ hàng đợi; ước lượng)

| Tuần | Mức A | Thêm cho mức B | Thêm cho mức C |
| --- | --- | --- | --- |
| **Giai đoạn 0 (≈ 1 tuần, GPU miễn phí)** | Đóng sách; WP0b kiểm câu hỏi; WP0c dựng và khóa P3 (hoặc ghi "không đạt"); WP0d `PREREG_MORONG.md` rồi khóa băm; WP1 trên P1 (2 × 1080 Ti); `full`/`bm25_x2` ở P1 (2 × T4). **Cổng:** P3 đạt tiêu chí? WP1 cho tín hiệu? | Chọn reader thứ hai; thêm cấu hình và test (có thể xin H100 pha 1 ngay) | Chọn nguồn văn bản cho WP8 |
| Trước pha 2 | Commit sạch; chuyển checkpoint và dữ liệu lên cụm (Hub, cần bạn đồng ý) | | |
| 1 (H100) | Smoke (≈ 0,5 giờ, hiệu chỉnh thời gian), WP2, WP1 trên P3, đánh giá P3, WP6; WP7 song song | Logit thầy reader hai; `stage1` seed hai | Mã loss tự mã hóa |
| 2 | Viết số liệu vào bài | `stage2`, đánh giá, test, P1 và P3 cho seed hai và reader hai | WP5 huấn luyện |
| 3 | | Tổng hợp, kiểm tiêu chí, viết mục | WP5 đánh giá; WP6b |
| 4-5 | | | WP8; tổng hợp |

Hạn nộp ICISN 2027: `[CẦN THÔNG TIN]`. Tôi không biết ngày này; lịch trên phải được căn lại theo nó. EN giới hạn 6 trang + 1
trang trả phí, nên phần kết quả mới chỉ vừa một mục và một bảng, phần còn lại chuyển phụ lục hoặc bản VI.

## 6. Rủi ro và cách giảm

| Rủi ro | Biểu hiện | Giảm |
| --- | --- | --- |
| Reader thứ hai không tương thích với bộ ghi bản sao L lớp | Lỗi hoặc loss không giảm | Kiểm bằng smoke 50 câu trước; nếu hỏng, hạ về WP3 và nêu giới hạn |
| Hết bộ nhớ ở 64k hoặc `full` | OOM | Nhúng lười đã có; giảm `--max-batch-tokens` |
| Nút bị cordon hoặc gián đoạn (đã xảy ra lượt trước) | Job chết giữa chừng | Mọi lệnh có `--skip-existing`, lưu từng ô |
| P3 không đạt tiêu chí chấp nhận (nhiễu vẫn dễ) | BM25 hạng 1 > 55% sau khi dựng | Không chạy reader trên P3; bài ghi giới hạn của P1; chuyển sang WP8 hoặc nêu hướng tương lai |
| Kiểm tự đủ nghĩa loại nhiều câu (> 15%) | Tập con sạch nhỏ | Giữ phân tích chính trên toàn bộ; tập con sạch chỉ là độ nhạy; báo tỉ lệ |
| Dao động của judge | Số đổi giữa hai lần chấm | WP7 chấm ba lần, báo dao động |
| Kết quả lại âm | Không ai thắng | Vẫn là kết luận hợp lệ; bài đã định vị là phát hiện có kiểm soát |
| Kết quả đảo dấu giữa seed hoặc reader | L1 hoặc L2 đổi | Hạ tuyên bố xuống "không ổn định"; không chọn seed đẹp |
| Chi phí vượt ước lượng | GPU-giờ đo > 1,5× ước | Báo ngay, dừng và hỏi, theo ngưỡng của `G0_KIEM_KE.md` |

## 7. Việc phải quyết trước khi gửi đề xuất xin tài nguyên

1. Hạn nộp ICISN 2027.
2. Xin mức A, B hay C; và xin một pha hay hai pha (khuyến nghị hai pha).
3. Reader thứ hai là mô hình nào (cần kiểm tra giấy phép và tiếng Việt).
4. Ngưỡng tương đương cho H-C1, H-C2 và so seed (`[CẦN QUYẾT]`; khuyến nghị Δ = 3 điểm F1 và ACC-LLM theo số đo CI của P1; không đặt sau khi thấy số của WP1).
5. Có đẩy checkpoint và dữ liệu lên Hub không (hành động ra bên ngoài; cần bạn đồng ý).
6. Ai chấm tay 200-300 mục (WP7) và 100 câu kiểm tự đủ nghĩa (WP0b).
7. Có commit mã hiện tại không (cần commit sạch để chạy trên cụm; tôi không commit khi chưa được yêu cầu).
8. Có duyệt dựng P3 và tiêu chí chấp nhận (BM25 hạng 1 ≤ 55%, ≥ 85% câu tự đủ nghĩa) không; có thêm Wikipedia vi làm nguồn nhiễu không (bài đích vẫn sạch).
9. Có chấp nhận ghi lại ba hạn chế của P1 vào bài (không phát hiện chênh lệch > ≈ 3 điểm chứ không phải tương đương; vị trí và độ dài lẫn độ khó; P1 không làm truy hồi khó hơn) không.

## 8. Tài liệu tham khảo cho đề xuất

Đã đọc toàn văn: 2610.19373 (đối chứng nội dung của bộ nhớ nén), 2412.17483 (lỗi của gist và cách sửa), 2609.05152 (DEX-Comp),
2608.26175 (kiểm toán nén đa ngôn ngữ, không có tiếng Việt), 2610.26827 (KEEP-Bench), 2611.16384 (CoMem), 2609.04434 (kênh nhớ
của mô hình lai). Chỉ đọc tóm tắt: 2609.33044, 2609.35815, 2605.06939 (judge và thống kê). Các bài 2026 là preprint, chưa qua bình
duyệt; dùng làm gợi ý hướng làm, không dùng như chân lý.
