# Nhờ đội vận hành GPU: chạy `full` và `bm25_x2` của ViLatent trên P1 (H100) — bản 2, phạm vi thu hẹp

Ngày soạn: 2026-11-18. **Bản nháp, chờ chủ đề tài duyệt và chốt cách giao dữ liệu (mục 3). Chưa gửi cho ai.** Mã đã đẩy lên `origin/main`, gắn tag `icisn-h100-v1`.
Đây là phần suy luận, **không huấn luyện**. Phạm vi đăng ký: `docs/icisn/PREREG_MORONG.md` (SHA-256 `6b27983487a6a43d9acf42d38abc237c607d775651bfc2646f7615849e5cef0b`) và `PREREG_MORONG_ERRATA.md` mục 4.
Đội vận hành chỉ cần chạy, kiểm đủ ô, gửi tệp; chấm bằng API và phân tích do chủ đề tài làm ở máy riêng.

## Vì sao chỉ hai điều kiện (bản 1 yêu cầu 13 job, đã bỏ)

Các phép kiểm soát bộ nhớ của ViLatent (swap/zero/shuf) và các điều kiện nguyên vẹn **đã chạy được trên GPU 1080 Ti của chủ đề tài** và là bộ chính đã đăng ký; chạy lại trên H100 chỉ tốn giờ GPU mà không thêm thông tin. H100 chỉ cần cho phần 1080 Ti không làm được: **`full`** (đọc cả bài 16k–64k token, hết bộ nhớ 11 GB) và **`bm25_x2`** (hai ô bị bỏ trong phần ngữ cảnh rất dài), cùng tùy chọn đối chiếu bf16.

## 0. Không được làm

- Không đổi mã, cờ, dữ liệu hay checkpoint. Máy ở đúng tag `icisn-h100-v1`, `git status --short` sạch (trừ `logs/`, `results/`).
- Không sửa/xóa `results/paper/`, không huấn luyện, không chạy P2/P3, không chạy swap/zero/shuf.
- Không đặt `VILATENT_CHUNK_SDPA` (chỉ cho GPU 11 GB).
- Không gửi dữ liệu, checkpoint hay kết quả ra ngoài nơi chủ đề tài chỉ định (`thanthienhai/vilatent-data` hoặc gửi trực tiếp).

## 1. Cần gì (ước lượng; chưa có số đo H100 trên dữ liệu này)

| Mục | Yêu cầu | Cơ sở |
| --- | --- | --- |
| GPU | 1–2× H100 (80 GB), một tiến trình mỗi GPU | 2 job (4 nếu bật `XCHECK=1`) |
| RAM máy chủ | ≥ 64 GiB là đủ | `full`/`bm25_x2` không giữ bộ nhớ ViLatent; chỉ ngữ cảnh văn bản |
| CPU | ≥ 8 lõi (bước `prepare` đơn luồng, ≈ 25–35 phút mỗi job trên máy 1080 Ti) | đo trên gpu1080 |
| Đĩa | ≥ 20 GiB (dữ liệu 105 MB, model ≈ 4–5 GB; checkpoint 0,9 GB chỉ cần nếu bật `XCHECK=1`) | |
| Mạng | tải `Qwen/Qwen3.5-2B` từ Hugging Face (hoặc cache); không cần API ngoài | |
| Thời gian | `full` 533 câu × 2–5 giây ≈ 0,3–0,75 GPU-giờ + `prepare` ≈ 0,5 giờ; `bm25_x2` ≈ 0,5–0,8 giờ. **≈ 1–2 GPU-giờ, ×1,5 dự phòng ≈ 2–3 GPU-giờ** (≈ 1–1,5 giờ lịch với 2 GPU). Bật `XCHECK=1`: thêm ≈ 1–2 GPU-giờ | ngoại suy từ 0,31 giây/câu ở ≈ 9,7k token (lượt 28–29/10); **cần bước thử mục 4** |

## 2. Lưu ý riêng cho `full`

Ô `full` ở 64k token là ô nặng nhất; trên T4 (15 GB) cần chia khối attention, trên H100 80 GB không cần. Nếu một câu OOM GPU: ghi tên job và `id` câu, **không đổi cờ**, báo lại. Mã đã có nhúng lười (`_LazyIds`) để không nhúng cả lô một lúc.

## 3. Chuẩn bị

```bash
cd VILATENT
git fetch --tags && git checkout icisn-h100-v1 && git rev-parse HEAD && git status --short
python -c "from huggingface_hub import snapshot_download; print(snapshot_download('Qwen/Qwen3.5-2B'))"
sha256sum data/icisn/longctx_p1.jsonl
ls configs/readers/qwen3.5-2b.json configs/bm25.json
nvidia-smi --query-gpu=index,name,memory.total --format=csv; free -g | sed -n 2p; nproc; df -h . | tail -1
```

| Tệp | SHA-256 |
| --- | --- |
| `data/icisn/longctx_p1.jsonl` (105 MB, 533 câu) | `52e01c31cc0097660d900e6ce7bcaa1e525c83b0758df567f7cd97b34eca20fc` |
| (chỉ nếu `XCHECK=1`) `runs/paper/stage2_mem/best.pt` | `3166c0aaf5c13812a515341e2e5c62a9427cdb38f97e028a7f8c16e14c6dac1a` |

Không khớp SHA thì dừng và báo. **Dữ liệu không nằm trong git** (`/data/` bị bỏ qua, và 105 MB vượt giới hạn 100 MB mỗi tệp của GitHub). Tệp `data/icisn/longctx_p1.jsonl` được giao riêng (chủ đề tài chốt: đẩy lên `thanthienhai/vilatent-data` hoặc gửi trực tiếp); đặt đúng đường dẫn đó trong thư mục repo rồi kiểm SHA ở trên. Tạo lại từ nguồn bằng `scripts/icisn/build_longctx.py` là khả thi nhưng cần dữ liệu thô ViQuAD/XQuAD-vi; không khuyến nghị.

## 4. Thử nhanh (bắt buộc, ≤ 20 phút, 1 GPU)

```bash
GPUS="0" LIMIT=12 OUT=results/icisn_h100_smoke/p1 bash scripts/icisn/run_h100.sh 2>&1 | tee logs/h100_smoke.log
```

Qua khi cả hai job có `rc=0`, không có `OutOfMemory`/`Traceback`/`Killed`, có `full.summary.json` và `bm25_x2_r4.summary.json` trong thư mục thử. Gửi lại `logs/h100_smoke.log` và thời gian từng job. **Kết quả thử không dùng làm số liệu.** Chủ đề tài chốt lệnh chạy thật sau khi nhận số thử; không tự chạy thật trước.

## 5. Chạy thật (sau khi được duyệt)

```bash
GPUS="0 1" bash scripts/icisn/run_h100.sh 2>&1 | tee logs/h100_main.log        # thêm XCHECK=1 nếu chủ đề tài yêu cầu
```

Gián đoạn: `rm -rf logs/h100/claim` rồi chạy lại; ô đã xong được bỏ qua.

## 6. Kiểm đủ ô

```bash
python - <<'PY'
import os, json
need = ["full", "bm25_x2_r4"]
miss = [n for n in need if not os.path.exists(f"results/icisn_h100/p1/{n}.summary.json")]
bad = [n for n in need if n not in miss and json.load(open(f"results/icisn_h100/p1/{n}.summary.json"))["n"] != 533]
print("THIẾU:", miss or "không", "| SAI n:", bad or "không")
PY
```

Phải in `THIẾU: không | SAI n: không`. Ô `full` tên `full.summary.json` (không `_r4`) là đúng, đừng đổi tên. Với `XCHECK=1` thêm `vilatent_m_r4`, `vilatent_me_f2_r4`.

## 7. Gửi lại

Đóng gói `results/icisn_h100/`, `logs/h100/`, `logs/h100_main.log`, `logs/h100_smoke.log` thành `icisn_h100_<ngày>.tgz`, kèm `sha256sum` của tệp đó và `git rev-parse HEAD`; gửi bảng thời gian từng job. Không cần gửi checkpoint.

## 8. Chưa nằm trong yêu cầu này

Huấn luyện seed hai và reader hai (WP3, WP4), P3 (chưa dựng), P2, đo độ trễ VRAM (WP6): chờ quyết định riêng.
