# G0 — Kiểm kê và kiểm tái lập (không có kết quả mới)

Ngày: 2026-11-07. Không gọi API. Mọi đầu ra nằm trong `results/icisn/g0/`, `scripts/icisn/`, `data/icisn/xquad_raw/`.

## 0.1 SHA-256 checkpoint

| File | Kết quả |
|---|---|
| `runs/paper/stage2_mem/best.pt` | khớp `CHECKPOINTS_SHA256.txt` (`3166c0aa…c1a`, đủ 64 ký tự trong `CHECKPOINTS_SHA256.txt`), cục bộ và gpu1080 |
| `runs/paper/stage2_prompt/best.pt` | khớp (`aa0808ea…567f`, đủ 64 ký tự trong `CHECKPOINTS_SHA256.txt`), cục bộ và gpu1080 |
| `stage2_mem/config.json`, `stage2_prompt/config.json` | khớp |
| `stage1/best.pt`, `stage2_frozen/best.pt` | **không có trên máy này** (không cần cho G1–G4) |

Code `vilatent/*.py`, `scripts/evaluate.py`, `configs/bm25.json`, `configs/readers/qwen3.5-2b.json` trên gpu1080 giống hệt bản cục bộ (so SHA từng file).

## 0.2 Tái lập fp16 so với H100 (bf16) — 200 câu test đầu, 4×

Dự đoán H100 lấy từ `results/paper/test/{single,long}`. So theo `id`. Bảng đầy đủ: `results/icisn/g0/compare.json`.

| Ô | Thiết bị | n | ΔF1 | Dự đoán trùng | EM mới / H100 |
|---|---|---|---|---|---|
| Đoạn đơn, M | GTX 1080 Ti | 200 | −0,02 | 93,5% | 30,0 / 30,0 |
| Đoạn đơn, ME f=2 | GTX 1080 Ti | 200 | +0,48 | 93,0% | 25,0 / 25,0 |
| Long, M | **Tesla T4** | 200 | +0,78 | 93,0% | 15,5 / 15,0 |
| Long, ME f=2 | **Tesla T4** | 200 | −0,57 | 96,0% | 30,5 / 31,0 |

**Kết luận:** không ô nào vượt ngưỡng |ΔF1| > 1,0, nên không dừng.

**Giới hạn (phải ghi vào bài):**
1. Ô Long chạy trên **T4, không phải 1080 Ti**. 1080 Ti bị OOM hai lần vì GPU dùng chung (người khác chiếm ~5 GB trên GPU1, ~10 GB trên GPU0). T4 cho biết fp16 nói chung không làm lệch, nhưng chưa chứng minh 1080 Ti (Pascal) cho cùng kết quả ở Long. **Việc cần làm lại khi 1080 Ti rảnh:** `KINDS=long BS=2 bash scripts/icisn/g0_run.sh <gpu> 1000`.
2. Phiên bản thư viện khác nhau: gpu1080 torch 2.6.0 / transformers 5.12.1; Kaggle T4 torch 2.11.0 / transformers 5.16.1. H100 chưa ghi lại trong báo cáo này.
3. 200 câu đầu của tập đoạn đơn thuộc **một bài duy nhất** (58 cụm); mẫu hẹp. Ô Long cũng chỉ gồm vài bài đầu.
4. Chỉ kiểm ME f=2 và M ở 4×; chưa kiểm 8×, 16×, prompt và các điều kiện văn bản.

## 0.3 Tốc độ và bộ nhớ

| Điều kiện (200 câu × 2: M và ME f=2, gồm thời gian nạp mô hình) | Thiết bị | Thời gian | Đỉnh VRAM |
|---|---|---|---|
| Đoạn đơn 4× | GTX 1080 Ti | 205 s (~0,5 s/câu/điều kiện) | 5,4 GB |
| Đoạn đơn 4× | T4 | 136 s | 5,4 GB |
| Long 4× (batch 4, mbt 6000) | T4 | 1876 s (~4,7 s/câu/điều kiện) | 9,85 GB (reserved 9,92) |

- **Độ dài tối đa đọc được với 11 GB (toàn văn, ME): CHƯA ĐO.** Cần 1080 Ti trống. Gợi ý: ViQuAD-Long test có bài trung bình ~9,7k token (có bài ~18k theo chú thích trong `vilatent/evaluate.py`); đỉnh 9,85 GB ở ME/M trên T4 gần sát 11 GB, nên toàn văn ở bài dài nhất có nguy cơ không vừa. Chưa có số đo.
- Tốc độ Long trên 1080 Ti chưa đo (Pascal không có tensor core fp16 nhanh; kỳ vọng chậm hơn T4, chưa xác minh).
- 1080 Ti dùng chung: tiến trình của người khác (llama-server, uvicorn, `ghard3.py`, `methods.py`) chiếm 5–10 GB mỗi GPU. Tôi không đụng đến chúng.

## 0.4 XQuAD tiếng Việt

- **Nguồn chính thức:** `github.com/google-deepmind/xquad`, file `xquad.vi.json` (đã tải trực tiếp, commit gần nhất của file `99910ec0f10151652f6726282ca922dd8eb0207a`, 2019-11-21). Bài gốc: Artetxe et al., *On the Cross-lingual Transferability of Monolingual Representations* (arXiv 1910.11856), theo README.
- **Giấy phép:** CC BY-SA 4.0 (theo README của repo; API GitHub không có file LICENSE riêng).
- **Quy mô** (đếm từ file): 48 bài, 240 đoạn, 1190 cặp hỏi–đáp. Khớp với README (240/1190). Không có câu không trả lời được (dựa trên SQuAD v1.1).
- **SHA-256:** `f619a1eb11fb42d3ab0834259e488a65f585447ef6154437bfb7199d85161a04` (`data/icisn/xquad_raw/xquad.vi.json`).
- **Chồng lấn** (`scripts/icisn/xquad_overlap.py`, 8-gram từ đã chuẩn hóa NFC; chi tiết `results/icisn/g0/xquad_overlap.txt`):

| So với | Đoạn có ≥1 8-gram trùng | Đoạn trùng ≥50% | Trùng tối đa |
|---|---|---|---|
| UIT-ViQuAD (mọi split, 15 780 đoạn duy nhất) | 10/240 | **0/240** | 24% |
| Corpus stage 1 (Wikipedia tiếng Việt, `data/corpus/docs.jsonl`) | 169/240 | **6/240** | 84% |

  Khớp nguyên chuỗi đoạn văn và khớp câu hỏi với mọi file `viquad_*` và `mlqa_vi_*`: 0 trùng.
- **Kết luận:** XQuAD-vi **không chồng lấn đáng kể với UIT-ViQuAD** (điều kiện đạt). Nhưng **chưa "chưa-thấy" hoàn toàn với writer**: nhiều đoạn dịch có nội dung giống các bài Wikipedia tiếng Việt trong corpus stage 1, mà writer đã học tái tạo ở stage 1. Writer không học câu hỏi hay đáp án của XQuAD, nên mức rò rỉ thấp, nhưng đây là một yếu tố đe dọa tính hợp lệ.
- **Đề xuất (chờ bạn duyệt, ghi vào PREREG_CONFIRM nếu đồng ý):** báo kết quả trên đủ 240 đoạn là chính; thêm phân tích độ nhạy loại 6 đoạn trùng ≥50% với corpus stage 1. Quy tắc loại phải ghi trước khi chạy reader.

## 0.5 Ước lượng giờ GPU và số lời gọi API cho G1–G4

Cơ sở: số đo ở 0.3, số dòng dự đoán hiện có, kích thước tập. Đây là ước lượng thô, sai số ±50%.

### Số lời gọi API (LLM)

| Việc | Ước lượng |
|---|---|
| G1 chấm lại dự đoán cũ (261 884 dòng; sau khi khử trùng lặp bộ ba câu hỏi–đáp án–dự đoán còn **~99 000**) | ~99 000 (người chấm chính) |
| G1 hiệu chỉnh 60 câu, hai người chấm | ~120 |
| G1 người chấm phụ trên dự đoán cũ | không chạy toàn bộ; chỉ nếu bạn muốn (+~99 000) |
| G2 tóm tắt Sum: ~560 đoạn đơn + 19 bài Long (test) + 240 đoạn + 48 bài (XQuAD) ≈ 870 tài liệu; tập select (125 đoạn + 6 bài) × tối đa 3 biến thể ≈ 400 | ~1 300 |
| G4 chấm dự đoán mới, chính: ViQuAD ~56 000 + XQuAD 4× ~26 000 (+ 8×/16× ~52 000 nếu chấm) | 82 000 – 134 000 |
| G4 người chấm phụ trên dự đoán xác nhận 4× | ~26 000 |
| **Tổng** | **~210 000 – 360 000 lời gọi**, đa số là lời chấm ngắn (vài trăm token) |

Bộ nhớ đệm (cache của `llm_client.py`) sẽ giảm số lời gọi thực nếu dự đoán lặp.

### Giờ GPU (suy luận, GTX 1080 Ti, một GPU rảnh)

Giả định: ~0,5 s/câu/điều kiện cho đọc văn bản và đoạn đơn (số đo 0.3); Long có writer ~5–9 s/câu/điều kiện (4,7 s trên T4; 1080 Ti chưa đo). Điều kiện Sum/Sum+E/bge-m3 đọc văn bản ngắn nên ~0,6–1 s/câu.

| Giai đoạn | Việc | Giờ ước lượng |
|---|---|---|
| G0 làm lại | Long 4× trên 1080 Ti (200 câu) | ~1 |
| G4.1 | ViQuAD test: Sum, Sum+E, bge-m3 × 6 ô (47 800 lượt đọc) + prompt f tốt nhất đoạn đơn × 3 (8 000) | 9 – 14 |
| G4.2 | XQuAD-vi 4×: ~11 điều kiện × 1190 × 2 bản (≈ 26 000) | 4 – 6 |
| G4.2 | XQuAD-vi 8× và 16× (mô tả, ≈ 52 000) | 8 – 12 (có thể cắt) |
| Chọn câu bge-m3, nhúng, chuẩn bị | nhỏ | ~1 |
| **Tổng G4 (không 8×/16×)** | | **~14 – 22 giờ** |
| **Tổng G4 (có 8×/16×)** | | **~22 – 34 giờ** |

- Nếu cả hai 1080 Ti rảnh và chia hàng đợi: nửa thời gian trên. Hiện cả hai bị chiếm 5–10 GB mỗi GPU; Long trên 11 GB chưa chắc chạy được. Kaggle T4 là phương án dự phòng (30 giờ/tuần, tối đa 12 giờ/phiên, một phiên GPU tương tác; thực tế đã có phiên chết khi upload file lớn — dùng Hugging Face Hub để chuyển file).
- Ngưỡng báo lại ở 4.3: 1,5 × ước lượng ≈ 21 – 33 giờ (không 8×/16×).

## Điểm cần bạn quyết trước G1

1. Ô Long 4× trên 1080 Ti: chờ rảnh rồi chạy lại, hay chấp nhận kết quả T4?
2. Quy tắc loại 6 đoạn XQuAD-vi trùng corpus (độ nhạy, không phải loại chính)?
3. Người chấm phụ chạy trên toàn bộ dự đoán cũ (+~99 000 lời gọi) hay chỉ trên mẫu hiệu chỉnh và dự đoán xác nhận?
4. Có chạy 8×/16× của XQuAD-vi (tốn ~8–12 giờ, chỉ mô tả) không?
5. Độ dài tóm tắt Sum: Long 4× cần ~2,4k token đầu ra mỗi bài. Có thể mô hình viết ngắn hơn; đề xuất đặt mục tiêu độ dài theo r=4× rồi cắt cho 8×, 16×.
