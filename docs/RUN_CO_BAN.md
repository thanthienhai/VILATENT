# Chạy huấn luyện và đánh giá bậc Cơ bản (cho đội vận hành GPU)

Tài liệu này là bản rút gọn của [RUN_PAPER.md](RUN_PAPER.md), chỉ gồm bậc **Cơ bản**: các bước đủ để đọc quy tắc quyết
định và có bảng chính của bài. **Không chạy** `stage2_q`, `stage2_seed2`, `adv_select_baselines`, `adv_gate`,
`adv_test` (mục 13 của RUN_PAPER.md). Khi cần chi tiết, bảng kiểm tra hoặc xử lý sự cố, xem số mục được ghi ở từng bước.

## Thông số lượt chạy

| Mục | Giá trị |
| --- | --- |
| Commit | `COMMIT_SẼ_ĐIỀN` (`git log -1` phải trùng) |
| `DATA_REVISION`, `TEACHER_REVISION` | chưa có; do cụm tạo ở `data_push`, `teacher_push` |
| `SELECTOR_REVISION` | chưa có; do cụm tạo ở `selector_push` |
| Repo dữ liệu (private) | `thanthienhai/vilatent-data` |
| GPU | H100, bf16. Hai GPU: `GPUS="0 1"`. Một GPU: `GPUS="0"` và chạy nối tiếp |

## Quy tắc

- Không sửa code, không đổi `configs/`, không đổi quy tắc quyết định. Cần sửa thì báo chủ đề tài để có commit mới.
- Số liệu lấy từ bf16 trên H100. Không đặt `DTYPE=float16` hay `QUANT=int4`.
- Tập test chỉ đọc một lần, ở bước `test`, sau `decide`.
- Không chạy `tune_bm25` (`configs/bm25.json` đã dò và commit; script tự bỏ qua).
- Chạy trong `tmux`, ghi log bằng `tee`. Huấn luyện không có chế độ chạy tiếp: bị ngắt thì chạy lại đúng lệnh của lượt đó.
- Dòng `DECISION: FAIL` không phải lỗi; vẫn chạy tiếp `test`.

## Bước 0. Cài đặt (RUN_PAPER.md mục 1)

```bash
git clone <repo> VILATENT && cd VILATENT && git checkout <COMMIT>
pip install -e ".[dev,model,data,baselines,teacher]" "transformers==5.16.1" flash-linear-attention
TORCH_CUDA_ARCH_LIST=9.0 MAX_JOBS=8 pip install --no-build-isolation causal-conv1d
export HF_TOKEN=...     # quyền ghi repo vilatent-data (để data_push, teacher_push, selector_push)
```

## Bước 1. Lượt thử (RUN_PAPER.md mục 2)

Chạy trong một bản sao riêng, vì script từ chối chạy khi `data/`, `runs/` hoặc `results/` đã có. Smoke chạy cả các bước
Nâng cao để kiểm đường code; đó là chủ đích của lượt thử, không phải chạy Nâng cao thật.

```bash
git clone . ../VILATENT-smoke && cd ../VILATENT-smoke
PYTHONPATH=$PWD DTYPE=bfloat16 GPUS="0" RATIOS="4 8 16" bash scripts/smoke_paper.sh 2>&1 | tee ../VILATENT/logs/smoke_h100.log
cd ../VILATENT && rm -rf ../VILATENT-smoke
```

Đạt khi dòng cuối là `smoke: done; …`. `DECISION: FAIL` ở đây là bình thường. Lỗi: **Dừng**, gửi log.

## Bước 2. Dữ liệu và logit thầy (RUN_PAPER.md mục 3, 4)

Dữ liệu dựng thẳng trên cụm từ các nguồn online (đã ghim revision). Bước `data` chủ yếu dùng CPU (khoảng 1-2 giờ, chủ
yếu là duyệt Wikipedia và BKAINewsCorpus), nên chạy nó trong một cửa sổ tmux riêng **cùng lúc** với bước 1 và `g0` trên GPU.

```bash
bash scripts/run_paper.sh data template 2>&1 | tee -a logs/data.log                  # tmux CPU
GPUS="0" bash scripts/run_paper.sh g0 2>&1 | tee -a logs/g0.log                      # tmux GPU
```

Kiểm tra `data` theo bảng ở RUN_PAPER.md mục 3 (gate 1228 câu, select 621, test 2653; lọc rò rỉ `kept` 15706; `pairs_train`
96.000 dòng; sha256 của `viquad_select.jsonl` bắt đầu bằng `cb88b5be8329`). Lệch số nào thì **Dừng** và báo. Khớp hết thì
đẩy lên Hub để lần sau dùng lại (không bắt buộc cho lượt này, nhưng nên làm: chủ đề tài cần revision):

```bash
bash scripts/run_paper.sh data_push 2>&1 | tee -a logs/data.log      # cần HF_TOKEN có quyền ghi; gửi revision về
GPUS="0" bash scripts/run_paper.sh selector aie selector_push 2>&1 | tee -a logs/prep.log
GPUS="0 1" bash scripts/run_paper.sh teacher teacher_push 2>&1 | tee -a logs/prep.log
```

| Bước | Đạt khi |
| --- | --- |
| `data` | các con số kiểm tra ở trên khớp |
| `data_push` | dòng cuối in `"bundle": "data"` kèm revision |
| `template` | `git diff configs/readers` rỗng |
| `g0` | `results/g0/Qwen_Qwen3.5-2B.json` có `G0_pass: true`, không mục `torch` trong `load.deltanet_kernels` |
| `selector`, `aie` | có `runs/paper/selector/` và `results/paper/select/answer_in_evidence.json` |
| `selector_push` | dòng cuối in `"bundle": "selector"` kèm revision (cũng ở `data/hub_selector_revision.txt`); gửi revision về. Cần `HF_TOKEN` có quyền ghi |

## Bước 3. Huấn luyện (RUN_PAPER.md mục 5)

Hai GPU: `stage1` (GPU 0) và `baselines` (GPU 1) chạy song song. Một GPU: nối tiếp.

```bash
GPUS="0" bash scripts/run_paper.sh stage1    2>&1 | tee -a logs/train.log       # tmux 1
GPUS="1" bash scripts/run_paper.sh baselines 2>&1 | tee -a logs/baselines.log   # tmux 2
```

Khi cả hai xong:

```bash
GPUS="0 1" bash scripts/run_paper.sh stage2 2>&1 | tee -a logs/train.log        # stage2_mem và stage2_prompt
```

Khi `stage2` xong, hai cửa sổ cùng lúc (một GPU thì `stage2_frozen` trước, `signal` sau):

```bash
GPUS="1" bash scripts/run_paper.sh stage2_frozen 2>&1 | tee -a logs/train.log   # tmux 1
GPUS="0" bash scripts/run_paper.sh signal        2>&1 | tee -a logs/decide.log  # tmux 2
```

`stage2_frozen` phải xong **trước** `eval_select`.

| Bước | Sinh ra |
| --- | --- |
| `stage1` | `runs/paper/stage1/best.pt` (5.000 bước) |
| `stage2` | `runs/paper/stage2_mem/`, `runs/paper/stage2_prompt/` (4.000 bước mỗi lượt) |
| `stage2_frozen` | `runs/paper/stage2_frozen/` (4.000 bước) |
| `baselines` | `results/paper/select/*` (`full`, `bm25_x2`), `results/paper/gate/long/*` (đủ mốc cứng, Long 4×) |
| `signal` | `results/paper/select/long/{vilatent_me,prompt_bm25}_f*_r4.*` |

Theo dõi bằng `tail -n 3 runs/paper/*/metrics.jsonl`. Nếu loss không hữu hạn, hoặc sau 1.000 bước loss dev của
`stage2_mem` và `stage2_prompt` gần như bằng nhau, hoặc `stage2` chậm hơn ~3 s/bước: báo chủ đề tài, không tự đổi.

**Dừng sau `signal`:** gửi F1 của ME và của đối chứng prompt ở mọi f. Nếu ME không hơn đối chứng ở f nào, báo chủ đề tài
trước khi chạy tiếp.

## Bước 4. Chọn trên select, quyết định trên gate (RUN_PAPER.md mục 7)

```bash
GPUS="0 1" bash scripts/run_paper.sh eval_select choose eval_gate decide 2>&1 | tee -a logs/decide.log
```

Đạt khi có `results/paper/select/choices.json` và `results/paper/gate/decision.json`; dòng cuối log là
`DECISION: PASS` hoặc `DECISION: FAIL`. Gửi hai file đó và dòng quyết định về.

## Bước 5. Test, một lần (RUN_PAPER.md mục 8)

```bash
GPUS="0 1" bash scripts/run_paper.sh test figures 2>&1 | tee -a logs/test.log
```

Bước này từ chối chạy nếu chưa có `decision.json` hoặc `results/paper/test/` đã có file. Nếu dừng giữa chừng: **không xoá**
`results/paper/test/`, gửi log và chờ chủ đề tài (có thể cho `TEST_RESUME=1`). Khi `latency.py` chạy ở cuối, không chạy
việc khác trên hai GPU.

## Bước 6. Sao lưu và gửi kết quả (RUN_PAPER.md mục 9, 10)

Sau mỗi bước 2 đến 5, chép `runs results logs` sang ổ lưu trữ lâu dài. Cuối cùng:

```bash
tar czf vilatent_paper.tgz logs results/g0 results/paper runs/paper/*/metrics.jsonl runs/paper/*/config.json \
  runs/paper/selector/selector.json configs/bm25.json data/*/*.meta.json data/tasks/viquad_long_stats.json
```

Kèm `git rev-parse HEAD`, `pip freeze`, `nvidia-smi --query-gpu=name,memory.total --format=csv`. Không xoá
`runs/paper/*/best.pt` và `data/` cho tới khi chủ đề tài báo đã nhận đủ.

## Báo sớm

| Lúc | Gửi gì |
| --- | --- |
| Lượt thử xong | `logs/smoke_h100.log` |
| 30 phút sau khi `stage1` và `stage2` bắt đầu | `tail -n 3 runs/paper/<tên>/metrics.jsonl` (`sec_per_step_recent`, `peak_mem_gb`) |
| `baselines` xong | các `*.summary.json` trong `results/paper/select` và `results/paper/gate/long` |
| `signal` xong | F1 của ME và đối chứng ở mọi f |
| `decide` xong | `decision.json` và dòng `DECISION` |
| `test` xong | gói kết quả ở bước 6 |
