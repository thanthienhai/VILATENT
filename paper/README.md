# Bài ACIIDS 2027: ViLatent

Bản thảo *ViLatent: Soft Context Compression with Question-Aware Evidence for a Frozen Vietnamese Reader*, viết
theo mẫu Springer LNCS/LNAI một cột. Các mục không phụ thuộc kết quả (giới thiệu, công trình liên quan, phương pháp,
thiết lập thực nghiệm, giới hạn) đã viết xong. Mọi ô kết quả đang để trống, chờ các lượt chạy của `scripts/run_paper.sh`.

**Sửa đổi 25/10/2026** theo `vilatent_method_experiment_revision_checklist_aciids_2027.md` (mục A): trọng tâm đổi thành
"khi nào memory mềm đáng hơn văn bản cùng ngân sách"; thiết lập chính là ViQuAD-Long ở 4×; bộ ghi đa tỉ lệ (một
checkpoint cho mọi r và f); BM25 theo từ (pyvi) bỏ từ để hỏi; MEF thành cascade 3 bước có kiểm tra đáp án nằm trong
bằng chứng (AiE); thêm mốc PhoBERT, bộ ghi đóng băng, đo chi phí đầu cuối. Bảng phân tầng theo loại đáp án (Bảng 4
cũ) đã bỏ để vừa 15 trang.

## Hội nghị (kiểm ngày 23/10/2026; hạn nộp và số trang kiểm lại ngày 25/10/2026)

| Mục | Quy định | Nguồn |
| --- | --- | --- |
| Hạn nộp | **31/10/2026** (đã gia hạn), 23:59 AoE, qua EasyChair | [dates](https://aciids.pwr.edu.pl/2027/dates.html), [CFP EasyChair](https://easychair.org/cfp/ACIIDS2027) |
| Độ dài | 12–15 trang, **tính cả** hình, bảng và tài liệu tham khảo. Bài dài hơn có thể phải trả phí trang, tối đa tuyệt đối 25 trang | [submit](https://aciids.pwr.edu.pl/2027/submit.html) |
| Mẫu | Springer LNCS/LNAI, nộp PDF, tiếng Anh. Bản camera-ready cần nguồn LaTeX | như trên |
| Phản biện | Ít nhất 3 người. Trang web không ghi rõ là single-blind; bài giữ tên tác giả theo mẫu LNCS và theo hướng dẫn của chủ đề tài | như trên |
| Tác giả | Không được đổi danh sách tác giả sau khi phản biện bắt đầu | như trên |
| Trùng lặp | Mọi bài được quét trùng lặp, **kể cả tự đạo văn**: không chép văn bản từ bài LACC hay ViWord-C | như trên |
| Hội nghị | 5–7/4/2027, Bali, Indonesia; bài chính in LNAI, bài poster in CCIS | [trang chủ](https://aciids.pwr.edu.pl/2027/) |

Hai điểm khác với bản hướng dẫn dán vào cuộc trò chuyện ngày 23/10/2026: trang chính thức không nói mức 100 USD/trang
hay giới hạn 17 trang (chỉ nói "có thể tính phí", tối đa 25 trang), và không nói gì về ORCID.
Ngày 25/10/2026 trang dates vẫn ghi "31 October 2026 (extended)"; ngày Sep 30 hiện cạnh đó là hạn gốc trước khi gia
hạn. Thông báo kết quả và camera-ready: tháng 1/2027, chưa có ngày cụ thể.

**Chính sách AI của Springer Nature:** LLM không được đứng tên tác giả. Việc dùng LLM phải được ghi trong mục Methods,
hoặc một mục phù hợp nếu bài không có mục Methods; riêng việc dùng AI để biên tập câu chữ ("AI assisted copy editing")
thì không cần khai ([chính sách](https://www.springer.com/us/editorial-policies/artificial-intelligence--ai-/25428500)).
Bản thảo này do Claude viết nháp từ tài liệu của đề tài, nên chủ đề tài cần quyết định cách khai trước khi nộp.

## Cấu trúc

```
main.tex              preamble, tác giả, thứ tự các mục, macro placeholder
sections/             abstract, introduction, related, method, setup, results, conclusion (gồm Limitations)
figures/overview.tex  Hình 1 (TikZ): ViLatent-ME và cascade MEF
figures/curves.tex    Hình 2 (F1 theo tỉ lệ nén) và Hình 3 (hai đường dự phòng): hai ô giữ chỗ cạnh nhau, vẽ bằng pgfplots khi có kết quả
references.bib        tài liệu tham khảo đã xác minh (mỗi mục kèm nguồn trong notes/references_verified.md)
notes/                nhật ký xác minh tài liệu và số liệu trích dẫn
llncs.cls, splncs04.bst   Springer LNCS v2.24 (29/01/2024), chép từ bài SoICT 2026, không phụ thuộc bản cài TeX
check_pages.py        đếm trang (12–15) và số placeholder còn lại
```

## Biên dịch

```bash
pdflatex main && bibtex main && pdflatex main && pdflatex main
python check_pages.py
```

Đã thử với MiKTeX trên Windows. Trên Overleaf: tải cả thư mục lên, chọn `main.tex` và trình biên dịch pdfLaTeX.
Chữ tiếng Việt (câu chỉ dẫn ở chú thích chân trang, tên tác giả) dùng mã hoá T5 của `vntex`; gói này phải nạp với
tuỳ chọn `nocaptions`, nếu không chú thích sẽ thành "Hình", "Bảng".

## Placeholder

| Macro | Hiển thị | Ý nghĩa |
| --- | --- | --- |
| `\tbd` | `??.?` màu đỏ | kết quả chưa có |
| `\prelim{x}` | `x` màu xanh | số đã đo nhưng phải đo lại trên đúng thiết lập trước khi dùng |
| `\todo{...}` | ghi chú đỏ | việc cho tác giả |

Đặt `\draftfalse` trong `main.tex` trước khi nộp: khi đó cả ba macro gây lỗi biên dịch, nên bài không thể nộp khi
còn sót placeholder. `check_pages.py` in số placeholder còn lại.

## Phạm vi của bài

Chọn ngày 23/10/2026, sửa ngày 25/10/2026 theo checklist (mục A1–A2, A13).

| Trong bài | Trong docs/VILATENT.md | Đo bằng |
| --- | --- | --- |
| RQ1: ME so với nén cứng trên ViQuAD-Long và đoạn đơn ở 4×/8×/16×; phần thắng đến từ nội dung memory | H1 | Bảng 2 (Long 4×, thêm cột đoạn đơn), Hình 2, các đối chứng |
| RQ2: cái giá của việc ghi mù câu hỏi (chỉ r = 4) | H6 | ViLatent-Q (tên trong code: W5) so với M và ME; Mục 5.3 |
| RQ3: cascade cần bao nhiêu token để giữ 95% F1 toàn văn | H7 | Hình 3, ECE; Mục 5.4 |
| Chi phí đầu cuối, điểm hoà vốn | (mới) | Bảng 4 |

Quy tắc quyết định (chốt trước B12): tập gate, ViQuAD-Long 4×, ME ở f*(Long, 4), seed 0; ba điều kiện cũ; "mốc cứng
tốt nhất" gồm cả PhoBERT. Đoạn đơn và 8×/16× chỉ là phân tích mô tả. Không có trong bài: H2, H3, H5, reader 9B, phân
tầng theo loại đáp án (đã bỏ để vừa trang).

## Số liệu lấy từ đâu

Mọi số trong bảng phải lấy từ file kết quả từng câu, không chép tay từ log.

Mọi đường dẫn dưới đây nằm trong `results/paper/` (sinh bởi `scripts/run_paper.sh`). Tên phương pháp: `full`, `none`,
`truncation`, `lead`, `llmlingua2`, `bm25`, `phobert`, `bm25_x2`, `vilatent_m`, `vilatent_me_f{f}`,
`vilatent_me_f{f}_swap`, `vilatent_q`, `prompt_bm25_f{f}`, `frozen_me_f{f}`; thêm `_s1` cho seed thứ hai.

| Chỗ trong bài | File |
| --- | --- |
| Bảng 2, cột Gate F1 | `gate/long/<method>_r4.summary.json` |
| Bảng 2, cột Test F1/EM, Δ, CI, Unread. | `test/long/<method>_r4.summary.json`, `test/long/report_r4.json` (CI theo bài là chính, theo đoạn là phụ) |
| Bảng 2, cột Single test F1 | `test/single/<method>_r4.summary.json` |
| f*, τ (mọi chỗ) | `select/choices.json` (f* theo select F1 cho từng setting và r; τ của cascade) |
| Quy tắc quyết định (Mục 5.1) | `gate/decision.json` |
| Hình 2 và 3 | `figures/curves.tex` do bước `figures` của `run_paper.sh` vẽ (`scripts/paper_figures.py`) từ `test/long/<method>_r{4,8,16}.summary.json` (ME ở f* của từng r) và `test/long/cascade_curve_r4.json`; không sửa tay |
| F1 theo vị trí đoạn chứa đáp án (Mục 5.1) | `test/long/positions_r4.json` |
| Bảng 3 | `select/long/vilatent_me_f{f}_r4.summary.json` (`f1`, `text_share`), `gate/long/vilatent_me_f{f}_r4.summary.json` và `..._swap_r4.summary.json`; cột "Ans. in E" = `present` của `me_f{f}_r4` cho `viquad_long_select.jsonl` trong `select/answer_in_evidence.json` |
| Mục 5.3 (RQ2) | `test/{long,single}/report_r4.json`, cặp `vilatent_q - vilatent_m` |
| Hình 3, Mục 5.4 (cascade, ECE) | `test/long/cascade_r4.json`, `test/long/cascade_curve_r4.json` |
| Bảng 4 | `test/latency_long.json`: `writer_ms_per_doc`, `mean_ms` (`*_select`, `*_ttft`, `*_read`), `per_question_ms`, `break_even_vs_full` (N*); `test/latency_single.json` cho câu về đoạn đơn |
| Thống kê ViQuAD-Long (Mục 4.1, đã điền) | `data/tasks/viquad_long_stats.json` (`scripts/build_long.py`) |

## Việc còn lại trước khi nộp

1. **Chạy thực nghiệm và test.** Theo `scripts/run_paper.sh` (lịch B1–B17 của checklist): một lượt stage 1, 4–5 lượt
   stage 2, đánh giá gate và select, rồi test **một lần** ngày 30/10. Số trong bài chỉ lấy từ H100 (bf16); T4 chỉ để gỡ
   lỗi. Còn phải điền: k1, b của BM25 sau khi dò lại (Mục 4.3), số seed (Mục 4.2), giờ GPU.
2. **Tác giả.** Tác giả đầu: Ngoc Thien Than, ORCID 0009-0007-7623-2413; `\authorrunning` là "N. T. Than et al.".
   Tên viết tên trước, họ sau, đúng như hồ sơ ORCID, để Springer lập chỉ mục họ là "Than" (quyết định 23/10/2026).
   Còn thiếu tên, đơn vị, email và ORCID của đồng tác giả; viết theo cùng thứ tự với hồ sơ ORCID của từng người.
3. **Kết quả.** Điền các `\tbd`, viết đoạn tóm tắt kết quả ở cuối Introduction, câu kết luận và các câu kết quả của
   Abstract. Bài có hai kịch bản:
   - *A, quy tắc đạt:* nhấn mạnh phần thắng vẫn còn sau các đối chứng và giữ được trên test.
   - *B, quy tắc không đạt:* nói rõ điều kiện nào không đạt; đường F1 theo tỉ lệ nén (Hình 2) vẫn là đóng góp chính.
     Nếu ME xấp xỉ "prompt học được + BM25" thì phần hơn so với các mốc zero-shot là do học kiểu đáp án; khi đó viết
     lại Abstract và Conclusion thành một kết quả có kiểm soát.
4. **Câu về điểm giao cắt ở Mục 5.1** (`\todo`): viết từ Hình 2 khi có số. Trang 15 hiện chỉ còn khoảng 4 dòng
   trống; sau khi điền số, chạy lại `check_pages.py`.
5. **Tài liệu tham khảo.** 44 mục trong `references.bib` đã xác minh (42 mục ngày 23/10/2026; PhoBERT và Memorilla
   thêm ngày 25/10/2026; nhật ký ở `notes/references_verified.md`); bài đang trích 31 mục. Ngày 25/10/2026, để vừa
   trang, bỏ trích Selective Context, RECOMP, nghiên cứu gist (Deng), Cartridges++ và Petrov (các mục vẫn còn trong
   bib). Văn bản đã sửa theo kết quả kiểm: tác giả đầu của
   LatentPress là Xu (khoá `xu2026latentpress`), AdaMem chênh 3,9 (NQ) và 5,7 (HotpotQA) điểm, Łajewska và cộng sự
   chỉ *đề xuất* giữ số và tên dạng token cứng. Để vừa trang, bài đã bỏ trích Transformers, AdamW, Hinton, PISCO,
   Sufficient Context, MLQA, Belebele và VietNews (các mục vẫn còn trong file bib). Còn phải quyết:
   - Efron và Tibshirani: bản ghi DOI của CRC ghi năm 1994; bản Springer 1993 có DOI hỏng. Bib đang dùng 1994.
   - SeDeM (EMNLP 2026) và LensVLM (NeurIPS 2026) mới ở trạng thái "accepted": kiểm lại khi có kỷ yếu.
   - Robertson và Zaragoza: Crossref ghi tập 4, số 1–2, tr. 1–174; xem lại trên trang nhà xuất bản.
6. **Bài LACC.** Nếu bài LACC đã đăng hoặc đang phản biện và được phép trích, thêm một câu trích ở Introduction (chỗ
   có ghi chú `TODO(authors)`), viết lại bằng lời mới.
7. **Khai báo dùng AI** theo chính sách Springer Nature ở trên.
8. **Trước khi nộp:** `\draftfalse`, biên dịch, `python check_pages.py` phải trả về 0, rồi xem lại PDF (font nhúng
   đủ, không có `??` của tham chiếu chéo).
