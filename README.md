# ViLatent

Mã nguồn nghiên cứu cho đề tài *ViLatent: nén mềm ngữ cảnh cho reader tiếng Việt đóng băng*. Bộ ghi (bản sao L lớp
đáy của reader, gộp trung bình mỗi ρ token, RMSNorm và adapter d×d) nén ngữ cảnh thành k memory vector. Reader đóng
băng đọc các vector này qua `inputs_embeds`.

- [`docs/VILATENT.md`](docs/VILATENT.md): đề xuất nghiên cứu (giả thuyết H1–H7, kiến trúc W0, cổng G0–G3). Các chú
  thích "docs/VILATENT.md §…" trong mã trỏ tới tài liệu này.
- [`docs/RUN_PAPER.md`](docs/RUN_PAPER.md): hướng dẫn chạy thực nghiệm của bài ACIIDS 2027 trên máy GPU (thay cho
  `RUN_G0_G1.md` từ 25/10/2026).
- [`paper/`](paper/README.md): bản thảo nộp ACIIDS 2027 (Springer LNCS).
- [`vilatent_method_experiment_revision_checklist_aciids_2027.md`](vilatent_method_experiment_revision_checklist_aciids_2027.md):
  checklist sửa phương pháp và thực nghiệm ngày 25/10/2026 (bộ ghi đa tỉ lệ, ViQuAD-Long, MEF ba tầng).
- [`docs/ViLatent_g1.html`](docs/ViLatent_g1.html): sơ đồ huấn luyện và đánh giá G1 (bản lưu ngày 16/10/2026, trước
  các sửa đổi 22/10 và 25/10/2026).

> Trạng thái (25/10/2026): mã đã sẵn sàng cho thực nghiệm của bài ACIIDS 2027 (Qwen3.5-2B; ViQuAD đoạn đơn và
> ViQuAD-Long; 4×, 8×, 16×), **chưa có kết quả thực nghiệm**. Hệ chính là ViLatent-ME: bộ ghi đa tỉ lệ không thấy câu
> hỏi (memory ghi một lần) cộng câu gốc chọn theo câu hỏi trong cùng ngân sách, kèm MEF (dự phòng ba tầng: ME, BM25
> với ngân sách 2k, toàn văn) và nhánh chẩn đoán ViLatent-Q (tên trong mã: W5). Luồng G1 cũ (mỗi tỉ lệ một bộ ghi,
> `run_g1.sh`) đã được thay; xem lịch sử git nếu cần.

## Cấu trúc

```
vilatent/            thư viện
  text.py            chuẩn hoá NFC, tách câu bằng regex (có danh sách viết tắt), âm tiết, từ (pyvi), từ để hỏi
  budget.py          chia khúc theo câu (≤ 512 token reader), ngân sách k = Σ ceil(n_i / r)  — dùng chung mọi nơi
  template.py        template chat cố định của từng reader (tắt thinking), ghép prompt theo đoạn token
  reader.py          nạp reader đóng băng, giải mã greedy từ inputs_embeds (một đường cho mọi phương pháp)
  writer.py          bộ ghi W0 đa tỉ lệ: L lớp đáy + token mồi bị bỏ + gộp ρ token (ρ theo từng khúc) + RMSNorm·s
                     + adapter (khởi tạo I); W5: câu hỏi đặt giữa token mồi và khúc; tuỳ chọn đóng băng các lớp;
                     PromptWriter cho đối chứng prompt học được
  model.py           ViLatent: mỗi mẫu đọc ở (r, f), f = 1 là M, f ≥ 2 là ME; encode_memory, memory_prompt, loss;
                     lưu/nạp checkpoint (kèm các cặp (r, f) đã huấn luyện)
  fallback.py        ViLatent-MEF: dự phòng ba tầng (ME, BM25 2k, toàn văn) với kiểm tra đáp án nằm trong bằng
                     chứng, dự phòng chỉ theo log-prob, đường đánh đổi, chọn τ, ECE
  selector.py        bộ chọn câu PhoBERT (cross-encoder, nhãn "câu chứa đáp án"): huấn luyện và chấm điểm
  losses.py          CE + λ·KL(thầy ‖ trò) trên top-20 của thầy + ô "còn lại"
  teacher.py         tính trước top-20 log-prob của thầy (reader đọc ngữ cảnh đầy đủ)
  train.py           vòng huấn luyện giai đoạn 1 và 2: bốc (r, f) cho từng mẫu, trộn mẫu nhiều đoạn, chọn
                     checkpoint theo loss dev
  baselines.py       full, none, truncation, lead (câu trọn vẹn), bm25 (từ pyvi, bỏ từ để hỏi), phobert, llmlingua2;
                     pack_sentences dùng chung cho BM25, PhoBERT và câu gốc của ME
  evaluate.py        đánh giá QA cho nén mềm và nén cứng trên cùng ngân sách (lô sinh giới hạn theo số token)
  metrics.py         F1/EM trên âm tiết, câu trả lời không đọc được, lặp từ
  stats.py           bootstrap cặp theo seed × cụm (bài hoặc đoạn), MDE, Holm
  leak.py            chỉ mục n-gram 13 âm tiết chống rò rỉ
  data.py            định dạng JSONL, sidecar provenance <file>.meta.json, ViQuAD-Long, cửa sổ nhiều đoạn
scripts/             prepare_viquad (tách theo bài), prepare_external_eval (MLQA, Belebele, VietNews để lọc rò
                     rỉ), build_long (ViQuAD-Long, cửa sổ nhiều đoạn), build_corpus, make_pairs, leak_filter,
                     generate_qa, filter_qa, render_template, g0_check, tune_bm25, train_selector,
                     answer_in_evidence, precompute_teacher, train, evaluate, choose_f (f* theo F1 select),
                     cascade_report (MEF, τ, ECE), paper_report (bảng, quy tắc quyết định), position_report,
                     latency, paper_figures; run_paper.sh nối tất cả, smoke_paper.sh chạy thử quy mô nhỏ
configs/readers/     template đã render của từng reader (commit vào git; checkpoint và logit thầy gắn với hash của nó)
configs/paper/       giai đoạn 1 đa tỉ lệ; giai đoạn 2 cho ME/M, đối chứng prompt, bộ ghi đóng băng, ViLatent-Q
configs/bm25.json    k1, b, đơn vị của BM25, dò trên ViQuAD select (mốc BM25 và câu gốc của ME); bản trong git là
                     bản âm tiết của G1, bước tune_bm25 ghi đè bằng bản trên từ
tests/               test CPU với Qwen3.5 ngẫu nhiên tí hon, không cần GPU hay tải mô hình
```

Dữ liệu (`data/`), checkpoint (`runs/`) và kết quả (`results/`) không đưa lên git.

## Cài đặt

Python ≥ 3.10. Mỗi nhóm phụ thuộc là một extra; `pyvi` (tách từ tiếng Việt) nằm trong phần lõi:

```bash
pip install -e ".[dev]"                          # lõi + test (CPU)
pip install -e ".[model,data,baselines,teacher]" # reader, dữ liệu, LLMLingua-2, LLM thầy
pip install -e ".[kernels]"                      # kernel Gated DeltaNet (Linux + CUDA), cần cho backward nhanh
pytest -q                                        # 58 test, chạy trên CPU
```

Qwen3.5 cần transformers có model type `qwen3_5` (đã thử với 5.12 và 5.16). Thiếu `flash-linear-attention` và
`causal-conv1d` thì transformers vẫn chạy DeltaNet bằng torch thuần nhưng chậm; `scripts/g0_check.py` báo cáo việc
này. Trên Windows, đặt `PYTHONIOENCODING=utf-8` để in được tiếng Việt.

## Chạy thực nghiệm của bài báo

```bash
bash scripts/smoke_paper.sh                                     # thử cả luồng ở quy mô nhỏ (Kaggle 2× T4), trong bản sao riêng
bash scripts/run_paper.sh data template g0                      # dữ liệu, ViQuAD-Long, template, kiểm tra kernel
bash scripts/run_paper.sh tune_bm25 selector aie                # T4 đủ: BM25 trên từ, bộ chọn PhoBERT
bash scripts/run_paper.sh teacher stage1 stage2                 # H100: logit thầy, một lượt giai đoạn 1, ba lượt giai đoạn 2
bash scripts/run_paper.sh baselines                             # H100: mốc cứng ở 4×/8×/16× (song song với huấn luyện)
bash scripts/run_paper.sh eval_select choose eval_gate decide   # H100: f*, τ trên select; quy tắc quyết định trên gate
bash scripts/run_paper.sh test figures                          # một lần, sau decide
bash scripts/run_paper.sh qa_download qa_filter                 # QA sinh tự động (không thuộc bài báo)
```

Trên GPU không có bf16 (T4), đặt `DTYPE=float16`. Số liệu trong bài chỉ lấy từ H100 (bf16); T4 chỉ để gỡ lỗi.
Chi tiết từng bước, lịch chạy theo mã việc B1–B17 và các file cần gửi lại nằm trong
[`docs/RUN_PAPER.md`](docs/RUN_PAPER.md).

## Các quyết định cài đặt ngoài tài liệu

Những điểm `docs/VILATENT.md` chưa quy định, đã thống nhất với chủ đề tài trước khi viết mã:

| Điểm | Quyết định |
| --- | --- |
| Token đầu khúc | Chèn token mồi (`<|endoftext|>` với Qwen, BOS với Vistral) vào đầu mỗi khúc rồi bỏ trạng thái ẩn của nó; mọi token nội dung đều được gộp |
| Bộ ghi và khúc | Mỗi khúc chạy độc lập qua bộ ghi |
| Ngân sách | k = Σ ceil(n_i / r), nhóm cuối của khúc có thể ít hơn r token; ⟨mem⟩ ⟨/mem⟩ không tính; mốc nén cứng nhận đúng k token reader |
| Truncation, Lead-k, BM25 | Truncation giữ k token đầu. Lead-k chỉ giữ câu trọn vẹn, không lấp phần còn lại (nếu lấp thì trùng với Truncation). BM25 chỉ giữ trọn câu có điểm > 0 (có từ chung với câu hỏi), rồi lấp phần còn lại bằng đầu của câu điểm cao nhất chưa vừa, cắt theo token của reader như Truncation (quyết định 19/10/2026: câu điểm 0 chiếm mất ngân sách của câu chứa đáp án; cắt theo từ bỏ trọn cả cụm như "1010,"). Từ 25/10/2026 BM25 tính trên từ tách bằng pyvi, viết thường, bỏ từ để hỏi khỏi truy vấn, k1 và b dò lại trên select |
| ⟨mem⟩ ⟨/mem⟩ | Khởi tạo bằng embedding trung bình của token "«" và "»" |
| Kiểu số | Trọng số huấn luyện fp32, tính bằng autocast bf16; reader bf16 |
| Giai đoạn 1 | Wikipedia + BKAINewsCorpus 50 : 50; A dài 128–1.024 token (cắt ở cuối câu), B là 128 token tiếp theo; qua chat template ("Viết tiếp đoạn văn sau") |
| Prompt | Không dùng system prompt cho mọi reader; chỉ dẫn QA lấy nguyên văn từ ViWord-C |
| QA sinh tự động | Đáp án phải là span nguyên văn, trọn cụm (số và thực thể ≤ 15 âm tiết, mô tả ≤ 30); câu hỏi loại số chỉ được xin khi đoạn văn có số; giữ khi reader đọc đầy đủ đạt F1 ≥ 0,8. Loại câu chứa đáp án, câu nhãn "số" mà đáp án không có số và câu hỏi nhắc "đoạn văn"; câu hỏi chép câu chứa đáp án (≥ 80% âm tiết trùng) được lấy mẫu về đúng tỉ lệ của ViQuAD train (khoảng 10%) |
| Huấn luyện | AdamW, weight decay 0, cắt chuẩn gradient 1,0, warmup 3% rồi giảm tuyến tính về 0 |
| Không đọc được | Có `<think>` hoặc không kết thúc lượt trong `max_new_tokens`. QA dùng 128 token: với tokenizer Qwen3.5, 10% đáp án vàng của dev cần hơn 32 token, nhưng không đáp án nào cần hơn 128 |
| Chỗ nối prompt | Dấu cách sau "Đoạn văn:" thuộc về khe ngữ cảnh (ngữ cảnh được tokenize thành " " + văn bản), nên prompt ghép từ các đoạn trùng với prompt tokenize liền một lượt |
| G0 | Bắt buộc có kernel flash-linear-attention và causal-conv1d (Qwen3.5); checkpoint không được thiếu key nào |
| Back end | Chỉ HF transformers (không dùng vLLM), một vòng giải mã greedy cho mọi phương pháp |
| Tách dữ liệu (22/10/2026) | Từ ViQuAD train tách theo bài: gate (16 bài, 1.228 câu, chỉ cho quy tắc quyết định) và select (6 bài, 621 câu, mọi lựa chọn). Dev của ViWord-C (chung bài với train) giữ ngoài train. Lọc rò rỉ thêm MLQA-vi, Belebele-vi, VietNews |
| ViQuAD-Long (25/10/2026) | Mỗi bài của gate, select, test: mọi đoạn khác nhau (bỏ trùng theo nguyên văn; không có đoạn trùng) nối theo thứ tự của file JSON chính thức, cách nhau một dòng trống, không giới hạn độ dài; chỉ dùng để đánh giá |
| Bộ ghi đa tỉ lệ (25/10/2026) | Một lượt giai đoạn 1 (5.000 bước, ρ ∈ {4, 8, 16, 32} bốc cho từng mẫu) và một lượt giai đoạn 2 (4.000 bước) cho cả M và ME: mỗi mẫu bốc r ∈ {4, 8, 16}, f ∈ {1, 2, 4, 8} với r·f ≤ 32; 30% mẫu là cửa sổ 2–8 đoạn liên tiếp của một bài train chứa đoạn của câu hỏi. Checkpoint chọn theo loss select 0,7 × đoạn đơn + 0,3 × nhiều đoạn, mỗi mẫu dev một cặp (r, f) cố định. f* chọn lúc suy luận theo F1 select, riêng cho từng thiết lập và từng r |
| Cơ chế đọc (sau tra cứu 16/10/2026) | Bộ ghi không thấy câu hỏi. ME: memory ở r·f + câu gốc BM25 nguyên văn ngay sau ⟨/mem⟩ (không nhãn) trong cùng k; giai đoạn 2 huấn luyện với câu gốc có sẵn |
| Dự phòng MEF (25/10/2026) | Ba tầng, một ngưỡng τ: nhận câu trả lời ME nếu nó nằm nguyên văn trong câu gốc **và** log-prob trung bình ≥ τ; nếu không, đọc BM25 với ngân sách 2k và áp cùng hai kiểm tra; nếu vẫn không, đọc toàn văn. τ là điểm rẻ nhất đạt ≥ 95% F1 toàn văn trên select (điểm giữa hai độ tự tin liền kề), cố định cho gate và test. Đường dự phòng chỉ theo log-prob (ME rồi toàn văn) báo cáo kèm; ECE 10 khoảng, đúng khi F1 ≥ 0,5 |
| W5 (ViLatent-Q) | Bộ ghi thấy câu hỏi: [mồi][câu hỏi][khúc], bỏ trạng thái của mồi và câu hỏi, gộp như W0; chỉ ở r = 4, từ checkpoint giai đoạn 1 đa tỉ lệ |
| Đối chứng và mốc (25/10/2026) | Prompt học được + BM25: một lượt, lr 1e-3, cùng cách bốc (r, f) và trộn nhiều đoạn như ME/M, đọc ở f* của ME. Bộ ghi đóng băng (kiểu LatentPress): L = 4 lớp không huấn luyện, chỉ adapter (khởi tạo I), s và hai embedding biên; chỉ giai đoạn 2; đọc ở f* riêng. Bộ chọn câu PhoBERT (phobert-base-v2, 2 epoch, lr 2e-5, checkpoint theo loss select) là mốc cứng có huấn luyện |
| Quy tắc quyết định (25/10/2026, thay tiêu chí G1) | Trên gate, ViQuAD-Long ở 4×, ME ở f* với seed 0: chênh lệch F1 với mốc cứng tốt nhất (truncation, lead, LLMLingua-2, BM25, PhoBERT) ≥ 3 **và** cận dưới CI 95% bootstrap theo **bài** > 0 **và** cận dưới CI 95% (theo bài) của ME trừ đối chứng "prompt học được + BM25" > 0 **và** tỉ lệ không đọc được < 2% với ME và mốc cứng tốt nhất. Bootstrap theo đoạn là phân tích phụ; đoạn đơn và 8×/16× chỉ mô tả |

## Kết quả

Chưa có. Bảng sẽ được điền sau lượt chạy trên H100.
