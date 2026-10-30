# Nhờ đội vận hành: đẩy checkpoint ViLatent lên Hugging Face (30/10/2026)

**Bối cảnh.** Checkpoint stage 2 của lần chạy `20261028` (code `9d71f3d`) chỉ nằm trên PVC `segspec-workspace`
của cluster `stg` / `llms-dev`. Trên `thanthienhai/vilatent-data` hiện chỉ có `data`, `teacher`, `selector` và
các bundle kết quả; chưa có `runs/paper/stage*`. Cần đẩy lên để đánh giá thêm (MLQA-vi) ngoài cluster.

**Không gấp trước hạn nộp 31/10.** Không chạy lại huấn luyện hay đánh giá nào; chỉ sao chép file.

## File cần đẩy

| Thư mục trên PVC | File | Bắt buộc |
|---|---|---|
| `runs/paper/stage2_mem/` | `best.pt`, `config.json`, `metrics.jsonl` | có (ViLatent-M/ME) |
| `runs/paper/stage2_prompt/` | `best.pt`, `config.json`, `metrics.jsonl` | có (learned prompt control) |
| `runs/paper/stage2_frozen/` | `best.pt`, `config.json`, `metrics.jsonl` | có (frozen writer) |
| `runs/paper/stage1/` | `best.pt`, `config.json`, `metrics.jsonl` | không bắt buộc (chỉ để lưu trữ) |

Nếu trong thư mục có các checkpoint trung gian (`step_*.pt`, `last.pt`, trạng thái optimizer) thì **không** cần đẩy.

## Lệnh (chạy trong repo VILATENT trên PVC, cần `HF_TOKEN` có quyền ghi vào `thanthienhai/vilatent-data`)

```bash
cd VILATENT
git rev-parse HEAD                      # phải là 9d71f3d...
ls -la runs/paper/stage1 runs/paper/stage2_mem runs/paper/stage2_prompt runs/paper/stage2_frozen

# SHA-256 để đối chiếu sau khi tải về
sha256sum runs/paper/stage*/best.pt runs/paper/stage*/config.json > runs/paper/CHECKPOINTS_SHA256.txt
cat runs/paper/CHECKPOINTS_SHA256.txt

for d in stage2_mem stage2_prompt stage2_frozen stage1; do
  hf upload thanthienhai/vilatent-data runs/paper/$d runs/paper/$d --repo-type dataset \
    --include "best.pt" "config.json" "metrics.jsonl" \
    --commit-message "checkpoints: runs/paper/$d (run 20261028, code 9d71f3d)"
done
hf upload thanthienhai/vilatent-data runs/paper/CHECKPOINTS_SHA256.txt runs/paper/CHECKPOINTS_SHA256.txt \
  --repo-type dataset --commit-message "checkpoints: sha256 (run 20261028)"
```

Nếu máy chỉ có `huggingface-cli` bản cũ, thay `hf upload` bằng `huggingface-cli upload` với cùng tham số.

## Gửi lại

- Nội dung `runs/paper/CHECKPOINTS_SHA256.txt` và kích thước từng `best.pt`.
- Commit id trên Hub sau lần upload cuối (`hf` in ra khi xong).
