# ViLatent

Mã nguồn nghiên cứu cho đề tài *ViLatent: nén mềm ngữ cảnh cho reader tiếng Việt đóng băng*. Bộ ghi (bản sao L lớp
đáy của reader, gộp trung bình mỗi r token, RMSNorm và adapter d×d) nén ngữ cảnh thành k memory vector. Reader đóng
băng đọc các vector này qua `inputs_embeds`.

- [`docs/VILATENT.md`](docs/VILATENT.md): đề xuất nghiên cứu (giả thuyết H1–H5, kiến trúc W0, cổng G0–G3). Các chú
  thích "docs/VILATENT.md §…" trong mã trỏ tới tài liệu này.
- [`docs/RUN_G0_G1.md`](docs/RUN_G0_G1.md): hướng dẫn chạy G0 và G1 trên máy GPU.

> Trạng thái: mã đã sẵn sàng cho **G0 và G1** (Qwen3.5-2B, ViQuAD, 4×), **chưa có kết quả thực nghiệm**. Hệ chính là
> ViLatent-ME: bộ ghi không thấy câu hỏi (memory ghi một lần) cộng câu gốc chọn theo câu hỏi trong cùng ngân sách,
> kèm cấu hình dự phòng MEF và nhánh so sánh W5 (xem docs/VILATENT.md, "Đọc theo câu hỏi"). Các phần
> sau G1 (W1/W2/W4, O-AE, trộn γ, MLQA/H2, Vi-MQA, IFEval-vi, ICAE, H4/H5, đo hiệu năng) sẽ được viết khi G1 đạt.

## Cấu trúc

```
vilatent/            thư viện
  text.py            chuẩn hoá NFC, tách câu bằng regex (có danh sách viết tắt), âm tiết
  budget.py          chia khúc theo câu (≤ 512 token reader), ngân sách k = Σ ceil(n_i / r)  — dùng chung mọi nơi
  template.py        template chat cố định của từng reader (tắt thinking), ghép prompt theo đoạn token
  reader.py          nạp reader đóng băng, giải mã greedy từ inputs_embeds (một đường cho mọi phương pháp)
  writer.py          bộ ghi W0: L lớp đáy + token mồi bị bỏ + gộp r token + RMSNorm·s + adapter (khởi tạo I);
                     W5: câu hỏi đặt giữa token mồi và khúc
  model.py           ViLatent ở ba chế độ M / ME / W5: encode_memory, memory_prompt, loss; lưu/nạp checkpoint
  fallback.py        ViLatent-MEF: đọc lại toàn văn khi log-prob câu trả lời < τ; đường đánh đổi, chọn τ trên dev
  losses.py          CE + λ·KL(thầy ‖ trò) trên top-20 của thầy + ô "còn lại"
  teacher.py         tính trước top-20 log-prob của thầy (reader đọc ngữ cảnh đầy đủ)
  train.py           vòng huấn luyện giai đoạn 1 và 2, chọn checkpoint theo loss dev
  baselines.py       full, none, truncation, lead (câu trọn vẹn), bm25 (chọn câu theo câu hỏi), llmlingua2
  evaluate.py        đánh giá QA cho nén mềm và nén cứng trên cùng ngân sách
  metrics.py         F1/EM trên âm tiết, câu trả lời không đọc được, lặp từ
  stats.py           bootstrap cặp theo seed × cụm đoạn văn, MDE, Holm
  leak.py            chỉ mục n-gram 13 âm tiết chống rò rỉ
  data.py            định dạng JSONL, sidecar provenance <file>.meta.json
scripts/             prepare_viquad, build_corpus, make_pairs, leak_filter, generate_qa, filter_qa,
                     render_template, g0_check, precompute_teacher, train, evaluate, select_me (chọn f theo
                     loss dev), fallback_report (MEF), g1_report; run_g1.sh nối tất cả
configs/readers/     template đã render của từng reader (commit vào git; checkpoint và logit thầy gắn với hash của nó)
configs/g1/          G1: giai đoạn 1 ở 4×/8×/16×/32×; giai đoạn 2 cho M, W5 và ME với f = 2, 4, 8
tests/               test CPU với Qwen3.5 ngẫu nhiên tí hon, không cần GPU hay tải mô hình
```

Dữ liệu (`data/`), checkpoint (`runs/`) và kết quả (`results/`) không đưa lên git.

## Cài đặt

Python ≥ 3.10. Mỗi nhóm phụ thuộc là một extra:

```bash
pip install -e ".[dev]"                          # lõi + test (CPU)
pip install -e ".[model,data,baselines,teacher]" # reader, dữ liệu, LLMLingua-2, LLM thầy
pip install -e ".[kernels]"                      # kernel Gated DeltaNet (Linux + CUDA), cần cho backward nhanh
pytest -q                                        # 34 test, chạy trên CPU
```

Qwen3.5 cần transformers có model type `qwen3_5` (đã thử với 5.12). Thiếu `flash-linear-attention` và
`causal-conv1d` thì transformers vẫn chạy DeltaNet bằng torch thuần nhưng chậm; `scripts/g0_check.py` báo cáo việc
này. Trên Windows, đặt `PYTHONIOENCODING=utf-8` để in được tiếng Việt.

## Chạy G0 và G1

```bash
bash scripts/run_g1.sh data template g0                  # tuần 1–2: dữ liệu, template, cổng G0
bash scripts/run_g1.sh qa_gen                             # chạy ngầm: QA sinh tự động (iCOMM 27B)
bash scripts/run_g1.sh teacher stage1 stage2 eval report  # tuần 3: cổng G1
```

Chi tiết từng bước, thời gian dự kiến và các file cần gửi lại nằm trong [`docs/RUN_G0_G1.md`](docs/RUN_G0_G1.md).

## Các quyết định cài đặt ngoài tài liệu

Những điểm `docs/VILATENT.md` chưa quy định, đã thống nhất với chủ đề tài trước khi viết mã:

| Điểm | Quyết định |
| --- | --- |
| Token đầu khúc | Chèn token mồi (`<|endoftext|>` với Qwen, BOS với Vistral) vào đầu mỗi khúc rồi bỏ trạng thái ẩn của nó; mọi token nội dung đều được gộp |
| Bộ ghi và khúc | Mỗi khúc chạy độc lập qua bộ ghi |
| Ngân sách | k = Σ ceil(n_i / r), nhóm cuối của khúc có thể ít hơn r token; ⟨mem⟩ ⟨/mem⟩ không tính; mốc nén cứng nhận đúng k token reader |
| Truncation, Lead-k, BM25 | Truncation giữ k token đầu. Lead-k chỉ giữ câu trọn vẹn, không lấp phần còn lại (nếu lấp thì trùng với Truncation). BM25 lấp phần còn lại bằng đầu của câu điểm cao nhất chưa vừa |
| ⟨mem⟩ ⟨/mem⟩ | Khởi tạo bằng embedding trung bình của token "«" và "»" |
| Kiểu số | Trọng số huấn luyện fp32, tính bằng autocast bf16; reader bf16 |
| Giai đoạn 1 | Wikipedia + BKAINewsCorpus 50 : 50; A dài 128–1.024 token (cắt ở cuối câu), B là 128 token tiếp theo; qua chat template ("Viết tiếp đoạn văn sau") |
| Prompt | Không dùng system prompt cho mọi reader; chỉ dẫn QA lấy nguyên văn từ ViWord-C |
| QA sinh tự động | Đáp án phải là span nguyên văn; giữ khi reader đọc đầy đủ đạt F1 ≥ 0,8 |
| Huấn luyện | AdamW, weight decay 0, cắt chuẩn gradient 1,0, warmup 3% rồi giảm tuyến tính về 0 |
| Không đọc được | Có `<think>` hoặc không kết thúc lượt trong `max_new_tokens`. QA dùng 128 token: với tokenizer Qwen3.5, 10% đáp án vàng của dev cần hơn 32 token, nhưng không đáp án nào cần hơn 128 |
| Chỗ nối prompt | Dấu cách sau "Đoạn văn:" thuộc về khe ngữ cảnh (ngữ cảnh được tokenize thành " " + văn bản), nên prompt ghép từ các đoạn trùng với prompt tokenize liền một lượt (đã kiểm trên 1.175/1.175 câu dev) |
| G0 | Bắt buộc có kernel flash-linear-attention và causal-conv1d (Qwen3.5); checkpoint không được thiếu key nào |
| Back end | Chỉ HF transformers ở G0/G1 (không dùng vLLM), một vòng giải mã greedy cho mọi phương pháp |
| Tiêu chí G1 | Trên ViQuAD dev ở 4×: chênh lệch F1 (ViLatent-ME trừ mốc cứng tốt nhất) ≥ 3 **và** cận dưới CI 95% bootstrap theo đoạn > 0 |
| Cơ chế đọc (sau tra cứu 16/10/2026) | Bộ ghi không thấy câu hỏi. ME: memory ở r·f + câu gốc BM25 nguyên văn ngay sau ⟨/mem⟩ (không nhãn) trong cùng k; giai đoạn 2 huấn luyện với câu gốc có sẵn. f ∈ {2, 4, 8} chọn theo loss dev, không theo F1 dev (tránh làm cổng lạc quan) |
| Dự phòng MEF | Đọc lại toàn văn khi log-prob trung bình của câu trả lời ME < τ; τ là ngưỡng nhỏ nhất đạt ≥ 95% F1 toàn văn trên dev, cố định cho test; chi phí tính cả lần đọc memory đầu |
| W5 | Bộ ghi thấy câu hỏi: [mồi][câu hỏi][khúc], bỏ trạng thái của mồi và câu hỏi, gộp như W0; dùng chung giai đoạn 1 với W0 ở cùng r |

## Kết quả

Chưa có. Bảng sẽ được điền sau G1.
