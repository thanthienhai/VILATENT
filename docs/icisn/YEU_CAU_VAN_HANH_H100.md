# Nhờ đội vận hành GPU: lượt 2 trên H100 — phép kiểm soát nội dung bộ nhớ của ViLatent-M (`m_swap`, `m_intact`)

Bản 3, soạn 2026-11-23. Lượt 1 (`full`, `bm25_x2`, SET=text) đã xong, kết quả ở `thanthienhai/vilatent-results/icisn_h100_main_20261123/`. Tài liệu này chỉ nói về lượt 2.
Đây là phần suy luận, **không huấn luyện**. Phạm vi đăng ký: `docs/icisn/PREREG_MORONG.md` (SHA-256 `6b27983487a6a43d9acf42d38abc237c607d775651bfc2646f7615849e5cef0b`) và `PREREG_MORONG_ERRATA.md` mục 5.
Đội vận hành chỉ cần chạy, kiểm đủ ô, gửi tệp; chấm bằng API và phân tích do chủ đề tài làm ở máy riêng.

## 0. Việc cần làm và vì sao

Một giả thuyết đã đăng ký cần số mới: **C1** (bộ nhớ của M có mang nội dung riêng của bài không: M nguyên vẹn so với M đọc bộ nhớ của bài khác). Cần hai ô, cùng GPU, cùng dtype:

| Job | Nội dung | Tệp kết quả |
| --- | --- | --- |
| `m_swap` | M, mỗi câu đọc bộ nhớ của một bài khác (`swap=0`) | `vilatent_m_swap_r4.{jsonl,summary.json}` |
| `m_intact` | M nguyên vẹn, cùng cờ | `vilatent_m_r4.{jsonl,summary.json}` |

Hai ô phải chạy cùng H100 bf16 để hiệu số không lẫn hiệu ứng dtype. `MORE=1` thêm `m_zero`, `m_shuf` (thứ yếu, tùy chọn; chỉ chạy nếu đã xong hai job chính và còn thời gian).

## 1. Không được làm

- Không đổi mã, cờ, dữ liệu hay checkpoint. Máy ở đúng `main` mới nhất (đã gộp bản vá tốc độ `f6f6424`); `git status --short` sạch (trừ `logs/`, `results/`, `runs/`, `data/`).
- Không huấn luyện, không chạy P2/P3, không chạy điều kiện khác ngoài bốn job trên, không đặt `VILATENT_CHUNK_SDPA`.
- Không đẩy dữ liệu hay checkpoint ra ngoài `thanthienhai/*` trên Hub.

## 2. Tài nguyên (ước lượng; chưa đo M trên H100)

| Mục | Yêu cầu | Cơ sở |
| --- | --- | --- |
| GPU | 1–2× H100 80 GB, một tiến trình mỗi GPU | 2 job chính |
| **RAM máy chủ** | **≥ 128 GiB nếu chạy hai GPU song song; ≥ 64 GiB nếu chạy một GPU** | một tiến trình M tăng đến ≈ 26 GB ở 55% bước ghi bộ nhớ, ngoại suy đỉnh 45–50 GB (đo trên máy 1080 Ti, chưa đo trên H100); hai tiến trình M từng bị hệ điều hành giết vì hết RAM trên máy 62 GB |
| CPU | ≥ 8 lõi | |
| Đĩa | ≥ 20 GiB (model ≈ 4–5 GB, checkpoint 0,9 GB, dữ liệu 105 MB) | |
| Thời gian | **chưa có số đo.** Bước chuẩn bị ngữ cảnh nay chỉ vài phút sau bản vá; lượt 1 hai job mất ≈ 14 phút. Tạm ước ≈ 0,5–1 giờ mỗi job; ≈ 1–2 GPU-giờ cho hai job chính | cần bước thử §5 |

Nếu `free -g` cho thấy RAM < 128 GiB: chạy `GPUS="0"` (hai job tuần tự trên một GPU) để tránh bị giết.

## 3. Chuẩn bị

```bash
cd VILATENT
git fetch --tags origin && git checkout main && git pull --ff-only && git rev-parse HEAD   # báo lại commit
python -c "from huggingface_hub import snapshot_download as d; d('thanthienhai/vilatent-data',repo_type='dataset',allow_patterns=['data/icisn/longctx_p1.jsonl','runs/paper/stage2_mem/*'],local_dir='.')"
sha256sum data/icisn/longctx_p1.jsonl runs/paper/stage2_mem/best.pt
ls configs/readers/qwen3.5-2b.json configs/bm25.json runs/paper/stage2_mem/config.json
nvidia-smi --query-gpu=index,name,memory.total --format=csv; free -g | sed -n 2p; nproc; df -h . | tail -1
```

| Tệp | SHA-256 |
| --- | --- |
| `data/icisn/longctx_p1.jsonl` (105 MB, 533 câu) | `52e01c31cc0097660d900e6ce7bcaa1e525c83b0758df567f7cd97b34eca20fc` |
| `runs/paper/stage2_mem/best.pt` (932 MB) | `3166c0aaf5c13812a515341e2e5c62a9427cdb38f97e028a7f8c16e14c6dac1a` |

Không khớp SHA thì dừng và báo. Dữ liệu đã được dùng ở lượt 1 (SHA khớp), checkpoint cùng repo `thanthienhai/vilatent-data`.

## 4. Thử nhanh (bắt buộc, 1 GPU)

```bash
SET=memctl GPUS="0" LIMIT=12 OUT=results/icisn_h100_smoke_memctl/p1 bash scripts/icisn/run_h100.sh 2>&1 | tee logs/h100_smoke_memctl.log
```

Qua khi cả hai job `rc=0`, không có `OutOfMemory`/`Traceback`/`Killed`, có `vilatent_m_swap_r4.summary.json` và `vilatent_m_r4.summary.json`. **Gửi lại**: log, thời gian từng job, **RSS đỉnh của tiến trình Python** (ví dụ `/usr/bin/time -v` hoặc theo dõi `ps -o rss`) và `nvidia-smi` đỉnh VRAM. Kết quả thử không dùng làm số liệu. Chủ đề tài chốt lệnh chạy thật sau khi nhận số thử; **không tự chạy thật trước.**

## 5. Chạy thật (sau khi được duyệt)

```bash
SET=memctl GPUS="0 1" bash scripts/icisn/run_h100.sh 2>&1 | tee logs/h100_memctl_main.log     # hoặc GPUS="0" nếu RAM < 128 GiB
# MORE=1 thêm m_zero, m_shuf (chỉ nếu chủ đề tài yêu cầu)
```

Gián đoạn: `rm -rf logs/h100/claim_memctl` rồi chạy lại; ô đã xong được bỏ qua. Nếu một tiến trình bị giết vì RAM, **không đổi cờ**, chạy lại bằng `GPUS="0"` và báo.

## 6. Kiểm đủ ô

```bash
python - <<'PY'
import os, json
need = ["vilatent_m_swap_r4", "vilatent_m_r4"]
d = "results/icisn_h100_memctl/p1"
miss = [n for n in need if not os.path.exists(f"{d}/{n}.summary.json")]
bad = [n for n in need if n not in miss and json.load(open(f"{d}/{n}.summary.json"))["n"] != 533]
print("THIẾU:", miss or "không", "| SAI n:", bad or "không")
PY
```

Phải in `THIẾU: không | SAI n: không`. Với `MORE=1` thêm `vilatent_m_zero_r4`, `vilatent_m_shuf_r4`.

## 7. Gửi lại

Đóng gói `results/icisn_h100_memctl/`, `logs/h100/`, `logs/h100_memctl_main.log`, `logs/h100_smoke_memctl.log` thành `icisn_h100_memctl_<ngày>.tgz`, kèm `sha256sum` và `git rev-parse HEAD`. Đẩy lên `thanthienhai/vilatent-results`, thư mục `icisn_h100_memctl_<ngày>/` (tách khỏi các thư mục smoke và lượt 1). Kèm bảng thời gian và RSS/VRAM đỉnh từng job. Không cần gửi checkpoint.

## 8. Chưa nằm trong yêu cầu này

Huấn luyện seed hai và reader hai (WP3, WP4), P3 (chưa dựng), P2, đo độ trễ VRAM (WP6): chờ quyết định riêng.
