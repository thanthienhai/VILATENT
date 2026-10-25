# Hướng dẫn chạy thực nghiệm cho bài ACIIDS 2027 (cho đội vận hành GPU)

Tài liệu này dành cho người chạy máy GPU. Nó thay cho `RUN_G0_G1.md` từ ngày 25/10/2026: luồng G1 cũ (mỗi tỉ lệ
nén một bộ ghi) được thay bằng luồng của bài báo theo checklist sửa đổi ngày 25/10/2026. Người chạy không cần hiểu
phương pháp. Chỉ cần làm đúng thứ tự, kiểm tra kết quả theo từng bảng và dừng lại ở những chỗ ghi **Dừng**.

Những thay đổi chính so với G1:

- **Một bộ ghi đa tỉ lệ.** Giai đoạn 1 chạy một lượt duy nhất, mỗi mẫu bốc ngẫu nhiên tỉ lệ gộp ρ ∈ {4, 8, 16, 32}.
  Giai đoạn 2 chạy một lượt cho cả ViLatent-M và ViLatent-ME ở mọi tỉ lệ r ∈ {4, 8, 16} và mọi hệ số f ∈ {1, 2, 4, 8}
  (chỉ các cặp có r·f ≤ 32). Khoảng 30% mẫu là cửa sổ 2–8 đoạn liên tiếp của cùng một bài.
- **ViQuAD-Long.** Ngoài từng đoạn văn, mỗi câu hỏi còn được hỏi trên cả bài Wikipedia (mọi đoạn của bài, không giới
  hạn độ dài). Thiết lập chính của bài là ViQuAD-Long ở 4×.
- **Mốc mới:** BM25 trên từ (tách bằng pyvi, bỏ từ để hỏi, dò lại k1, b), bộ chọn câu PhoBERT, bộ ghi đóng băng
  (kiểu LatentPress).
- **Dự phòng ba tầng (MEF):** ME, rồi BM25 với ngân sách 2k, rồi toàn văn; đo thêm độ trễ đầu cuối.

Nguyên tắc chung:

- Chạy đúng commit được giao. Mỗi file `.meta.json` ghi lại `git_commit`, nên đừng sửa code trên máy chạy. Nếu cần
  sửa, báo chủ đề tài để có commit mới.
- Không đổi file trong `configs/` (trừ `configs/bm25.json`, do bước `tune_bm25` ghi) và không đổi quy tắc quyết định.
- Tập test (`data/tasks/viquad_test.jsonl`, `viquad_long_test.jsonl`) chỉ được đọc **một lần**, ở bước `test`, sau
  bước `decide`. Các bước lọc rò rỉ chỉ đọc phần ngữ cảnh của nó.
- **Số liệu trong bài chỉ lấy từ H100 (bf16).** T4 trên Kaggle (fp16) chỉ để gỡ lỗi.
- Muốn bỏ hay cắt bớt lượt chạy nào, phải hỏi chủ đề tài trước.
- Mọi lệnh chạy ở thư mục gốc của repo.

## Lịch chạy (26–30/10/2026)

Mã B1–B17 là mã việc trong checklist. H100 #1 chạy luồng chính, H100 #2 chạy mốc và đối chứng song song. Với hai
GPU trên cùng một máy, đặt `GPUS="0 1"`: các lượt độc lập được chia vòng tròn cho hai GPU.

| Ngày | Máy | Lệnh `bash scripts/run_paper.sh …` | Việc |
| --- | --- | --- | --- |
| 26/10 | T4 | `smoke_paper.sh` (mục 2) | B1, B2: kernel DeltaNet fp16, mọi bước chạy được |
| 26/10 | CPU | `data template` | B4: dữ liệu, ViQuAD-Long, cửa sổ nhiều đoạn |
| 26/10 | T4 | `tune_bm25 selector aie` | B3, B5: BM25 trên từ, bộ chọn PhoBERT, tỉ lệ đáp án còn trong văn bản |
| 26/10 | H100 | `g0 teacher` | B6: logit thầy (cả mẫu nhiều đoạn) |
| 26–27/10 | H100 #2 | `baselines` | B7: mốc cứng ở 4×/8×/16×, select và gate, cả hai thiết lập |
| 27/10 | H100 #1 | `stage1` | B8: một lượt giai đoạn 1, 5.000 bước |
| 28–29/10 | H100 #1, #2 | `stage2` | B9 (ME/M), B10 (prompt), B13 (bộ ghi đóng băng); mỗi lượt 4.000 bước |
| 29/10 | H100 | `eval_select choose eval_gate decide` | B12: chọn f* và τ trên select, rồi quy tắc quyết định trên gate |
| 30/10 | H100 | `test figures` | B14: test **một lần**, kèm độ trễ |
| nếu kịp | H100 #2 | `stage2_q`, `stage2_seed2` (trước `eval_select`) | B17 (ViLatent-Q), B15 (seed thứ hai) |

Chỉ có một H100: chạy `stage2` (ba lượt nối tiếp nhau), bỏ `stage2_q` và `stage2_seed2`. **Đo thời gian mỗi bước
ngay ở lượt đầu** (mục 5) để chủ đề tài chốt lịch các ngày sau.

## 0. Yêu cầu máy

| Hạng mục | Yêu cầu |
| --- | --- |
| GPU | GPU có bf16, khuyến nghị H100 80 GB, một hoặc hai GPU. Kaggle 2× T4 chỉ cho lượt thử và các bước `tune_bm25`, `selector` |
| Hệ điều hành | Linux, có CUDA toolkit (`nvcc`) khớp với bản CUDA của torch, để build `causal-conv1d` |
| Đĩa | Nên có ≥ 100 GB trống: bộ nhớ đệm Hugging Face khoảng 30 GB (Qwen3.5-2B và 9B, xlm-roberta-large của LLMLingua-2, PhoBERT, Wikipedia tiếng Việt); `data/` vài GB (logit thầy của cặp giai đoạn 1 khoảng 1,5 GB, của mẫu nhiều đoạn khoảng 0,5 GB); `runs/` khoảng 1 GB mỗi checkpoint |
| RAM | ≥ 32 GB |
| Mạng | Hugging Face Hub (mô hình, dataset, `vinai/phobert-base-v2`) và `dl.fbaipublicfiles.com` (MLQA, chỉ để lọc rò rỉ) |

## 1. Cài đặt

```bash
git clone https://github.com/thanthienhai/VILATENT.git && cd VILATENT
git checkout <commit hoặc nhánh được giao>
python -m venv .venv && source .venv/bin/activate
# transformers ghim ở 5.16.1 (G0 nhận diện kernel DeltaNet theo cách của 5.12 và 5.16); pyvi đi kèm gói vilatent
pip install -e ".[dev,model,data,baselines,teacher]" "transformers==5.16.1" flash-linear-attention
TORCH_CUDA_ARCH_LIST=9.0 MAX_JOBS=8 pip install --no-build-isolation causal-conv1d   # A100: 8.0; T4: 7.5
python -c "import torch, transformers, fla, causal_conv1d, pyvi; print(torch.__version__, transformers.__version__, torch.cuda.is_available())"
pytest -q                                   # 58 passed (CPU)
mkdir -p logs
```

Trên image container có sẵn torch trong venv riêng (ví dụ `/opt/venv`), cài thẳng vào venv đó và ghim đúng bản torch
của image, như đã làm ngày 22/10/2026:

```bash
echo "torch==$(/opt/venv/bin/python -c 'import torch; print(torch.__version__.split("+")[0])')" > /tmp/constraints.txt
uv pip install --python /opt/venv/bin/python -c /tmp/constraints.txt -e ".[dev,model,data,baselines,teacher]" \
  "transformers==5.16.1" flash-linear-attention
TORCH_CUDA_ARCH_LIST=9.0 MAX_JOBS=24 uv pip install --python /opt/venv/bin/python -c /tmp/constraints.txt \
  --no-build-isolation causal-conv1d
```

Các lệnh chạy lâu nên để trong `tmux` hoặc `screen` và ghi log bằng `tee`. `logs/` không đưa lên git.

## 2. Lượt thử (bắt buộc, trước mọi lượt thật)

Lượt thử chạy mọi bước của `run_paper.sh` trên vài chục câu và 16 bước huấn luyện. Chạy trong **một bản sao riêng**
của repo, vì script ghi `data/`, `runs/`, `results/`, `configs/bm25.json`, `paper/figures/curves.tex` và từ chối chạy
nếu `data/`, `runs/` hoặc `results/` đã có:

```bash
git clone . ../VILATENT-smoke && cd ../VILATENT-smoke
# Kaggle 2× T4 (B1, B2): fp16, kèm kiểm tra kernel DeltaNet trên T4
PYTHONPATH=$PWD SMOKE_G0=1 bash scripts/smoke_paper.sh 2>&1 | tee ../VILATENT/logs/smoke.log
# H100: bf16
PYTHONPATH=$PWD DTYPE=bfloat16 GPUS="0" bash scripts/smoke_paper.sh 2>&1 | tee ../VILATENT/logs/smoke_h100.log
cd ../VILATENT
```

Kết quả đạt khi:

- Dòng cuối của log là `smoke: done; …`, và lệnh trả về exit 0.
- Có `results/paper/gate/decision.json`, `results/paper/test/{long,single}/report_r{4,8,16}.json`,
  `results/paper/test/latency_{long,single}.json`.
- Với `SMOKE_G0=1`: `results/g0/Qwen_Qwen3.5-2B.json` có `load.deltanet_kernels` không chứa `torch` (kernel nhanh
  chạy được trên T4). G0 trên T4 trượt không làm dừng lượt thử, nhưng hãy gửi file JSON về.

Dòng `DECISION: FAIL` là **bình thường**: với 16 bước, bộ ghi chưa học được gì. Số liệu của lượt thử không có giá trị
làm bằng chứng. Nếu lệnh dừng với lỗi: **Dừng**, gửi log. Chạy xong thì xoá `../VILATENT-smoke`.

Nếu T4 báo lỗi kernel (B1 lỗi hoặc rất chậm): báo chủ đề tài và gỡ lỗi thẳng trên H100 bằng lượt thử bf16 ở trên.

## 3. Dữ liệu, template, G0 (B1, B4)

```bash
bash scripts/run_paper.sh data template 2>&1 | tee -a logs/data.log
GPUS="0" bash scripts/run_paper.sh g0 2>&1 | tee -a logs/g0.log
```

| Bước | Sinh ra | Kiểm tra |
| --- | --- | --- |
| `data` | `data/tasks/viquad_{train,gate,select,viwordc_dev,test}.jsonl`, `viquad_train_clean.jsonl`, `viquad_long_{gate,select,test}.jsonl`, `viquad_{train,select}_multi.jsonl`, `viquad_long_stats.json`, `data/eval_ext/*.jsonl`, `data/corpus/docs.jsonl`, `data/stage1/pairs_{train,dev}.jsonl`, mỗi file kèm `*.meta.json` | <ul><li>`viquad gate: 1228 answerable questions, 244 passages, 16 articles`, `viquad select: 621 …, 125 passages, 6 articles`, `viquad test: 2653 …, 557 passages, 19 articles`</li><li>Lọc rò rỉ in `{"n_input": 16318, "kept": 15706, "dropped": 612}`</li><li>`long test` in `"articles": 19`, `"answers_in_context": "2653/2653"`, `"duplicate_passages_removed": 0`; độ dài bài (token Qwen3.5) min 1.279, trung vị 4.470, max 18.327</li><li>`train_multi: {"questions": 15706, …}`</li><li>`pairs_train.jsonl` có 96.000 dòng</li></ul> |
| `template` | `configs/readers/qwen3.5-{2b,9b}.json` | `git diff configs/readers` phải rỗng; nếu khác, báo chủ đề tài trước khi đi tiếp |
| `g0` | `results/g0/Qwen_Qwen3.5-2B.json` | `G0_pass: true` |

Các con số ở bảng trên đã được đo lại trên máy của chủ đề tài ngày 25/10/2026. Lệch thì **Dừng** và báo.

## 4. Các bước chạy được trên T4 (B3, B5)

```bash
DTYPE=float16 GPUS="0" bash scripts/run_paper.sh tune_bm25 selector aie 2>&1 | tee -a logs/t4.log
```

| Bước | Việc | Sinh ra |
| --- | --- | --- |
| `tune_bm25` | dò k1 ∈ {0,9; 1,2; 1,5; 2,0} × b ∈ {0,3; 0,5; 0,75; 1,0} của BM25 trên từ, theo F1 của Qwen3.5-2B trên select (đoạn đơn, 4×). Khoảng 1 giờ trên T4 | `configs/bm25.json` với `"units": "word"` |
| `selector` | huấn luyện bộ chọn câu PhoBERT (2 epoch), giữ checkpoint có loss nhỏ nhất trên select. Khoảng 15–30 phút | `runs/paper/selector/` |
| `aie` | đo tỉ lệ đáp án vàng còn nguyên văn, bị cắt dở, hoặc mất trong văn bản mà mỗi cách chọn giữ lại, trên select (chỉ CPU) | `results/paper/select/answer_in_evidence.json` |

Sau bước này, **gửi `configs/bm25.json` về để commit** trước khi chạy `stage2`: các bước `stage2`, `baselines`,
`aie` từ chối chạy nếu `configs/bm25.json` chưa có `"units": "word"`. Nếu `tune_bm25` và `selector` chạy trên máy
khác máy H100, chép `configs/bm25.json` và cả thư mục `runs/paper/selector/` sang máy H100.

## 5. Logit thầy và huấn luyện (B6, B8, B9, B10, B13)

```bash
GPUS="0 1" bash scripts/run_paper.sh teacher stage1 stage2 2>&1 | tee -a logs/train.log
```

| Bước | Việc | Sinh ra |
| --- | --- | --- |
| `teacher` | top-20 log-prob của thầy (reader đọc toàn văn) trên cặp giai đoạn 1, ViQuAD train/select và mẫu nhiều đoạn train/select | `data/teacher/qwen3.5-2b/{pairs_train,pairs_dev,viquad_train,viquad_select,viquad_train_multi,viquad_select_multi}.pt` |
| `stage1` | một bộ ghi đa tỉ lệ, 5.000 bước × batch 32 | `runs/paper/stage1/{best.pt,metrics.jsonl,config.json}` |
| `stage2` | ba lượt, mỗi lượt 4.000 bước: ME/M (`stage2_mem`, từ `stage1`), đối chứng prompt học được + BM25 (`stage2_prompt`, lr 1e-3), bộ ghi đóng băng (`stage2_frozen`); checkpoint chọn theo loss trên select (0,7 × đoạn đơn + 0,3 × nhiều đoạn) | `runs/paper/stage2_{mem,prompt,frozen}/…` |
| `stage2_q` (nếu kịp) | ViLatent-Q, chỉ r = 4, từ `stage1` | `runs/paper/stage2_q/…` |
| `stage2_seed2` (nếu kịp) | seed thứ hai của ME/M và của đối chứng prompt | `runs/paper/stage2_{mem,prompt}_s1/…` |

`stage2_q` và `stage2_seed2` phải xong **trước** `eval_select`, nếu không thì các bước đánh giá sẽ bỏ qua chúng.

### Theo dõi khi huấn luyện

```bash
tail -n 3 runs/paper/*/metrics.jsonl
```

- Dòng `start` liệt kê các cặp `(r, f)` được bốc (`pairs`) và số mẫu nhiều đoạn (`n_train_multi`).
- Dòng `train` (mỗi 10 bước) có `loss`, `ce`, `kl`, `grad_norm`, `mem_norm` cạnh `emb_norm`, `sec_per_step_recent`
  và `peak_mem_gb`. `loss` phải hữu hạn; `mem_norm` không nên lệch `emb_norm` nhiều bậc.
- Dòng `eval` (mỗi 250 bước) có `dev_loss` (đã gộp), `dev_single_loss` và `dev_multi_loss`. `best: true` nghĩa là
  `best.pt` vừa được ghi lại.

**Báo sớm thời gian chạy.** Khoảng 30 phút sau khi `stage1` bắt đầu, và 30 phút sau khi `stage2` bắt đầu, gửi
`sec_per_step_recent` và `peak_mem_gb`. Nếu `stage2` chậm vì mẫu nhiều đoạn dài, chủ đề tài có thể hạ tỉ lệ trộn
xuống 15%: `TRAIN_ARGS="--multi-share 0.15"` (không bao giờ về 0). Không tự đổi khi chưa được báo.

Huấn luyện **không có chế độ chạy tiếp**. Nếu một lượt bị ngắt, chạy lại đúng lệnh của lượt đó (in trong log ở dòng
`GPU <n>: python scripts/train.py --config …`). Khi một lượt lỗi, các lượt xếp sau nó trên cùng GPU không chạy và log
in `GPU <n>: skipped …`.

## 6. Mốc cứng (B7)

Không cần chờ huấn luyện: chạy trên H100 #2 khi đã có `configs/bm25.json` (từ chữ) và bộ chọn PhoBERT.

```bash
GPUS="1" bash scripts/run_paper.sh baselines 2>&1 | tee -a logs/baselines.log
```

Đánh giá full, none, truncation, lead, bm25, bm25_x2 (BM25 với ngân sách 2k, tầng 2 của MEF), phobert, llmlingua2 ở
4×, 8×, 16× trên select và gate, cho cả đoạn đơn và ViQuAD-Long, vào `results/paper/{select,gate}/{long,single}/`.
Toàn văn trên ViQuAD-Long là lượt nặng nhất (bài dài tới khoảng 18 nghìn token). Mỗi phương pháp ghi
`<method>_r<r>.jsonl` và `.summary.json`; chạy lại thì bỏ qua các file đã có.

## 7. Chọn trên select, quyết định trên gate (B12)

```bash
GPUS="0 1" bash scripts/run_paper.sh eval_select choose eval_gate decide 2>&1 | tee -a logs/decide.log
```

| Bước | Việc | Sinh ra |
| --- | --- | --- |
| `eval_select` | ME/M, đối chứng prompt, bộ ghi đóng băng ở mọi (r, f) đã huấn luyện, trên select | `results/paper/select/{long,single}/…` |
| `choose` | f* = f có F1 select cao nhất, riêng cho từng thiết lập và từng r; rồi τ của MEF ở f* (rẻ nhất mà vẫn đạt ≥ 95% F1 toàn văn) | `results/paper/select/choices.json`, `select/*/cascade_r*.json` |
| `eval_gate` | như `eval_select` trên gate, thêm bản đổi memory và ViLatent-Q ở 4× | `results/paper/gate/{long,single}/…` |
| `decide` | MEF với τ đã chốt, báo cáo mọi thiết lập và tỉ lệ, rồi quy tắc quyết định | `results/paper/gate/*/report_r*.json`, `results/paper/gate/decision.json` |

### Quy tắc quyết định (cố định ngày 25/10/2026, trước mọi lượt chạy)

Trên gate, ViQuAD-Long ở 4×, ViLatent-ME ở f* với seed 0, đạt khi thoả cả ba điều kiện:

1. F1 của ME trừ F1 của mốc cứng tốt nhất (truncation, lead, LLMLingua-2, BM25, PhoBERT) ≥ 3 điểm, và cận dưới CI 95%
   (bootstrap theo **bài**) > 0.
2. Cận dưới CI 95% (theo bài) của F1 ME trừ F1 đối chứng prompt học được + BM25 > 0.
3. Tỉ lệ câu trả lời không đọc được dưới 2% với ME và mốc cứng tốt nhất.

Dòng cuối log là `DECISION: PASS` hoặc `DECISION: FAIL`. Người chạy không cần diễn giải. **Dù đạt hay không**, chạy
tiếp mục 8 rồi gửi kết quả.

## 8. Test, một lần (B14)

```bash
GPUS="0 1" bash scripts/run_paper.sh test figures 2>&1 | tee -a logs/test.log
```

`test` đánh giá mọi phương pháp trên test (đoạn đơn và ViQuAD-Long, 4×/8×/16×), MEF với τ của select, báo cáo, F1
theo vị trí đoạn chứa đáp án trong bài (`positions_r4.json`) và đo độ trễ trên H100, batch 1
(`latency_{long,single}.json`). `figures` vẽ lại `paper/figures/curves.tex`.

Bước này từ chối chạy nếu chưa có `results/paper/gate/decision.json`, hoặc nếu `results/paper/test/` đã có file. Nếu
nó dừng giữa chừng vì lỗi: **không xoá** `results/paper/test/`, gửi log về và chờ chủ đề tài. Chủ đề tài có thể cho
chạy tiếp bằng `TEST_RESUME=1` (các file đã xong không bị đánh giá lại).

Đo độ trễ cần GPU rảnh: không chạy việc khác trên GPU đó trong lúc `latency.py` chạy.

## 9. QA sinh tự động (không thuộc bài báo)

Như trước, sau khi xong mục 8, nếu còn thời gian: `bash scripts/run_paper.sh qa_download qa_filter` (cần `HF_TOKEN`
đọc được repo private `thanthienhai/vilatent-qa-gen`). Không chạy `qa_generate` trên cụm.

## 10. Gửi kết quả

```bash
tar czf vilatent_paper.tgz logs results/g0 results/paper runs/paper/*/metrics.jsonl runs/paper/*/config.json \
  runs/paper/selector/selector.json configs/bm25.json data/*/*.meta.json data/tasks/viquad_long_stats.json
```

Kèm `git rev-parse HEAD`, `pip freeze` và `nvidia-smi --query-gpu=name,memory.total --format=csv`. Giữ lại trên máy
(không xoá) `runs/paper/*/best.pt` và `data/`.

## 11. Sự cố thường gặp

| Triệu chứng | Nguyên nhân thường gặp | Cách xử lý |
| --- | --- | --- |
| `fast_deltanet_kernels: false`; trong `deltanet_kernels` có mục là `torch` | thiếu `flash-linear-attention` hoặc `causal-conv1d` | cài lại theo mục 1, rồi chạy lại `run_paper.sh g0` |
| `configs/bm25.json is not tuned for pyvi words yet` | chưa chạy `tune_bm25`, hoặc chưa chép file sang máy này | chạy mục 4, hoặc chép `configs/bm25.json` đã dò |
| `ModuleNotFoundError: pyvi` | cài thiếu | `pip install pyvi==0.1.1` |
| `the phobert baseline needs a trained selector` hoặc không thấy `runs/paper/selector` | chưa chạy `selector` trên máy này | chạy `run_paper.sh selector`, hoặc chép thư mục từ máy T4 |
| `CUDA out of memory` khi huấn luyện | micro-batch 32 không vừa GPU (mẫu nhiều đoạn dài hơn đoạn đơn) | giữ batch hiệu dụng, giảm micro-batch: `TRAIN_ARGS="--micro-batch 16"`; ghi lại trong báo cáo |
| `CUDA out of memory` khi đánh giá ViQuAD-Long | lô sinh quá lớn với bài dài | `EVAL_ARGS="--max-batch-tokens 16000"` rồi chạy lại bước đó (các file đã xong được bỏ qua) |
| `… was trained at ρ […]; this run pools at […]` | `stage2` khởi tạo từ checkpoint giai đoạn 1 khác | chạy lại `stage1` của commit này |
| `(r=…, f=…) was not trained` | đánh giá một cặp không có trong lượt huấn luyện | báo chủ đề tài (không sửa cấu hình) |
| `N examples have no teacher` | dữ liệu đổi sau khi chạy `teacher` | chạy lại `teacher` rồi các bước sau |
| `… was trained with BM25 {…}, not those of configs/bm25.json` | `configs/bm25.json` bị dò lại sau khi đã huấn luyện | khôi phục bản đã dùng khi huấn luyện; báo chủ đề tài |
| `gradient check failed on the writer …`, `dev loss was never finite` | lỗi số học hoặc cài đặt | **Dừng**, gửi `logs/` và `runs/paper/<tên>/metrics.jsonl` |
| `test: … is not empty` | bước `test` đã chạy | không xoá gì, báo chủ đề tài |

Trên GPU không có bf16 (T4), đặt `DTYPE=float16`. Khoảng 10 bước đầu bị GradScaler bỏ qua là bình thường. Kết quả fp16
chỉ dùng để thử đường chạy và cho hai bước `tune_bm25`, `selector`.

## Phụ lục: biến môi trường của `scripts/run_paper.sh`

| Biến | Mặc định | Ý nghĩa |
| --- | --- | --- |
| `GPUS` | `0` | danh sách GPU; các lượt độc lập chia vòng tròn cho các GPU này |
| `DTYPE` | `bfloat16` | `float16` chỉ cho GPU không có bf16 (T4) |
| `RATIOS` | `4 8 16` | các tỉ lệ đánh giá; giữ mặc định |
| `READER`, `READER_9B`, `SLUG` | `Qwen/Qwen3.5-2B`, `Qwen/Qwen3.5-9B`, `qwen3.5-2b` | giữ mặc định |
| `N_PAIRS`, `N_DEV_PAIRS`, `N_WIKI`, `N_NEWS` | 96.000, 1.000, 200.000, 200.000 | cỡ dữ liệu giai đoạn 1; giữ mặc định |
| `TRAIN_ARGS`, `EVAL_ARGS`, `SELECTOR_ARGS`, `LATENCY_ARGS` | rỗng | dành cho `smoke_paper.sh`; ngoài lượt thử chỉ dùng khi thiếu bộ nhớ (xem mục 11) |
| `TEST_RESUME` | `0` | `1` cho phép chạy tiếp bước `test` bị ngắt, chỉ khi chủ đề tài đồng ý |
| `QUANT`, `G0_READERS`, `G0_ARGS` | `none`, reader 2B, rỗng | chỉ cho lượt thử; **không dùng `QUANT=int4` trên cụm** |
| `TEACHER_URL`, `TEACHER_MODEL`, `QA_REPO`, `QA_REVISION` | như G1 | chỉ cho mục 9 |
