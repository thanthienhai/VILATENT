# Chạy bù các ô test còn thiếu (sau REPORT_VILATENT_2910)

Mục tiêu: hoàn tất bước 5 (`test figures`) của lần chạy `20261028` mà **không đổi bất cứ lựa chọn nào**.
Test vẫn là "đọc một lần": chỉ đánh giá các ô chưa có `*.summary.json`; ô đã có thì `--skip-existing` bỏ qua.

## 0. Không được làm

- Không đổi code: giữ đúng commit `9d71f3d` (mọi `.meta.json`/report ghi commit này).
- Không sửa, không xoá `results/paper/select/choices.json`, `results/paper/gate/decision.json`, hay bất kỳ file nào đã có trong `results/paper/test/`.
- Không chạy lại `eval_select`, `choose`, `eval_gate`, `decide`.
- Không thêm seed, không chạy `adv_*`.

## 1. Vì sao lần trước thiếu ô

`on_gpus` chia job vòng tròn: GPU 0 nhận job 1, 3, 5, 7, 9; GPU 1 nhận job 2, 4, 6, 8, 10. Một job trên GPU lỗi thì **các job sau của GPU đó bị bỏ qua**, và vì `set -e` nên `reports`, `position_report`, `latency` cũng không chạy.

| Job | Nội dung | GPU | Trạng thái |
|---|---|---|---|
| 1 | long: hard baselines r=4/8/16 | 0 | thiếu (node bị cordon) |
| 2 | long: trained r=4 | 1 | có |
| 3 | long: trained r=8 | 0 | thiếu (OOM) |
| 4 | long: trained r=16 | 1 | có |
| 5 | long: swap r=4 | 0 | **thiếu** (report không nhắc tới) |
| 6 | single: hard baselines | 1 | có |
| 7 | single: trained r=4 | 0 | thiếu (bị bỏ qua sau OOM) |
| 8 | single: trained r=8 | 1 | có |
| 9 | single: trained r=16 | 0 | thiếu (bị bỏ qua sau OOM) |
| 10 | single: swap r=4 | 1 | có |

Nếu chỉ chạy lại `TEST_RESUME=1 GPUS="0 1" ... test`, mọi job còn thiếu lại dồn hết vào GPU 0 và GPU 1 ngồi không. Nên chạy bù theo **mục 3** (hai hàng đợi cân bằng), sau đó mới chạy lại stage `test` để làm phần report.

## 2. Chuẩn bị

Pod như lần trước: pin node `dn24z`, 2× H100, 8 CPU / 64 GiB RAM, PVC `segspec-workspace` gắn vào repo.

```bash
cd VILATENT
git checkout 9d71f3d && git status --short     # không được có file code bị sửa
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
ls runs/paper/stage2_mem/best.pt runs/paper/stage2_prompt/best.pt runs/paper/stage2_frozen/best.pt runs/paper/selector
ls results/paper/select/choices.json results/paper/gate/decision.json
```

Nếu PVC mất dữ liệu: kéo `data`, `selector`, `teacher` từ Hub theo §6 của report, giải nén bundle `vilatent_step6_20261029_0410.tgz` để có lại `runs/paper/*` và `results/paper/*`.

Lưu danh sách file test hiện có (để sau đối chiếu cái gì là mới):

```bash
(cd results/paper/test && ls */*.summary.json | sort) > /tmp/test_before.txt
wc -l /tmp/test_before.txt
```

## 3. Chạy bù (hai GPU, hai hàng đợi)

```bash
R=Qwen/Qwen3.5-2B; CFG=configs/readers/qwen3.5-2b.json; RUNS=runs/paper; OUT=results/paper/test
C=results/paper/select/choices.json
ch() { python -c 'import json,sys; print(json.load(open(sys.argv[1]))["settings"][sys.argv[2]][sys.argv[3]][sys.argv[4]])' $C "$@"; }
EV="python scripts/evaluate.py --reader $R --reader-config $CFG --dtype bfloat16 --quant none --selector $RUNS/selector --skip-existing"
# EV="$EV --max-batch-tokens 16384"   # chỉ bật nếu OOM lại; ghi vào report nếu đã bật
soft() {  # setting, ratio: giống soft_at_choice của run_paper.sh
  echo "vilatent:$RUNS/stage2_mem/best.pt,f=1+$(ch $1 $2 f_star) vilatent:$RUNS/stage2_prompt/best.pt,f=$(ch $1 $2 f_star) vilatent:$RUNS/stage2_frozen/best.pt,f=$(ch $1 $2 frozen_f_star)"
}
mkdir -p logs

# GPU 0: hard baselines của Long (job 1)
CUDA_VISIBLE_DEVICES=0 $EV --data data/tasks/viquad_long_test.jsonl --ratios 4 8 16 --out-dir $OUT/long \
  --methods full none truncation lead bm25 bm25_x2 phobert llmlingua2 > logs/bu_gpu0.log 2>&1 &
P0=$!

# GPU 1: các job trained còn thiếu (job 3, 5, 7, 9), nối tiếp nhau
( set -e
  CUDA_VISIBLE_DEVICES=1 $EV --data data/tasks/viquad_long_test.jsonl --ratios 8  --out-dir $OUT/long   --methods $(soft long 8)
  CUDA_VISIBLE_DEVICES=1 $EV --data data/tasks/viquad_long_test.jsonl --ratios 4  --out-dir $OUT/long   --methods vilatent:$RUNS/stage2_mem/best.pt,f=$(ch long 4 f_star),swap=0
  CUDA_VISIBLE_DEVICES=1 $EV --data data/tasks/viquad_test.jsonl      --ratios 4  --out-dir $OUT/single --methods $(soft single 4)
  CUDA_VISIBLE_DEVICES=1 $EV --data data/tasks/viquad_test.jsonl      --ratios 16 --out-dir $OUT/single --methods $(soft single 16)
) > logs/bu_gpu1.log 2>&1 &
P1=$!

wait $P0; echo "GPU 0 rc=$?"; wait $P1; echo "GPU 1 rc=$?"
```

Nếu một lệnh OOM: bật dòng `--max-batch-tokens 16384` rồi chạy lại đúng lệnh đó (các ô đã xong vẫn được bỏ qua). Ghi rõ trong report là ô nào chạy với giá trị này.

## 4. Kiểm tra đủ ô trước khi làm report

```bash
python - <<'EOF'
import json, os
c = json.load(open("results/paper/select/choices.json"))["settings"]
hard = ["truncation", "lead", "bm25", "bm25_x2", "phobert", "llmlingua2"]
missing = []
for s in ("long", "single"):
    want = ["full", "none"] + [f"{h}_r{r}" for h in hard for r in (4, 8, 16)]
    for r in (4, 8, 16):
        e = c[s][str(r)]
        want += [f"vilatent_m_r{r}", f"vilatent_me_f{e['f_star']}_r{r}", f"prompt_bm25_f{e['f_star']}_r{r}"]
        if e["frozen_f_star"] is not None:
            want.append(f"frozen_me_f{e['frozen_f_star']}_r{r}")
    want.append(f"vilatent_me_f{c[s]['4']['f_star']}_swap_r4")
    missing += [f"{s}/{w}" for w in want if not os.path.exists(f"results/paper/test/{s}/{w}.summary.json")]
print("THIẾU:", missing if missing else "không")
EOF
```

Phải in `THIẾU: không` thì mới sang bước 5.

## 5. Report, latency, hình

Chạy lại đúng stage của pipeline. Mọi ô đánh giá đều đã có nên được bỏ qua; stage chỉ chạy `reports test` (cascade + paper_report), `position_report`, `latency` và `figures`.

```bash
TEST_RESUME=1 GPUS="0 1" bash scripts/run_paper.sh test figures 2>&1 | tee logs/test_resume.log
(cd results/paper/test && ls */*.summary.json | sort) > /tmp/test_after.txt
comm -13 /tmp/test_before.txt /tmp/test_after.txt > results/paper/test/BU_NEW_FILES.txt
```

Tiêu chí đạt: rc=0, có `results/paper/test/latency_long.json`, `latency_single.json`, `long/cascade_r4.json`, `single/cascade_r4.json`, `paper/figures/curves.tex` có số thật (không còn placeholder). `BU_NEW_FILES.txt` chỉ chứa các ô ở mục 1 có trạng thái "thiếu".

## 6. Gửi lại

Đóng gói `results/paper/test/`, `paper/figures/`, `logs/bu_gpu*.log`, `logs/test_resume.log`, đẩy lên Hub như bundle `results` lần trước. Gửi bảng F1/EM/unreadable của **mọi** ô trong `BU_NEW_FILES.txt`, kèm hai dòng tóm tắt in ra từ `paper_report.py` cho `test/long r=4` (các ΔF1 với CI ở cấp article).

Khi viết report, sửa ba chỗ của REPORT_VILATENT_2910:

- **τ = −∞** không có nghĩa là "ngưỡng không đạt được". Code (`vilatent/fallback.py`, `choose_tau`) chọn τ **nhỏ nhất** (điểm rẻ nhất) có F1 ≥ 0,95 × F1 full-context trên select; −∞ nghĩa là điểm rẻ nhất **đã** đạt tiêu chí, nên không cần ngưỡng log-prob. Với cascade, ở τ = −∞ vẫn còn kiểm tra answer-in-evidence: câu trả lời của ME không nằm nguyên văn trong evidence vẫn chuyển sang BM25 2k rồi full context. Nên MEF **không** trùng với ME; chỉ bản fallback log-prob mới trùng với ME.
- **Frozen f\* ở Long r=16 là 2, không phải 4.** Ở r=16 stage 2 chỉ huấn luyện f ∈ {1, 2} (ρ = r·f ≤ 32), nên `frozen_me_f2_r16` là đúng. Cột frozen_f\* trong bảng §4 của report gõ nhầm.
- **"Cluster"**: cluster chính của bootstrap là **bài báo** (16 bài ở gate, 19 bài ở test); 557 là số **đoạn** (cluster phụ). Swap check phải so `single/vilatent_me_f2_swap_r4` với `single/vilatent_me_f2_r4` (ô này sẽ có sau lần chạy bù), không so với Long.
