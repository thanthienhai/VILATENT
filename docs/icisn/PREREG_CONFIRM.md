# PREREG_CONFIRM — đăng ký trước pha xác nhận trên XQuAD-vi

Khóa ngày 2026-11-08 (người dùng đồng ý bước này cùng ngày), **trước** mọi lượt đọc của reader trên XQuAD-vi và
**trước** mọi lượt đọc Sum, Sum+E, bge-m3 và prompt-ở-f-tốt-nhất trên ViQuAD test. SHA-256 của file này ghi trong
`docs/icisn/PREREG_CONFIRM.sha256` (tính trên đúng nội dung file này). Mọi sai khác sau khóa phải ghi vào báo cáo với nhãn "lệch khỏi đăng ký".

## 0. Bối cảnh và những điều đã biết trước khi khóa

- RQ1 gốc (quy tắc đăng ký trước: ME hơn prompt học được ở Long 4×) **không đạt**: ME hòa prompt (+0,43 F1, CI [−1,43; +2,18]). Bài **không** được viết lại để che điều đó.
- Pha này là **xác nhận** các giả thuyết mới trên dữ liệu chưa dùng để chọn gì: XQuAD-vi (1 190 câu, 48 bài, 240 đoạn).
- Các giả thuyết H-R1, H-R2 được hình thành **sau** khi thấy kết quả ViQuAD test (hậu nghiệm, đã nêu trong bài). Pha này là lần kiểm đầu tiên trên dữ liệu độc lập; ViQuAD test **không** được tính là xác nhận cho chúng.
- Điều đã quan sát trước khi khóa (không dùng XQuAD-vi): ở ViQuAD test, Long 4×, ME−prompt +0,43; ME ≥ M; prompt ở f=2 kém hơn prompt ở f lớn hơn trên select đoạn đơn (`CHUAN_BI.md` §2.5).
- Chưa có lượt đọc reader nào trên XQuAD-vi tại thời điểm khóa. Reader mới chỉ chạy trên select (ViQuAD) và 200 câu test đầu (kiểm tái lập G0).

## 1. Dữ liệu, mốc và điều kiện được khóa

**Dữ liệu:** `data/icisn/xquad_vi_single.jsonl` (đoạn đơn) và `xquad_vi_long.jsonl` (ghép theo bài), SHA-256 trong `data/icisn/SHA256SUMS.txt`.
**Reader:** Qwen/Qwen3.5-2B, `configs/readers/qwen3.5-2b.json`, **fp16** trên GTX 1080 Ti (T4 nếu 1080 Ti không dùng được; mỗi file dự đoán ghi thiết bị). **Writer:** `runs/paper/stage2_mem/best.pt` (ME, M) và `stage2_prompt/best.pt` (prompt), SHA trong `CHECKPOINTS_SHA256.txt`. Không huấn luyện lại, không chọn lại siêu tham số.
**Tỉ lệ nén chính:** 4×. Không chạy 8×/16× cho XQuAD-vi.

**Điều kiện đọc trên XQuAD-vi (mỗi điều kiện ở cả hai thiết lập: đoạn đơn, Long):**

| Tên | Nội dung |
|---|---|
| full | toàn văn (nếu không vừa bộ nhớ ở một bài Long: ghi nhận thiếu, không bỏ chọn lọc) |
| none | không có ngữ cảnh |
| truncation, lead | cắt đầu / lead tới ngân sách k(4) |
| bm25 | BM25 chọn câu, ngân sách k(4) |
| bm25_x2 | BM25 chọn câu, ngân sách 2·k(4) |
| phobert | PhoBERT chọn câu, ngân sách k(4) |
| llmlingua2 | LLMLingua-2, ngân sách k(4) |
| bgem3 | bge-m3 chọn câu (`BAAI/bge-m3` bản `5617a9f6…`), ngân sách k(4) |
| M | `vilatent_m` (f=1) |
| ME | `vilatent_me_f2` (f=2; f* của cả hai thiết lập ở 4× trong bài chính) |
| prompt-f2 | `prompt_bm25_f2` |
| prompt-fbest | prompt ở f tốt nhất (khóa ở `results/icisn/select/prompt_f_choice.json`: f=8 ở 4×) |
| Sum | `sum_v1` (biến thể v1; `results/icisn/select/sum_choice.json`) |
| Sum+E | `sumE_v1_f2` (f=2, cùng câu BM25 như ME) |
| router | không chạy reader mới: "ME nếu cờ aie của ME bằng 1, ngược lại M" (`scripts/paper_numbers.py`, định nghĩa dòng "router"). Cờ aie = đáp án dự đoán của ME xuất hiện nguyên văn trong bằng chứng BM25 của ME. Router là hậu nghiệm ở bài chính; ở đây được **đặt trước** cho pha xác nhận. |

Tóm tắt Sum, prompt tóm tắt, quyết định chọn v1 và f tốt nhất của prompt: SHA-256 trong `data/icisn/SHA256SUMS.txt`, **không đổi**.

**Bổ sung trên ViQuAD test** (gắn nhãn `[test, bổ sung]`, **không** có quyết định xác nhận, chỉ ước lượng và CI): Sum, Sum+E, bge-m3 ở 6 ô (đoạn đơn, Long) × (4×, 8×, 16×); prompt-fbest ở đoạn đơn (f=8@4×, f=4@8×). Mục đích: xem các mốc mới có đổi bức tranh chính không. So với các dự đoán H100 (bf16) có sẵn là so khác thiết bị; phải ghi chú.

## 2. Giả thuyết xác nhận (mọi thứ ở 4×, XQuAD-vi, mỗi thiết lập riêng)

Ký hiệu: giá trị theo câu hỏi, F1 tính theo `vilatent/metrics.py` (theo âm tiết, như bài chính); ACC-LLM theo `PREREG_JUDGE.md`. Một câu hỏi = một đơn vị, **gom theo bài** (khóa `title`) cho bootstrap.

- **H-R1 (memory bù ở nơi bộ chọn câu hụt đáp án).** Tương tác I = [mean(ME − prompt-f2) trên nhóm Out] − [mean(ME − prompt-f2) trên nhóm In] > 0. In/Out theo `scripts/gold_split.py` (đáp án vàng có/không nguyên văn trong các câu BM25 mà ME nhận, f=2). Một phía.
  *Prompt đối chứng của H-R1 là prompt-f2 (cùng bằng chứng với ME).* Phiên bản với prompt-fbest là **thứ yếu, thăm dò**, không vào họ Holm.
- **H-R2a.** router − M > 0 (một phía).
- **H-R2b (không kém).** router − bm25_x2 > −δ, với δ = **2,0 điểm F1** và δ = **0,02 ACC-LLM** (một phía; H0: hiệu ≤ −δ).
- **H-S1.** M so với Sum (hai phía).
- **H-S2.** ME so với Sum+E (hai phía).

**Kiểm định:** bootstrap ghép cặp theo bài, 10 000 lần, seed 0 (`vilatent.stats.paired_test`); p một phía từ phân phối bootstrap dịch về H0 (hàm sẵn có). Tương tác H-R1: cùng cách, dùng bootstrap chọn lại bài (như `gold_split.interaction`) với phân phối dịch về 0. Không kiểm kích thước hiệu ứng nào khác. Không-kém: kiểm `paired_test(router + δ, bm25_x2)` một phía. p hai phía = min(1, 2·min(p(a>b), p(b>a))).

**Họ Holm:** 10 kiểm định = 5 giả thuyết × 2 thiết lập, một họ cho F1 và **một họ riêng** cho ACC-LLM (người chấm chính), α = 0,05 (`vilatent.stats.holm`).

**Tiêu chí "đạt":** một giả thuyết ở một thiết lập **đạt** chỉ khi **cả** F1 **và** ACC-LLM (người chấm chính) đều có p hiệu chỉnh Holm < 0,05 theo đúng chiều đã nêu (với H-S1/H-S2: khác có ý nghĩa; chiều báo riêng). Nếu chỉ một độ đo qua thì ghi "một phần" (kèm độ đo nào), không ghi "đạt". EM và ACC-LLM của người chấm phụ được báo nhưng **không** quyết định. Báo thêm MDE (80% power, `vilatent.stats.mde`) cho mọi kiểm định; kết quả không có ý nghĩa mà |hiệu| < MDE ghi là "không đủ lực để kết luận", không ghi là "tương đương".

**Diễn giải đã nêu trước cho từng kết quả:**
- H-R1 đạt ở cả hai thiết lập: bài kết luận memory bù ở nơi bộ chọn hụt (cơ chế), vẫn kèm nhận xét ME không hơn prompt ở Long 4× (RQ1 gốc). Đạt một thiết lập: kết luận giới hạn ở thiết lập đó. Không đạt: bỏ H-R1 khỏi các đóng góp, chỉ báo như một quan sát ViQuAD không lặp lại.
- H-R2a/b: router chỉ được gọi là "đạt" khi cả hai (R2a và R2b) cùng qua ở thiết lập đó; ngược lại router là quan sát thăm dò.
- H-S1: nếu Sum ≥ M (không có khác biệt hoặc Sum cao hơn có ý nghĩa), bài **phải nêu rằng văn bản tóm tắt bằng hoặc hơn memory mềm** ở cùng ngân sách (nêu cả điểm yếu "Sum chưa lấp đầy ngân sách ở Long", `CHUAN_BI.md` §2.1). M cao hơn Sum có ý nghĩa: nêu là "memory hơn tóm tắt văn bản cùng ngân sách (trên XQuAD-vi)".
- H-S2: tương tự cho ME so với Sum+E.
- Các kết luận về văn bản rất dài (hàng nghìn token) **không** rút từ XQuAD-vi-Long (bài chỉ ~1 000 token trung vị); chỉ ViQuAD-Long làm điều đó.

## 3. Phân tích độ nhạy được khóa (không vào họ Holm)

1. **Loại đoạn trùng corpus giai đoạn 1:** loại mọi câu hỏi thuộc 6 đoạn trùng ≥50% 8-gram từ với `data/corpus/docs.jsonl` (quy tắc và danh sách tiền tố `xquad-AAAA-PPPP` trong `results/icisn/g0/xquad_overlap_ids.json`, SHA-256 ở mục 6; ở Long loại theo đoạn của câu hỏi `passage_index`, bài vẫn đọc nguyên). Báo lại mọi H ở 4× trên phần còn lại.
2. **Tính lại H-R1 với prompt-fbest** (thứ yếu).
3. **Tính lại mọi giả thuyết trên ViQuAD test 4×** (`[test, bổ sung]`, không phải xác nhận).

## 4. Điều trung thực phải ghi trong bài (đe dọa tính hợp lệ, định trước)

- fp16 (1080 Ti/T4) so với bf16 (H100) ở các dự đoán cũ: G0 cho |ΔF1| ≤ 0,78 trên 200 câu. Trên XQuAD-vi mọi điều kiện cùng thiết bị, nên phép so ghép cặp không bị lẫn thiết bị; trên ViQuAD test bổ sung thì có lẫn.
- Một hạt giống (seed) huấn luyện; không đo phương sai giữa các lần huấn luyện.
- Người chấm (DeepSeek-V4.1-Flash) và reader thuộc hai họ khác nhau nhưng người chấm cùng họ với người viết tóm tắt Sum; người chấm phụ Qwen3.8-27B cùng họ với reader. Hai điều này có thể thiên lệch.
- Tóm tắt Sum do mô hình lớn hơn (DeepSeek) viết: Sum dùng thêm tri thức/năng lực ngoài hệ nén; không nói đây là so sánh "cùng tài nguyên".
- XQuAD-vi là bản dịch của SQuAD v1.1: phong cách khác ViQuAD; 6 đoạn trùng corpus giai đoạn 1 (mục 3.1); không đo độ dài rất dài.
- ACC-LLM có κ với nhãn tham chiếu trong `KET_QUA_JUDGE.md`; nếu κ < 0,60 thì ACC-LLM không được dùng để tuyên bố "đạt" (như `PREREG_JUDGE.md` §5).
- Không có tuyên bố tiết kiệm thời gian/chi phí.

## 5. Thứ tự và cách chạy

1. Khóa file này (băm) → mới chạy reader trên XQuAD-vi và các lượt bổ sung trên ViQuAD test.
2. Mọi lượt đọc chạy nền với `--skip-existing` (tiếp tục được), log ở `logs/`. Báo lại nếu tổng giờ vượt 1,5 × ước lượng.
3. Chấm toàn bộ dự đoán XQuAD-vi 4× (và ViQuAD test mới) bằng người chấm chính, prompt đã khóa; người chấm phụ chạy trên các điều kiện xuất hiện trong giả thuyết (M, ME, prompt-f2, bm25_x2, Sum, Sum+E) ở XQuAD-vi 4×, báo kèm, không quyết định.
4. Một script duy nhất tạo số liệu: `scripts/icisn/confirm_numbers.py` → `paper_icisn/numbers_icisn.tex` và `docs/icisn/KET_QUA_XAC_NHAN.md`.

## 6. Các mục được khóa kèm SHA-256 (tại thời điểm khóa)

Ghi trong `docs/icisn/PREREG_CONFIRM.sha256`: file này; `data/icisn/SHA256SUMS.txt`; `results/icisn/g0/xquad_overlap_ids.json`; `docs/icisn/PREREG_JUDGE.md`; `docs/icisn/judge_prompt.json`.
