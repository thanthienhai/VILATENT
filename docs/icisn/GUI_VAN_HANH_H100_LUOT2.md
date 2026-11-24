# Gửi đội vận hành GPU — lượt 2 trên H100: ViLatent-M `m_swap` và `m_intact` (P1)

Ngày 2026-11-24. Mã: tag **`icisn-h100-v2`** trên `origin/main` (đã gồm bản vá tốc độ của lượt 1). Tài liệu chi tiết từng bước: `docs/icisn/YEU_CAU_VAN_HANH_H100.md` (bản 3). Tài liệu này là bản gửi đi: nó nói **cần gì, sửa gì trong script lượt 1, chạy thế nào, báo lại gì**.

Cảm ơn anh/chị về lượt 1 (`full`, `bm25_x2`, 14 phút, đủ 533 câu, SHA khớp). Lượt 2 cần số thật về **một** việc: bộ nhớ của ViLatent-M có mang nội dung riêng của từng bài không. Không huấn luyện.

## 1. Việc cần chạy

| Job | Nội dung | Tệp kết quả (`results/icisn_h100_memctl/p1/`) |
| --- | --- | --- |
| `m_swap` | ViLatent-M, mỗi câu đọc bộ nhớ của một bài khác | `vilatent_m_swap_r4.{jsonl,summary.json}` |
| `m_intact` | ViLatent-M nguyên vẹn, cùng cờ, cùng GPU, cùng bf16 | `vilatent_m_r4.{jsonl,summary.json}` |

Hai ô phải cùng phần cứng để hiệu số không lẫn hiệu ứng dtype. `MORE=1` thêm `m_zero`, `m_shuf` (thứ yếu; chỉ khi chúng tôi yêu cầu).

## 2. Khác lượt 1 — cần sửa script khởi tạo của anh/chị

| Mục | Lượt 1 | Lượt 2 |
| --- | --- | --- |
| Mã | ghim `icisn-h100-v1` (`a4ec1cc`), `git apply` bản vá `text.py` | **`git checkout icisn-h100-v2`**; **bỏ ghim `a4ec1cc` và bỏ `git apply`** (bản vá đã nằm trong mã, `git apply` sẽ lỗi) |
| Dữ liệu | `longctx_p1.jsonl` từ Hub | như cũ (SHA `52e01c31…20fc`) |
| Checkpoint | không cần | **cần** `runs/paper/stage2_mem/` từ `thanthienhai/vilatent-data` (`best.pt` SHA `3166c0aa…6dac1a`, 932 MB) |
| Lệnh chạy | `GPUS="0 1" bash scripts/icisn/run_h100.sh` | **`SET=memctl GPUS="0 1" bash scripts/icisn/run_h100.sh`** |
| Dọn claim | `rm -rf logs/h100/claim` | **không cần** (script tự làm) |
| RAM pod | 128Gi | **khuyến nghị 256Gi** (xem §3) |

Đoạn thay trong script khởi tạo (thay cho các dòng `git checkout … HEAD mismatch … git apply …`):

```bash
git fetch -q --tags origin; git checkout -q icisn-h100-v2 || die "checkout"
echo "== HEAD $(git rev-parse HEAD)"; git status --short            # phải sạch (trừ logs/ results/ runs/ data/)
python -c "from huggingface_hub import snapshot_download as d; d('thanthienhai/vilatent-data',repo_type='dataset',allow_patterns=['data/icisn/longctx_p1.jsonl','runs/paper/stage2_mem/*'],local_dir='.')" || die "download"
[ "$(sha256sum data/icisn/longctx_p1.jsonl | cut -d' ' -f1)" = 52e01c31cc0097660d900e6ce7bcaa1e525c83b0758df567f7cd97b34eca20fc ] || die "SHA data"
[ "$(sha256sum runs/paper/stage2_mem/best.pt | cut -d' ' -f1)" = 3166c0aaf5c13812a515341e2e5c62a9427cdb38f97e028a7f8c16e14c6dac1a ] || die "SHA ckpt"
```

Các bước cài thư viện giữ nguyên như lượt 1.

## 3. Tài nguyên và rủi ro đã biết

- **GPU:** 1–2× H100. **CPU:** 16 (như lượt 1).
- **RAM pod: xin 256Gi.** Một tiến trình M tăng đến ≈ 26 GB giữa chừng và ngoại suy đỉnh 45–50 GB (đo trên máy 1080 Ti, chưa đo trên H100). Hai tiến trình M từng bị hệ điều hành giết trên máy 62 GB. `dshm` 16 GiB tính vào giới hạn của pod.
- Nếu pod chỉ có < 200 GiB, script **tự chạy tuần tự trên một GPU**: vẫn đủ kết quả, lâu gấp đôi. Không cần anh/chị làm gì thêm.
- **Thời gian:** chưa đo. Ước 0,5–1 giờ mỗi job. Xin **không đặt `activeDeadlineSeconds` dưới 6 giờ.**

## 4. Hai giai đoạn (xin giữ đúng thứ tự)

**Giai đoạn A — thử nhanh (bắt buộc).** 12 câu, 3 bài, đủ ngữ cảnh 16k/32k/64k (có câu ≈ 75k token); kiểm được đường 64k và phép hoán đổi giữa các bài. Không dùng `LIMIT=12` (12 câu đầu cùng một bài).

```bash
python scripts/icisn/make_smoke_p1.py     # SHA-256 của data/icisn/longctx_p1_smoke.jsonl phải là 0a0ac70d5b630db3cccc0a0b2e9ddd3c742b34cf27fceb9a05c24ff8703d15de
SET=memctl GPUS="0" DATA=data/icisn/longctx_p1_smoke.jsonl OUT=results/icisn_h100_smoke_memctl/p1 \
  bash scripts/icisn/run_h100.sh 2>&1 | tee logs/h100_smoke_memctl.log
```

Đạt khi dòng cuối là `RESULT_COMPLETE set=memctl n=12`. Gửi lại: log, thời gian từng job, `logs/h100/rss_memctl.log` (RSS đỉnh), `nvidia-smi` đỉnh VRAM, `free -g`. **Kết quả thử không dùng làm số liệu. Xin dừng ở đây và chờ chúng tôi duyệt trước khi chạy thật.**

**Giai đoạn B — chạy thật (sau khi được duyệt).**

```bash
SET=memctl GPUS="0 1" bash scripts/icisn/run_h100.sh 2>&1 | tee logs/h100_memctl_main.log
```

Đạt khi dòng cuối là `RESULT_COMPLETE set=memctl n=533`.

## 5. Script tự đảm bảo chạy đủ

- Kiểm SHA-256 của `longctx_p1.jsonl`; sai thì dừng (exit 4). Dùng dữ liệu khác thì không được ghi vào thư mục kết quả chính.
- Ô thiếu hoặc sai số câu thì tự thử lại tối đa 2 lần; ô đã xong được giữ.
- Kết thúc luôn in **một** trong hai dòng: `RESULT_COMPLETE …` (exit 0) hoặc `RESULT_INCOMPLETE … thiếu: <ô>` (exit 1).
- Gián đoạn (pod bị đuổi, mất kết nối): chạy lại **cùng lệnh**, ô đã xong được bỏ qua.
- **Chỉ khi thấy `RESULT_COMPLETE` mới đóng gói và báo xong.** Thấy `RESULT_INCOMPLETE`: giữ nguyên log, báo lại, **không đổi cờ, không sửa mã, không chạy lại với cờ khác.**

## 6. Không được làm

Không đổi mã, cờ, dữ liệu hay checkpoint; không huấn luyện; không chạy P2/P3 hay điều kiện khác ngoài bốn job trên; không đặt `VILATENT_CHUNK_SDPA`; không đẩy dữ liệu hay checkpoint ra ngoài `thanthienhai/*`.

## 7. Gửi lại (sau giai đoạn B)

Đóng gói `results/icisn_h100_memctl/`, `logs/h100/`, `logs/h100_memctl_main.log`, `logs/h100_smoke_memctl.log` thành `icisn_h100_memctl_<ngày>.tgz`, kèm `sha256sum` và `git rev-parse HEAD`. Đẩy lên `thanthienhai/vilatent-results`, thư mục `icisn_h100_memctl_<ngày>/` (tách khỏi thư mục smoke và lượt 1). Kèm bảng thời gian, RSS đỉnh và VRAM đỉnh từng job. Chấm điểm bằng API và phân tích do chúng tôi làm.

## 8. Khi gặp sự cố

| Triệu chứng | Làm gì |
| --- | --- |
| `SAI SHA-256` hoặc `THIẾU …` | dừng, báo, không tự dựng lại dữ liệu |
| `RESULT_INCOMPLETE` | giữ log `logs/h100/memctl_*.log`, báo tên ô thiếu |
| OOM GPU ở một câu | ghi tên job và `id` câu, báo, không đổi cờ |
| tiến trình bị giết (`Killed`, rc=137) | script tự thử lại; nếu vẫn lỗi, gửi `rss_memctl.log` và `free -g` |
| `git apply` báo lỗi | bước này phải bỏ (xem §2) |
