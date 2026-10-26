# Hướng dẫn chạy thực nghiệm cho bài ACIIDS 2027 (cho đội vận hành GPU)

> **Lượt chạy 26–30/10/2026 trên H100.** Hạn nộp bài là 31/10/2026, nên lịch ở mục "Lịch chạy" là lịch thật, không
> phải ví dụ. Chạy đúng commit chủ đề tài giao (`git log -1` phải trùng). Từ commit `6cc889a`, `configs/bm25.json` đã
> được dò và commit: **không chạy bước `tune_bm25`** (script tự bỏ qua bước này).

Tài liệu này dành cho người chạy máy GPU. Người chạy không cần hiểu phương pháp. Chỉ cần làm đúng thứ tự, kiểm tra kết
quả theo từng bảng, gửi về những gì mục "Báo sớm" yêu cầu và dừng lại ở những chỗ ghi **Dừng**.

Tóm tắt việc cần làm: một lượt giai đoạn 1, ba lượt giai đoạn 2, các mốc so sánh, đánh giá trên tập select và gate, một
quy tắc quyết định, rồi đúng **một lần** đánh giá trên tập test.

Nguyên tắc chung:

- Đừng sửa code trên máy chạy. Mỗi file `.meta.json` ghi `git_commit`; nếu cần sửa, báo chủ đề tài để có commit mới.
- Không đổi file trong `configs/` và không đổi quy tắc quyết định.
- Tập test (`data/tasks/viquad_test.jsonl`, `viquad_long_test.jsonl`) chỉ được đọc **một lần**, ở bước `test`, sau bước
  `decide`. Các bước lọc rò rỉ chỉ đọc phần ngữ cảnh của nó.
- Số liệu trong bài lấy từ H100 (bf16). Không dùng `DTYPE=float16` hay `QUANT=int4` trên cụm.
- Muốn bỏ, cắt bớt hay chạy lại lượt nào, phải hỏi chủ đề tài trước.
- Mọi lệnh chạy ở thư mục gốc của repo, trong `tmux` hoặc `screen`, ghi log bằng `tee`.

## Lịch chạy

Cần hai H100 (gọi là GPU 0 và GPU 1) trên cùng một máy. Thời gian là ước tính, suy từ lượt thử trên Kaggle T4 ngày
25–26/10/2026 và lượt thử H100 ngày 22/10/2026; số thật được đo ở lượt đầu và **phải báo sớm** (mục "Báo sớm").

| Ngày | GPU | Lệnh (`bash scripts/run_paper.sh …`) | Thời gian ước tính | Mục |
| --- | --- | --- | --- | --- |
| 26/10 | 0 | lượt thử `smoke_paper.sh` trong bản sao riêng | 30–45 phút | 2 |
| 26/10 | CPU | `data data_push template` | 1–2 giờ, cộng 10–20 phút tải lên | 3 |
| 26/10 | 0 | `g0 selector aie teacher teacher_push` | 1–1,5 giờ | 3, 4 |
| 27/10 | 0 | `stage1` | 2–3 giờ | 5 |
| 27/10 | 1 | `baselines` (song song với `stage1`) | 2–3 giờ | 6 |
| 28/10 | 0 và 1 | `stage2` (chỉ bắt đầu khi `baselines` đã xong) | 4–6 giờ | 5 |
| 28/10 | 1 | nếu còn thời gian: `stage2_q`, rồi `stage2_seed2` | 2–4 giờ mỗi bước | 5 |
| 29/10 | 0 và 1 | `eval_select choose eval_gate decide` | 3–5 giờ | 7 |
| 30/10 | 0 và 1 | `test figures`, rồi gửi kết quả | 2–4 giờ | 8, 10 |

`stage2_q` và `stage2_seed2` là tuỳ chọn; chỉ chạy khi chủ đề tài xác nhận còn kịp, và phải xong **trước**
`eval_select`. Chỉ có một H100: chạy mọi bước trên `GPUS="0"`, nối tiếp nhau, và bỏ `stage2_q`, `stage2_seed2`.

## Báo sớm (gửi ngay, không chờ hết lượt)

| Lúc | Gửi gì |
| --- | --- |
| Lượt thử (mục 2) xong | `logs/smoke_h100.log`; dòng cuối phải là `smoke: done` |
| Sau `data` | các dòng log của bảng kiểm tra ở mục 3 |
| Sau `data_push` và `teacher_push` | revision in ra (nội dung `data/hub_data_revision.txt`, `data/hub_teacher_revision.txt`) |
| 30 phút sau khi `stage1` bắt đầu | `tail -n 3 runs/paper/stage1/metrics.jsonl` (lấy `sec_per_step_recent`, `peak_mem_gb`), và kết quả của `nvidia-smi dmon -s u -c 30` |
| `baselines` xong | các file `results/paper/select/*/*.summary.json` (chỉ select; gate để sau) |
| 30 phút sau khi `stage2` bắt đầu | như với `stage1`, cho cả ba lượt `stage2_mem`, `stage2_prompt`, `stage2_frozen` |
| `decide` xong | `results/paper/gate/decision.json` và dòng `DECISION: …` cuối log |
| `test` xong | gói kết quả ở mục 10 |

Dòng `DECISION: FAIL` **không** phải lỗi và không làm dừng việc: vẫn chạy tiếp mục 8.

## Bài học từ lượt thử trên Kaggle T4 (25–26/10/2026)

- Mọi bước chạy được: kernel DeltaNet, bộ ghi đa tỉ lệ, mẫu nhiều đoạn, bộ chọn PhoBERT, LLMLingua-2. Trên một T4,
  giai đoạn 1 mất khoảng 8 s/bước và giai đoạn 2 khoảng 9,5 s/bước ở batch 16; bộ nhớ đỉnh dưới 9 GB.
- **Giai đoạn 2 bị CPU giới hạn một phần**: mỗi mẫu được tách từ (pyvi) và chọn câu bằng BM25 ngay trong tiến trình
  huấn luyện, nên GPU có lúc chỉ chạy 45–70%. Trên H100 phần CPU chiếm tỉ lệ lớn hơn: cấp cho job **ít nhất 8 lõi
  CPU**, và gửi kết quả `nvidia-smi dmon` như ở mục "Báo sớm".
- Toàn văn trên ViQuAD-Long (bài tới khoảng 18 nghìn token) hết bộ nhớ trên GPU 16 GB với lô mặc định; trên H100 80 GB
  thì không. Nếu vẫn gặp `CUDA out of memory` khi đánh giá, xem mục 11.
- Phiên Kaggle tự dừng sau 2,4 giờ và mất toàn bộ file. Trên cụm, **sao lưu sau mỗi bước** (mục 9).

## 0. Yêu cầu máy

| Hạng mục | Yêu cầu |
| --- | --- |
| GPU | 2 × H100 80 GB (bf16) trên cùng một máy. Một H100 cũng chạy được, nhưng chậm gần gấp đôi |
| CPU | Ít nhất 8 lõi cho job (giai đoạn 2 chọn câu trên CPU) |
| Hệ điều hành | Linux, có CUDA toolkit (`nvcc`) khớp với bản CUDA của torch, để build `causal-conv1d` |
| Đĩa | Nên có ≥ 100 GB trống: bộ nhớ đệm Hugging Face khoảng 30 GB; `data/` vài GB; `runs/` khoảng 1 GB mỗi checkpoint (khoảng 6 checkpoint) |
| RAM | ≥ 64 GB (hai lượt chạy song song, mỗi lượt nạp logit thầy vào RAM) |
| Mạng | Hugging Face Hub (Qwen3.5-2B và 9B, `vinai/phobert-base-v2`, `microsoft/llmlingua-2-xlm-roberta-large-meetingbank`, Wikipedia tiếng Việt, BKAINewsCorpus, UIT-ViQuAD 2.0, đều ghim revision) và `dl.fbaipublicfiles.com` (MLQA, chỉ để lọc rò rỉ). Tải lên Hub khoảng 5 GB (mục 3, 4) |
| Token | `HF_TOKEN` có quyền **ghi** vào repo dataset private `thanthienhai/vilatent-data` (chủ đề tài cấp; repo được tạo ở lần đẩy đầu nếu chưa có) |

## 1. Cài đặt

```bash
git clone https://github.com/thanthienhai/VILATENT.git && cd VILATENT
git checkout <commit được giao> && git log -1 --oneline
python -m venv .venv && source .venv/bin/activate
# transformers ghim ở 5.16.1; pyvi (tách từ tiếng Việt) đi kèm gói vilatent
pip install -e ".[dev,model,data,baselines,teacher]" "transformers==5.16.1" flash-linear-attention
TORCH_CUDA_ARCH_LIST=9.0 MAX_JOBS=8 pip install --no-build-isolation causal-conv1d
python -c "import torch, transformers, fla, causal_conv1d, pyvi; print(torch.__version__, transformers.__version__, torch.cuda.device_count())"
pytest -q                                   # 60 passed (CPU)
grep '"units"' configs/bm25.json            # phải in "units": "word"
export HF_TOKEN=...                         # token chủ đề tài cấp, có quyền ghi (không ghi vào file trong repo)
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

## 2. Lượt thử trên H100 (bắt buộc, khoảng 30–45 phút)

Lượt thử chạy mọi bước trên vài chục câu và 16 bước huấn luyện, để lỗi lộ ra trước khi tốn giờ GPU. Chạy trong **một
bản sao riêng** của repo: script ghi `data/`, `runs/`, `results/`, `configs/bm25.json`, `paper/figures/curves.tex`, và
từ chối chạy nếu `data/`, `runs/` hoặc `results/` đã có.

```bash
git clone . ../VILATENT-smoke && cd ../VILATENT-smoke
PYTHONPATH=$PWD DTYPE=bfloat16 GPUS="0" bash scripts/smoke_paper.sh 2>&1 | tee ../VILATENT/logs/smoke_h100.log
cd ../VILATENT && rm -rf ../VILATENT-smoke
```

Đạt khi dòng cuối của log là `smoke: done; …` và lệnh trả về exit 0. Dòng `DECISION: FAIL` là **bình thường** (16 bước
chưa học được gì); số liệu của lượt thử không dùng vào đâu. Lỗi: **Dừng**, gửi log.

## 3. Dữ liệu, template, G0 (B1, B4)

```bash
bash scripts/run_paper.sh data template 2>&1 | tee -a logs/data.log
GPUS="0" bash scripts/run_paper.sh g0 2>&1 | tee -a logs/g0.log
```

| Bước | Sinh ra | Kiểm tra |
| --- | --- | --- |
| `data` | `data/tasks/viquad_{train,gate,select,viwordc_dev,test}.jsonl`, `viquad_train_clean.jsonl`, `viquad_long_{gate,select,test}.jsonl`, `viquad_{train,select}_multi.jsonl`, `viquad_long_stats.json`, `data/eval_ext/*.jsonl`, `data/corpus/docs.jsonl`, `data/stage1/pairs_{train,dev}.jsonl`, mỗi file kèm `*.meta.json` | <ul><li>`viquad gate: 1228 answerable questions, 244 passages, 16 articles`, `viquad select: 621 …, 125 passages, 6 articles`, `viquad test: 2653 …, 557 passages, 19 articles`</li><li>Lọc rò rỉ in `{"n_input": 16318, "kept": 15706, "dropped": 612}`</li><li>`long test` in `"articles": 19`, `"answers_in_context": "2653/2653"`, `"duplicate_passages_removed": 0`, độ dài bài min 1.279, trung vị 4.470, max 18.327 token</li><li>`train_multi: {"questions": 15706, …}`</li><li>`pairs_train.jsonl` có 96.000 dòng</li><li>`sha256sum data/tasks/viquad_select.jsonl` bắt đầu bằng `cb88b5be8329` (khớp `configs/bm25.json`)</li></ul> |
| `template` | `configs/readers/qwen3.5-{2b,9b}.json` | `git diff configs/readers` phải rỗng; nếu khác, **Dừng** và báo |
| `g0` | `results/g0/Qwen_Qwen3.5-2B.json` | `G0_pass: true`; `load.deltanet_kernels` không có mục nào là `torch` |

Các con số trên đã được đo lại trên máy của chủ đề tài ngày 25/10/2026. Lệch số nào thì **Dừng** và báo, và **không**
chạy `data_push`. `data` chủ yếu chạy CPU: nó duyệt toàn bộ Wikipedia tiếng Việt và một phần BKAINewsCorpus.

Khi mọi dòng của bảng trên khớp, đẩy dữ liệu vừa dựng lên Hugging Face để lần sau dùng lại (mục 12):

```bash
bash scripts/run_paper.sh data_push 2>&1 | tee -a logs/data.log
```

Lệnh tải khoảng 2,5 GB (corpus chiếm gần hết) vào repo dataset private `thanthienhai/vilatent-data` trong một commit,
kèm `MANIFEST_data.json` (đường dẫn, cỡ và SHA-256 của từng file, commit git đã sinh ra chúng). Dòng cuối in
`{"repo": …, "bundle": "data", "revision": "<commit>"}`; revision cũng được ghi vào `data/hub_data_revision.txt`.
Gửi revision này về. Nếu log in `WARNING: the working tree is not a clean commit`, nghĩa là code trên máy đã bị sửa:
**Dừng** và báo.

## 4. Bộ chọn PhoBERT, đo đáp án trong văn bản, logit thầy (B3, B5, B6)

```bash
GPUS="0" bash scripts/run_paper.sh selector aie 2>&1 | tee -a logs/prep.log
GPUS="0 1" bash scripts/run_paper.sh teacher teacher_push 2>&1 | tee -a logs/prep.log
```

`teacher_push` đẩy 6 file logit thầy (khoảng 2–3 GB) vào cùng repo, kèm `MANIFEST_teacher.json`; gửi revision in ra
(`data/hub_teacher_revision.txt`).

| Bước | Việc | Sinh ra |
| --- | --- | --- |
| `selector` | huấn luyện bộ chọn câu PhoBERT (2 epoch), giữ checkpoint có loss nhỏ nhất trên select; khoảng 10 phút | `runs/paper/selector/` |
| `aie` | đo tỉ lệ đáp án vàng còn nguyên văn, bị cắt dở hoặc mất trong văn bản mỗi cách chọn giữ lại, trên select; chỉ CPU | `results/paper/select/answer_in_evidence.json` |
| `teacher` | top-20 log-prob của thầy (reader đọc toàn văn): cặp giai đoạn 1, ViQuAD train và select, mẫu nhiều đoạn train và select | `data/teacher/qwen3.5-2b/*.pt` (6 file) |

Không chạy `tune_bm25`: `configs/bm25.json` đã có `"units": "word"`, k1 = 2,0, b = 1,0 (dò trên select ngày
26/10/2026). Nếu lỡ gọi, script in `tune_bm25: … already tuned … skipped` và không làm gì.

## 5. Huấn luyện (B8, B9, B10, B13; B15, B17 nếu kịp)

Ngày 27/10, `stage1` trên GPU 0 và `baselines` (mục 6) trên GPU 1, hai cửa sổ tmux:

```bash
GPUS="0" bash scripts/run_paper.sh stage1 2>&1 | tee -a logs/train.log        # tmux 1
GPUS="1" bash scripts/run_paper.sh baselines 2>&1 | tee -a logs/baselines.log  # tmux 2
```

Ngày 28/10, khi **cả hai** đã xong, chạy `stage2` trên hai GPU:

```bash
GPUS="0 1" bash scripts/run_paper.sh stage2 2>&1 | tee -a logs/train.log
```

| Bước | Việc | Sinh ra |
| --- | --- | --- |
| `stage1` | một bộ ghi đa tỉ lệ (mỗi mẫu bốc ρ ∈ {4, 8, 16, 32}), 5.000 bước × batch 32 | `runs/paper/stage1/{best.pt,metrics.jsonl,config.json}` |
| `stage2` | ba lượt, mỗi lượt 4.000 bước: `stage2_mem` (ME/M, từ `stage1`) và `stage2_frozen` (bộ ghi đóng băng) trên GPU 0, `stage2_prompt` (đối chứng prompt, lr 1e-3) trên GPU 1 | `runs/paper/stage2_{mem,prompt,frozen}/…` |
| `stage2_q` (nếu kịp) | ViLatent-Q, chỉ r = 4, từ `stage1` | `runs/paper/stage2_q/…` |
| `stage2_seed2` (nếu kịp) | seed thứ hai của ME/M và của đối chứng prompt | `runs/paper/stage2_{mem,prompt}_s1/…` |

### Theo dõi khi huấn luyện

```bash
tail -n 3 runs/paper/*/metrics.jsonl
nvidia-smi dmon -s u -c 30          # mức dùng GPU trong 30 giây
```

- Dòng `start` liệt kê các cặp `(r, f)` được bốc (`pairs`) và số mẫu nhiều đoạn (`n_train_multi`, 15.706 ở `stage2`).
- Dòng `train` (mỗi 10 bước) có `loss`, `ce`, `kl`, `grad_norm`, `mem_norm` cạnh `emb_norm`, `sec_per_step_recent`,
  `peak_mem_gb`. `loss` phải hữu hạn; `mem_norm` không nên lệch `emb_norm` nhiều bậc. Bước đầu chậm (biên dịch kernel).
- Dòng `eval` (mỗi 250 bước) có `dev_loss`; ở giai đoạn 2 còn có `dev_single_loss` và `dev_multi_loss`. `best: true`
  nghĩa là `best.pt` vừa được ghi. Ở lượt thử T4, loss dev của `stage2_mem` thấp hơn rõ của `stage2_prompt`; nếu trên
  H100 sau 1.000 bước mà hai giá trị gần như bằng nhau, báo ngay.
- Nếu `stage2` chậm hơn khoảng 3 s/bước, hoặc GPU thường dưới 70%, báo chủ đề tài. Chủ đề tài có thể cho giảm tỉ lệ
  mẫu nhiều đoạn bằng `TRAIN_ARGS="--multi-share 0.15"` (không bao giờ về 0). Không tự đổi.

Huấn luyện **không có chế độ chạy tiếp**: lượt bị ngắt thì chạy lại đúng lệnh của lượt đó (in trong log ở dòng
`GPU <n>: python scripts/train.py --config …`). Khi một lượt lỗi, các lượt xếp sau nó trên cùng GPU không chạy và log in
`GPU <n>: skipped …`.

## 6. Mốc cứng (B7)

```bash
GPUS="1" bash scripts/run_paper.sh baselines 2>&1 | tee -a logs/baselines.log
```

Đánh giá full, none, truncation, lead, bm25, bm25_x2 (BM25 với ngân sách 2k, tầng 2 của MEF), phobert, llmlingua2 ở
4×, 8×, 16× trên select và gate, cho cả đoạn đơn và ViQuAD-Long, vào `results/paper/{select,gate}/{long,single}/`. Cần
`runs/paper/selector/` (mục 4). Toàn văn và LLMLingua-2 trên ViQuAD-Long là các lượt nặng nhất. Chạy lại thì các file
đã có được bỏ qua.

## 7. Chọn trên select, quyết định trên gate (B12)

```bash
GPUS="0 1" bash scripts/run_paper.sh eval_select choose eval_gate decide 2>&1 | tee -a logs/decide.log
```

| Bước | Việc | Sinh ra |
| --- | --- | --- |
| `eval_select` | ME/M, đối chứng prompt, bộ ghi đóng băng (và `stage2_q`, `_s1` nếu có) ở mọi (r, f) đã huấn luyện, trên select | `results/paper/select/{long,single}/…` |
| `choose` | f* = f có F1 select cao nhất, riêng cho từng thiết lập và từng r; rồi τ của MEF ở f* | `results/paper/select/choices.json`, `select/*/cascade_r*.json` |
| `eval_gate` | như `eval_select` trên gate, thêm bản đổi memory ở 4× | `results/paper/gate/{long,single}/…` |
| `decide` | MEF với τ đã chốt, báo cáo mọi thiết lập và tỉ lệ, rồi quy tắc quyết định | `results/paper/gate/*/report_r*.json`, `results/paper/gate/decision.json` |

Quy tắc quyết định (cố định ngày 25/10/2026, trước mọi lượt chạy): trên gate, ViQuAD-Long ở 4×, ViLatent-ME ở f* với
seed 0, đạt khi (1) F1 của ME trừ F1 mốc cứng tốt nhất (truncation, lead, LLMLingua-2, BM25, PhoBERT) ≥ 3 điểm và cận
dưới CI 95% (bootstrap theo bài) > 0; (2) cận dưới CI 95% của ME trừ đối chứng prompt > 0; (3) tỉ lệ câu trả lời không
đọc được dưới 2% với ME và mốc cứng tốt nhất. Dòng cuối log là `DECISION: PASS` hoặc `DECISION: FAIL`.

## 8. Test, một lần (B14)

```bash
GPUS="0 1" bash scripts/run_paper.sh test figures 2>&1 | tee -a logs/test.log
```

`test` đánh giá mọi phương pháp trên test (đoạn đơn và ViQuAD-Long, 4×/8×/16×), MEF với τ của select, báo cáo, F1 theo
vị trí đoạn chứa đáp án (`positions_r4.json`) và đo độ trễ (`latency_{long,single}.json`, batch 1). `figures` vẽ lại
`paper/figures/curves.tex`.

- Bước này từ chối chạy nếu chưa có `results/paper/gate/decision.json`, hoặc nếu `results/paper/test/` đã có file.
- Nếu nó dừng giữa chừng vì lỗi: **không xoá** `results/paper/test/`, gửi log về và chờ. Chủ đề tài có thể cho chạy tiếp
  bằng `TEST_RESUME=1` (các file đã xong không bị đánh giá lại).
- Lúc `latency.py` chạy (cuối bước), không chạy việc gì khác trên hai GPU này, kể cả của người khác.

## 9. Sao lưu sau mỗi bước

Sau mỗi bước của mục 4–8, chép sang ổ lưu trữ lâu dài (không phải ổ tạm của node), ví dụ:

```bash
BACKUP=/path/den/o/luu/tru/vilatent_paper     # thay bằng đường dẫn thật
rsync -a runs results logs "$BACKUP"/
rsync -a --include='*/' --include='*.meta.json' --include='*_stats.json' --exclude='*' data "$BACKUP"/
```

Không xoá `runs/paper/*/best.pt` và `data/` trên máy chạy cho tới khi chủ đề tài báo đã nhận đủ.

## 10. Gửi kết quả

```bash
tar czf vilatent_paper.tgz logs results/g0 results/paper runs/paper/*/metrics.jsonl runs/paper/*/config.json \
  runs/paper/selector/selector.json configs/bm25.json data/*/*.meta.json data/tasks/viquad_long_stats.json
```

Kèm `git rev-parse HEAD`, `pip freeze`, `nvidia-smi --query-gpu=name,memory.total --format=csv` và `nproc`. Gói
này nhỏ (vài chục MB). Checkpoint (`best.pt`, khoảng 1 GB mỗi file) chỉ gửi khi được yêu cầu.

QA sinh tự động (không thuộc bài báo): nếu còn thời gian sau mục 8, `bash scripts/run_paper.sh qa_download qa_filter`
(cần `HF_TOKEN` đọc được repo private `thanthienhai/vilatent-qa-gen`). Không chạy `qa_generate` trên cụm.

## 11. Sự cố thường gặp

| Triệu chứng | Nguyên nhân thường gặp | Cách xử lý |
| --- | --- | --- |
| `tune_bm25: … already tuned … skipped` | bình thường: BM25 đã dò và commit | không cần làm gì |
| `configs/bm25.json is not tuned for pyvi words yet` | file bị sửa hoặc checkout sai commit | `git checkout configs/bm25.json`; kiểm tra `git log -1` |
| `fast_deltanet_kernels: false`; trong `deltanet_kernels` có mục là `torch` | thiếu `flash-linear-attention` hoặc `causal-conv1d` | cài lại theo mục 1, rồi chạy lại `run_paper.sh g0` |
| `ModuleNotFoundError: pyvi` | cài thiếu | `pip install pyvi==0.1.1` |
| `the phobert baseline needs a trained selector` | chưa chạy `selector` | chạy `run_paper.sh selector` |
| `CUDA out of memory` khi huấn luyện | micro-batch 32 không vừa (mẫu nhiều đoạn dài hơn đoạn đơn) | giữ batch hiệu dụng, giảm micro-batch: `TRAIN_ARGS="--micro-batch 16"`, chạy lại đúng lượt đó; ghi lại trong báo cáo |
| `CUDA out of memory` khi đánh giá ViQuAD-Long | lô sinh quá lớn với bài dài | `EVAL_ARGS="--max-batch-tokens 16000"` (GPU nhỏ hơn: 9000) rồi chạy lại bước đó; các file đã xong được bỏ qua |
| `… was trained at ρ […]; this run pools at […]` | `stage2` khởi tạo từ checkpoint giai đoạn 1 khác | chạy lại `stage1` của commit này |
| `(r=…, f=…) was not trained` | đánh giá một cặp không có trong lượt huấn luyện | báo chủ đề tài (không sửa cấu hình) |
| `N examples have no teacher` | dữ liệu đổi sau khi chạy `teacher` | chạy lại `teacher` rồi các bước sau |
| `… was trained with BM25 {…}, not those of configs/bm25.json` | `configs/bm25.json` bị sửa sau khi đã huấn luyện | `git checkout configs/bm25.json`; báo chủ đề tài |
| `gradient check failed on the writer …`, `dev loss was never finite` | lỗi số học hoặc cài đặt | **Dừng**, gửi `logs/` và `runs/paper/<tên>/metrics.jsonl` |
| `test: … is not empty` | bước `test` đã chạy | không xoá gì, báo chủ đề tài |
| `data_push`/`teacher_push` lỗi 401 hoặc 403 | `HF_TOKEN` chưa đặt hoặc không có quyền ghi | xin chủ đề tài token có quyền ghi vào `thanthienhai/vilatent-data`, rồi chạy lại đúng bước đó (không cần dựng lại dữ liệu) |
| `data_pull`: `local files differ from …, not replacing them` | máy đã có `data/` từ một bản dựng khác | chuyển thư mục `data/` cũ đi chỗ khác (đừng xoá), rồi chạy lại |
| `files do not match the manifest after the download` | tải về hỏng | chạy lại `data_pull`; vẫn lỗi thì **Dừng** và báo |

## 12. Lần sau: dùng lại dữ liệu đã đẩy lên Hugging Face

Khi chủ đề tài giao `DATA_REVISION` (và `TEACHER_REVISION`), thay bước `data` (và `teacher`) bằng bước tải về:

```bash
DATA_REVISION=<commit> bash scripts/run_paper.sh data_pull template g0 2>&1 | tee -a logs/data.log
TEACHER_REVISION=<commit> bash scripts/run_paper.sh teacher_pull 2>&1 | tee -a logs/prep.log
```

`data_pull` tải đúng revision đó vào `data/` rồi so từng file với `MANIFEST_data.json` (cỡ và SHA-256); lệch một file là
dừng. Dòng cuối in `"verified": true` và commit git đã dựng dữ liệu (`built_at`). Logit thầy chỉ dùng lại được với cùng
template (`configs/readers/qwen3.5-2b.json`) và cùng dữ liệu; nếu không, bước huấn luyện báo `teacher computed with
another template` hoặc `N examples have no teacher`, và phải chạy lại `teacher`. Revision là mã commit, không phải tên
nhánh, nên dữ liệu không đổi dù repo có thêm lần đẩy mới.

## Phụ lục: biến môi trường của `scripts/run_paper.sh`

| Biến | Mặc định | Ý nghĩa |
| --- | --- | --- |
| `GPUS` | `0` | danh sách GPU; các lượt độc lập chia vòng tròn cho các GPU này |
| `DTYPE` | `bfloat16` | giữ mặc định trên H100 |
| `RATIOS` | `4 8 16` | giữ mặc định |
| `READER`, `READER_9B`, `SLUG` | `Qwen/Qwen3.5-2B`, `Qwen/Qwen3.5-9B`, `qwen3.5-2b` | giữ mặc định |
| `N_PAIRS`, `N_DEV_PAIRS`, `N_WIKI`, `N_NEWS` | 96.000, 1.000, 200.000, 200.000 | cỡ dữ liệu giai đoạn 1; giữ mặc định |
| `TRAIN_ARGS`, `EVAL_ARGS` | rỗng | chỉ dùng khi thiếu bộ nhớ (mục 11) hoặc khi chủ đề tài yêu cầu |
| `SELECTOR_ARGS`, `LATENCY_ARGS` | rỗng | dành cho `smoke_paper.sh` |
| `TEST_RESUME` | `0` | `1` cho phép chạy tiếp bước `test` bị ngắt, chỉ khi chủ đề tài đồng ý |
| `DATA_REPO` | `thanthienhai/vilatent-data` | repo dataset private chứa dữ liệu đã dựng và logit thầy; giữ mặc định |
| `DATA_REVISION`, `TEACHER_REVISION` | rỗng | commit cần tải ở `data_pull`, `teacher_pull` (mục 12) |
| `FORCE_TUNE` | `0` | chỉ `smoke_paper.sh` đặt `1`; **không dùng trên bản chạy thật** |
| `QUANT`, `G0_READERS`, `G0_ARGS` | `none`, reader 2B, rỗng | giữ mặc định; không dùng `QUANT=int4` trên cụm |
| `TEACHER_URL`, `TEACHER_MODEL`, `QA_REPO`, `QA_REVISION` | như G1 | chỉ cho phần QA sinh tự động |
