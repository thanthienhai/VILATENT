# Chạy huấn luyện và đánh giá bậc Cơ bản (cho đội vận hành GPU)

Tài liệu này là bản rút gọn của [RUN_PAPER.md](RUN_PAPER.md), chỉ gồm bậc **Cơ bản**: các bước đủ để đọc quy tắc quyết
định và có bảng chính của bài. **Không chạy** `stage2_q`, `stage2_seed2`, `adv_select_baselines`, `adv_gate`, `adv_test`
(mục 13 của RUN_PAPER.md). Cần chi tiết, bảng kiểm tra đầy đủ hoặc cách xử lý sự cố thì xem số mục RUN_PAPER.md ghi ở
từng bước. Lịch theo ngày trong RUN_PAPER.md (26-30/10) đã cũ: hãy theo thứ tự và thời gian ước tính ở dưới.

Người chạy không cần hiểu phương pháp. Làm đúng thứ tự, kiểm tra kết quả theo từng bảng, gửi những gì mục "Báo sớm" yêu
cầu, và **dừng lại** ở những chỗ ghi **Dừng** (dừng nghĩa là không chạy tiếp, gửi log cho chủ đề tài và chờ trả lời).

## Thông số lượt chạy

| Mục | Giá trị |
| --- | --- |
| Mã nguồn | `https://github.com/thanthienhai/VILATENT.git`, nhánh `main`, đúng commit chủ đề tài giao (hash đầy đủ; `git log -1` phải trùng) |
| Repo dữ liệu (private) | `thanthienhai/vilatent-data` (dữ liệu, logit thầy, bộ chọn PhoBERT) |
| Máy | hai H100 trên cùng một máy (GPU 0 và GPU 1), bf16. Chỉ có một GPU: dùng `GPUS="0"` và chạy mọi bước nối tiếp |
| `HF_TOKEN` | token có quyền **ghi** vào repo dữ liệu (chủ đề tài cấp). Không ghi vào file trong repo |
| Revision cần gửi về | `DATA_REVISION`, `TEACHER_REVISION`, `SELECTOR_REVISION` (do ba lệnh `*_push` ở bước 2 in ra) |

## Quy tắc

- Không sửa code, không đổi `configs/`, không đổi quy tắc quyết định. Cần sửa thì báo chủ đề tài để có commit mới.
- Số liệu lấy từ bf16 trên H100. Không đặt `DTYPE=float16` hay `QUANT=int4`.
- Tập test chỉ được đọc **một lần**, ở bước `test`, sau `decide`.
- Không chạy `tune_bm25` (`configs/bm25.json` đã dò và commit; script tự bỏ qua).
- Mọi lệnh chạy ở thư mục gốc của repo, trong `tmux` hoặc `screen`, ghi log bằng `tee -a`.
- Huấn luyện không có chế độ chạy tiếp: bị ngắt thì chạy lại đúng lệnh của lượt đó (script in lệnh trong log).
- Dòng `DECISION: FAIL` **không** phải lỗi: vẫn chạy tiếp bước 5.
- Muốn bỏ, cắt bớt hay chạy lại một lượt, hỏi chủ đề tài trước.

## Tổng quan: thứ tự, phụ thuộc, thời gian

Thời gian là ước tính của chủ đề tài (chưa đo trên H100); số thật được đo ở lượt đầu và phải báo sớm. Hai GPU.

| Bước | Lệnh (`bash scripts/run_paper.sh …`) | Cần có trước | GPU | Ước tính |
| --- | --- | --- | --- | --- |
| 1 | lượt thử `smoke_paper.sh` | cài đặt | 0 | 30-45 phút |
| 2a | `data template`, rồi `data_push` | cài đặt | CPU | 1-2 giờ, cộng 10-20 phút tải lên |
| 2b | `g0` | cài đặt | 1 | gộp với 2c, 2d: 1-1,5 giờ |
| 2c | `selector aie selector_push` | 2a | 0 | (gộp ở trên) |
| 2d | `teacher teacher_push` | 2a | 0 và 1 | (gộp ở trên) |
| 3a | `stage1` | 2d | 0 | 2-3 giờ |
| 3b | `baselines` (song song với 3a) | 2c | 1 | 2-3 giờ |
| 3c | `stage2` | 3a và 3b | 0 và 1 | 3-5 giờ |
| 3d | `stage2_frozen` (song song với 3e) | 3c | 1 | 1-1,5 giờ |
| 3e | `signal` (song song với 3d) | 3c | 0 | dưới 1 giờ |
| 4 | `eval_select choose eval_gate decide` | 3d và 3e | 0 và 1 | 2-3 giờ |
| 5 | `test figures` (một lần) | 4 | 0 và 1 | 1,5-3 giờ |

Đường găng (2a, 2c hoặc 2d, 3a, 3c, 3d, 4, 5) khoảng 12-20 giờ nếu mọi thứ chạy liền. Bước 1 và 2b chạy song song với 2a.

## Bước 0. Cài đặt (RUN_PAPER.md mục 1)

```bash
git clone https://github.com/thanthienhai/VILATENT.git && cd VILATENT && git checkout <commit chủ đề tài giao>
pip install -e ".[dev,model,data,baselines,teacher]" "transformers==5.16.1" flash-linear-attention
TORCH_CUDA_ARCH_LIST=9.0 MAX_JOBS=8 pip install --no-build-isolation causal-conv1d
export HF_TOKEN=...
python -c "import torch, transformers, fla, causal_conv1d, pyvi; print(torch.__version__, transformers.__version__, torch.cuda.device_count())"
```

Dòng cuối phải in `transformers` 5.16.1 và 2 GPU, không lỗi import.

## Bước 1. Lượt thử (RUN_PAPER.md mục 2)

Chạy mọi bước một lần trên vài chục câu và 16 bước huấn luyện, để lỗi lộ ra trước khi tốn giờ GPU. Lượt thử cũng chạy
qua các bước Nâng cao một lần để kiểm đường code; đó là chủ đích của lượt thử, **không** phải chạy Nâng cao thật. Chạy
trong một bản sao riêng, vì script từ chối chạy nếu `data/`, `runs/` hoặc `results/` đã có:

```bash
git clone . ../VILATENT-smoke && cd ../VILATENT-smoke
PYTHONPATH=$PWD DTYPE=bfloat16 GPUS="0" RATIOS="4 8 16" bash scripts/smoke_paper.sh 2>&1 | tee ../VILATENT/logs/smoke_h100.log
cd ../VILATENT && rm -rf ../VILATENT-smoke
```

(Tạo `logs/` trước nếu chưa có: `mkdir -p logs`.) **Đạt** khi dòng cuối của log là `smoke: done; …` và lệnh trả về 0.
`DECISION: FAIL` trong lượt thử là bình thường, các con số của nó không dùng vào đâu. Lỗi: **Dừng**, gửi `logs/smoke_h100.log`.

## Bước 2. Dữ liệu, bộ chọn, logit thầy (RUN_PAPER.md mục 3, 4)

Dữ liệu dựng thẳng trên cụm từ các nguồn online (đã ghim revision). `data` chủ yếu dùng CPU nên chạy trong một cửa sổ
tmux riêng, cùng lúc với bước 1 và `g0` trên GPU.

**2a. Dữ liệu** (tmux CPU):

```bash
bash scripts/run_paper.sh data template 2>&1 | tee -a logs/data.log
```

Kiểm tra theo bảng ở RUN_PAPER.md mục 3. Các con số chính:

| Kiểm tra | Giá trị đúng |
| --- | --- |
| số câu hỏi theo split | gate 1228 (16 bài), select 621 (6 bài), test 2653 (19 bài) |
| lọc rò rỉ | `{"n_input": 16318, "kept": 15706, "dropped": 612}` |
| `data/stage1/pairs_train.jsonl` | 96.000 dòng |
| `sha256sum data/tasks/viquad_select.jsonl` | bắt đầu bằng `cb88b5be8329` |
| `git diff configs/readers` (sau `template`) | rỗng |

Lệch số nào thì **Dừng** và báo, và **không** chạy `data_push`. Khớp hết thì đẩy lên Hub (khoảng 2,5 GB):

```bash
bash scripts/run_paper.sh data_push 2>&1 | tee -a logs/data.log
```

**Đạt** khi dòng cuối in `{"repo": …, "bundle": "data", "revision": "<commit>"}`. Gửi revision về. Nếu log in
`WARNING: the working tree is not a clean commit`, nghĩa là code trên máy đã bị sửa: **Dừng** và báo.

**2b. Kiểm tra kernel** (GPU, chạy song song với 2a):

```bash
CUDA_VISIBLE_DEVICES=1 bash scripts/run_paper.sh g0 2>&1 | tee -a logs/g0.log
```

**Đạt** khi `results/g0/Qwen_Qwen3.5-2B.json` có `G0_pass: true` và trong `load.deltanet_kernels` không có mục nào là
`torch`. Không đạt: cài lại `flash-linear-attention` và `causal-conv1d` (bước 0) rồi chạy lại.

**2c. Bộ chọn PhoBERT và đo đáp án** (sau 2a):

```bash
CUDA_VISIBLE_DEVICES=0 bash scripts/run_paper.sh selector aie selector_push 2>&1 | tee -a logs/prep.log
```

**Đạt** khi có `runs/paper/selector/`, `results/paper/select/answer_in_evidence.json`, và dòng cuối in
`"bundle": "selector"` kèm revision (cũng ghi ở `data/hub_selector_revision.txt`). Gửi revision về.

**2d. Logit thầy** (sau 2a, `template` đã chạy):

```bash
GPUS="0 1" bash scripts/run_paper.sh teacher teacher_push 2>&1 | tee -a logs/prep.log
```

**Đạt** khi có 6 file trong `data/teacher/qwen3.5-2b/` và dòng cuối in `"bundle": "teacher"` kèm revision. Gửi revision về.

## Bước 3. Huấn luyện và mốc cứng (RUN_PAPER.md mục 5, 6)

**3a và 3b**, hai cửa sổ tmux cùng lúc (một GPU thì chạy lần lượt):

```bash
GPUS="0" bash scripts/run_paper.sh stage1    2>&1 | tee -a logs/train.log        # tmux 1
GPUS="1" bash scripts/run_paper.sh baselines 2>&1 | tee -a logs/baselines.log    # tmux 2
```

**3c**, khi **cả hai** đã xong:

```bash
GPUS="0 1" bash scripts/run_paper.sh stage2 2>&1 | tee -a logs/train.log
```

**3d và 3e**, khi `stage2` xong, hai cửa sổ cùng lúc (một GPU thì `stage2_frozen` trước, `signal` sau):

```bash
GPUS="1" bash scripts/run_paper.sh stage2_frozen 2>&1 | tee -a logs/train.log    # tmux 1
GPUS="0" bash scripts/run_paper.sh signal        2>&1 | tee -a logs/decide.log   # tmux 2
```

`stage2_frozen` phải xong **trước** bước 4 (nếu không, chạy lại `eval_select choose` sau khi nó xong).

| Bước | Việc | Sinh ra |
| --- | --- | --- |
| `stage1` | một bộ ghi đa tỉ lệ, 5.000 bước, batch hiệu dụng 32 | `runs/paper/stage1/{best.pt,metrics.jsonl,config.json}` |
| `stage2` | hai lượt 4.000 bước: `stage2_mem` (GPU 0) và `stage2_prompt` (GPU 1) | `runs/paper/stage2_{mem,prompt}/` |
| `stage2_frozen` | bộ ghi đóng băng, 4.000 bước | `runs/paper/stage2_frozen/` |
| `baselines` | chỉ các ô mà bước sau đọc: select `full` và `bm25_x2`; gate chỉ Long ở 4× với đủ mốc cứng | `results/paper/select/*`, `results/paper/gate/long/*` |
| `signal` | ME và đối chứng prompt trên select, Long, 4×, mọi f | `results/paper/select/long/{vilatent_me,prompt_bm25}_f*_r4.*` |

Theo dõi: `tail -n 3 runs/paper/*/metrics.jsonl` và `nvidia-smi dmon -s u -c 30`. Báo chủ đề tài (không tự đổi gì) nếu:

- `loss` không hữu hạn, hoặc có thông báo `gradient check failed` / `dev loss was never finite`: **Dừng**, gửi `logs/` và `metrics.jsonl`.
- sau 1.000 bước, loss dev của `stage2_mem` và `stage2_prompt` gần như bằng nhau;
- `stage2` chậm hơn khoảng 3 giây mỗi bước, hoặc GPU thường dưới 70%.

**Dừng sau `signal`:** gửi F1 của ME và của đối chứng prompt ở mọi f. Nếu ME không hơn đối chứng ở f nào, báo chủ đề
tài **trước** khi chạy bước 4.

## Bước 4. Chọn trên select, quyết định trên gate (RUN_PAPER.md mục 7)

```bash
GPUS="0 1" bash scripts/run_paper.sh eval_select choose eval_gate decide 2>&1 | tee -a logs/decide.log
```

| Bước | Việc | Sinh ra |
| --- | --- | --- |
| `eval_select` | đánh giá ME, đối chứng prompt, bộ ghi đóng băng ở mọi (tỉ lệ, f) đã huấn luyện, trên select | `results/paper/select/{long,single}/` |
| `choose` | chọn f\* theo F1 select cho từng thiết lập và tỉ lệ, rồi τ của MEF | `results/paper/select/choices.json` |
| `eval_gate` | ME và đối chứng prompt tại f\*, Long, 4×, trên gate | `results/paper/gate/long/` |
| `decide` | báo cáo và quy tắc quyết định | `results/paper/gate/decision.json` |

**Đạt** khi có `choices.json` và `decision.json`, và dòng cuối log là `DECISION: PASS` hoặc `DECISION: FAIL`. Gửi hai file
đó và dòng quyết định về, rồi chạy tiếp bước 5 (kể cả khi FAIL).

## Bước 5. Test, đúng một lần (RUN_PAPER.md mục 8)

```bash
GPUS="0 1" bash scripts/run_paper.sh test figures 2>&1 | tee -a logs/test.log
```

`test` đánh giá trên test (đoạn đơn và ViQuAD-Long, 4×/8×/16×): mọi mốc cứng; ME tại f\* và M; đối chứng prompt tại f\*;
bộ ghi đóng băng tại f\* của nó; bản đổi memory tại f\* của 4×; MEF; cùng F1 theo vị trí đoạn và đo độ trễ. `figures` vẽ
lại `paper/figures/curves.tex`.

- Bước này từ chối chạy nếu chưa có `results/paper/gate/decision.json`, hoặc nếu `results/paper/test/` đã có file.
- Nếu dừng giữa chừng vì lỗi: **không xoá** `results/paper/test/`, gửi log và chờ. Chủ đề tài có thể cho chạy tiếp bằng `TEST_RESUME=1`.
- Lúc `latency.py` chạy ở cuối, không chạy việc gì khác trên hai GPU này, kể cả của người khác.

## Bước 6. Sao lưu và gửi kết quả (RUN_PAPER.md mục 9, 10)

Sau mỗi bước 2 đến 5, chép sang ổ lưu trữ lâu dài (không phải ổ tạm của node):

```bash
BACKUP=/path/den/o/luu/tru/vilatent_paper     # thay bằng đường dẫn thật
rsync -a runs results logs "$BACKUP"/
rsync -a --include='*/' --include='*.meta.json' --include='*_stats.json' --exclude='*' data "$BACKUP"/
```

Sau bước 5, đóng gói và gửi:

```bash
tar czf vilatent_paper.tgz logs results/g0 results/paper runs/paper/*/metrics.jsonl runs/paper/*/config.json \
  runs/paper/selector/selector.json configs/bm25.json data/*/*.meta.json data/tasks/viquad_long_stats.json
git rev-parse HEAD > GIT_COMMIT.txt; pip freeze > pip_freeze.txt
nvidia-smi --query-gpu=name,memory.total --format=csv > gpu.txt; nproc > nproc.txt
```

Gói này nhỏ (vài chục MB); gửi kèm bốn file `GIT_COMMIT.txt`, `pip_freeze.txt`, `gpu.txt`, `nproc.txt`. Checkpoint
(`best.pt`, khoảng 1 GB mỗi file) chỉ gửi khi được yêu cầu. Không xoá `runs/paper/*/best.pt` và `data/` cho tới khi chủ
đề tài báo đã nhận đủ.

## Báo sớm (gửi ngay, không chờ hết lượt)

| Lúc | Gửi gì |
| --- | --- |
| Lượt thử xong | `logs/smoke_h100.log` (dòng cuối phải là `smoke: done`) |
| `data` xong | các dòng kiểm tra ở bước 2a |
| `data_push`, `selector_push`, `teacher_push` xong | ba revision |
| 30 phút sau khi `stage1` và `stage2` bắt đầu | `tail -n 3 runs/paper/<tên>/metrics.jsonl` (lấy `sec_per_step_recent`, `peak_mem_gb`) |
| `baselines` xong | các `*.summary.json` trong `results/paper/select` và `results/paper/gate/long` |
| `signal` xong | F1 của ME và của đối chứng prompt ở mọi f |
| `decide` xong | `decision.json` và dòng `DECISION: …` |
| `test` xong | gói kết quả ở bước 6 |

## Sự cố thường gặp

Bảng đầy đủ ở RUN_PAPER.md mục 11. Ba lỗi hay gặp:

| Triệu chứng | Cách xử lý |
| --- | --- |
| `CUDA out of memory` khi huấn luyện | giữ batch hiệu dụng, chạy lại đúng lượt đó với `TRAIN_ARGS="--micro-batch 16"`; ghi lại trong báo cáo |
| `CUDA out of memory` khi đánh giá ViQuAD-Long | chạy lại bước đó với `EVAL_ARGS="--max-batch-tokens 16000"`; các file đã xong được bỏ qua |
| `data_push` / `selector_push` / `teacher_push` lỗi 401 hoặc 403 | `HF_TOKEN` chưa đặt hoặc thiếu quyền ghi: xin chủ đề tài token đúng, chạy lại đúng bước đó (không cần dựng lại dữ liệu) |
