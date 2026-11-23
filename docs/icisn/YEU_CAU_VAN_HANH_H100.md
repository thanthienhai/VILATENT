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
| GPU | 1–2× H100 80 GB | 2 job chính |
| **RAM của pod** | **Khuyến nghị `requests`/`limits` memory = 256Gi** (lượt 1 dùng 128Gi). Dưới 200 GiB, script tự chạy hai job **tuần tự trên một GPU** để không bị giết; vẫn đủ kết quả, chỉ lâu gấp đôi | một tiến trình M tăng đến ≈ 26 GB ở 55% bước ghi bộ nhớ, ngoại suy đỉnh 45–50 GB (đo trên máy 1080 Ti, chưa đo trên H100); hai tiến trình M từng bị hệ điều hành giết vì hết RAM trên máy 62 GB. `dshm` 16 GiB tính vào giới hạn RAM của pod |
| CPU | ≥ 8 lõi (lượt 1 dùng 16) | |
| Đĩa | ≥ 20 GiB (model ≈ 4–5 GB, checkpoint 0,9 GB, dữ liệu 105 MB) | |
| Thời gian | **chưa có số đo.** Bước chuẩn bị ngữ cảnh nay chỉ vài phút sau bản vá; lượt 1 hai job mất ≈ 14 phút. Tạm ước ≈ 0,5–1 giờ mỗi job; **không đặt giới hạn thời gian cứng (`activeDeadlineSeconds`) dưới 6 giờ** | cần bước thử §4 |

## Bảo đảm chạy đủ (đã tích hợp trong `run_h100.sh`)

- Tự kiểm SHA-256 của `longctx_p1.jsonl` trước khi chạy thật; sai thì dừng (exit 4), không tính kết quả.
- Nếu RAM dùng được (cgroup) < 200 GiB và có hai GPU: tự chạy tuần tự trên GPU đầu. `FORCE_PARALLEL=1` để bỏ qua (không khuyến nghị).
- Sau khi chạy xong, tự kiểm đủ ô và đủ `n`; ô thiếu hoặc bị giết thì **tự thử lại tối đa 2 lần** (ô đã xong được giữ nguyên).
- Cuối cùng in đúng một trong hai dòng: `RESULT_COMPLETE set=memctl n=533 ...` (exit 0) hoặc `RESULT_INCOMPLETE ... thiếu: <tên ô>` (exit 1). **Chỉ khi thấy `RESULT_COMPLETE` mới được đóng gói và báo xong.** Nếu thấy `RESULT_INCOMPLETE`: giữ nguyên log, báo lại, **không đổi cờ**.
- Có thể chạy lại cùng lệnh bất cứ lúc nào sau gián đoạn: hàng đợi tự khởi tạo lại, ô đã xong được bỏ qua.
- Tự ghi RSS đỉnh vào `logs/h100/rss_memctl.log` (15 giây một lần).

## 3. Chuẩn bị

```bash
cd VILATENT
git fetch --tags origin && git checkout <COMMIT> && git rev-parse HEAD   # <COMMIT> do chủ đề tài báo; trước đó phải là `main`. Script khởi tạo của lượt 1 ghim `icisn-h100-v1` và vá bằng `git apply`: BỎ cả hai (bản vá đã nằm trong main)
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

Tập thử gồm 12 câu, 3 bài, đủ ngữ cảnh 16k/32k/64k (có câu tới ≈ 75k token), nên kiểm được đường 64k và phép hoán đổi bộ nhớ giữa các bài (cần ≥ 2 bài). Không dùng `LIMIT=12` (12 câu đầu cùng một bài, phép swap không có ý nghĩa).

```bash
python scripts/icisn/make_smoke_p1.py          # tạo data/icisn/longctx_p1_smoke.jsonl; SHA-256 phải là 0a0ac70d5b630db3cccc0a0b2e9ddd3c742b34cf27fceb9a05c24ff8703d15de
SET=memctl GPUS="0" DATA=data/icisn/longctx_p1_smoke.jsonl OUT=results/icisn_h100_smoke_memctl/p1   bash scripts/icisn/run_h100.sh 2>&1 | tee logs/h100_smoke_memctl.log
```

Qua khi in `RESULT_COMPLETE set=memctl n=12`. **Gửi lại**: log, thời gian từng job, `logs/h100/rss_memctl.log` (RSS đỉnh), `nvidia-smi` đỉnh VRAM và `free -g`. Kết quả thử không dùng làm số liệu. Chủ đề tài chốt lệnh chạy thật sau khi nhận số thử; **không tự chạy thật trước.**

## 5. Chạy thật (sau khi được duyệt)

```bash
SET=memctl GPUS="0 1" bash scripts/icisn/run_h100.sh 2>&1 | tee logs/h100_memctl_main.log
# MORE=1 thêm m_zero, m_shuf (chỉ nếu chủ đề tài yêu cầu)
```

Dòng cuối phải là `RESULT_COMPLETE set=memctl n=533`. Nếu bị gián đoạn (pod bị đuổi, mất kết nối): chạy lại cùng lệnh. Nếu một tiến trình bị giết vì RAM, **không đổi cờ**; script tự thử lại trên một GPU.

## 6. Kiểm đủ ô

Đã nằm trong script (`RESULT_COMPLETE`). Kiểm tay thêm cho chắc:

```bash
ls -l results/icisn_h100_memctl/p1/vilatent_m_swap_r4.summary.json results/icisn_h100_memctl/p1/vilatent_m_r4.summary.json
grep -h '"n"' results/icisn_h100_memctl/p1/*.summary.json     # cả hai phải là 533
```

Với `MORE=1` thêm `vilatent_m_zero_r4`, `vilatent_m_shuf_r4`.

## 7. Gửi lại

Đóng gói `results/icisn_h100_memctl/`, `logs/h100/`, `logs/h100_memctl_main.log`, `logs/h100_smoke_memctl.log` thành `icisn_h100_memctl_<ngày>.tgz`, kèm `sha256sum` và `git rev-parse HEAD`. Đẩy lên `thanthienhai/vilatent-results`, thư mục `icisn_h100_memctl_<ngày>/` (tách khỏi các thư mục smoke và lượt 1). Kèm bảng thời gian và RSS/VRAM đỉnh từng job. Không cần gửi checkpoint.

## 8. Chưa nằm trong yêu cầu này

Huấn luyện seed hai và reader hai (WP3, WP4), P3 (chưa dựng), P2, đo độ trễ VRAM (WP6): chờ quyết định riêng.
