# KET_QUA_JUDGE — chấm lại dự đoán đã có bằng LLM (Giai đoạn 1)

Phạm vi thực hiện: **chỉ 4×** (cả tập test ViQuAD đoạn đơn và Long, cùng `full`/`none`). Theo lựa chọn (b) của người dùng
(2026-11-07), 8×, 16× và MLQA **chưa chấm** (đã chấm ~52 000/98 621 bộ ba trong cache nhưng chưa thu kết quả; xem §6).
Ràng buộc: `PREREG_JUDGE.md` (SHA-256 `085d0279cbfff847c7aba76b7810103f87dde24270d25ca4402cd63f581effe9`), người chấm chính
DeepSeek-V4.1-Flash, nhiệt độ 0, tắt thinking. Số liệu thô: `results/icisn/judge/tables_r4.json`.
Bootstrap theo bài (19 bài), 10 000 lần, seed 0. Mọi số là điểm phần trăm; `[a, b]` là CI 95%.

## 1. Hiệu chỉnh người chấm (60 câu, đoạn đơn + Long, 4×)

Nhãn tham chiếu: agent gán mù, **người dùng soát ngày 2026-11-08 và sửa 1 nhãn** (item 27, 1→0); theo PREREG, κ tính trên
nhãn đã sửa là chính. Bản gốc của agent: `human_audit_60.agent_original.csv`; kết quả theo nhãn gốc: `calibration_agent_labels.json`.

| Cặp | Cohen κ (nhãn người dùng đã soát) | Đồng ý | κ theo nhãn gốc của agent |
|---|---|---|---|
| DeepSeek (chính) và nhãn tham chiếu | **0,899** | 95,0% | 0,866 |
| Qwen3.8-27B (phụ) và nhãn tham chiếu | 0,900 | 95,0% | 0,867 |
| DeepSeek và Qwen3.8-27B | 0,799 | 90,0% | (không đổi) |

- Ngưỡng định trước κ ≥ 0,60: **đạt**, ACC-LLM là độ đo chính thức.
- Không có câu trả lời của người chấm bị coi là không hợp lệ (0/60 mỗi người; 0 trong cả 33 733 bộ ba đã thu).
- Người dùng đã soát cả 60 nhãn và chỉ sửa 1 (SHA-256 file đã sửa: `18ab24d8…02e5`, trong `human_audit_60.sha256`); 11 ca ranh giới
  còn lại giữ nguyên nhãn. Nhãn được soát bởi một người, không có người gán độc lập thứ hai.
- Người chấm chính (DeepSeek) khác họ với reader (Qwen3.5-2B); người chấm phụ cùng họ Qwen. κ giữa hai người chấm 0,80.

## 2. Bảng test 4× (F1 / EM / ACC-LLM, trung bình [CI 95%])

| Hệ | Đoạn đơn F1 | EM | ACC-LLM | Long F1 | EM | ACC-LLM |
|---|---|---|---|---|---|---|
| Toàn văn | 73,5 | 45,9 | 84,1 | 61,7 | 34,3 | 70,7 |
| Không ngữ cảnh | 11,4 | 1,8 | 6,4 | 11,4 | 1,8 | 6,4 |
| Cắt đầu (truncation) | 30,0 | 15,6 | 31,2 | 22,6 | 11,5 | 23,1 |
| LLMLingua-2 | 26,7 | 9,8 | 31,3 | 20,2 | 7,8 | 22,2 |
| BM25 | 51,7 | 31,1 | 56,8 | 62,8 | 35,4 | 70,7 |
| BM25 2k | 66,0 | 40,4 | 74,9 | 61,8 | 34,5 | 70,2 |
| PhoBERT | 55,4 | 33,3 | 61,4 | 63,1 | 36,3 | 71,2 |
| M (memory thuần) | 65,4 | 30,1 | 69,7 | 51,9 | 21,4 | 53,2 |
| ME (f = 2) | 63,3 | 29,6 | 64,6 | 68,9 | 45,2 | 74,4 |
| Prompt + BM25 (f = 2) | 40,1 | 20,9 | 36,1 | 68,5 | 45,6 | 74,8 |

(CI đầy đủ của từng ô trong `tables_r4.json`, trường `systems`.) ACC-LLM cao hơn F1 ở hầu hết hệ vì chấp nhận diễn đạt khác và
đáp án dài/ngắn hơn; thứ hạng giữa các hệ ít thay đổi (xem §3 cho các ngoại lệ).

## 3. Hiệu số ghép cặp (a − b), F1 và ACC-LLM cạnh nhau

| Cặp | Đoạn đơn F1 | Đoạn đơn ACC | Long F1 | Long ACC |
|---|---|---|---|---|
| ME − prompt | +23,2 [21,7; 24,6] | +28,6 [26,5; 30,5] | **+0,43 [−1,43; +2,18]** | **−0,41 [−2,34; +1,48]** |
| ME − M | −2,1 [−3,4; −0,8] | −5,1 [−7,6; −2,4] | +17,0 [15,0; 18,8] | +21,2 [18,8; 23,1] |
| ME − BM25 (cùng k) | +11,6 [10,2; 12,9] | +7,8 [5,7; 9,8] | +6,1 [3,6; 8,3] | +3,7 [1,3; 6,1] |
| ME − BM25 2k | −2,8 [−4,6; −1,2] | −10,2 [−12,7; −8,1] | +7,1 [4,2; 9,5] | +4,2 [1,2; 6,8] |
| ME − PhoBERT | +7,8 [5,8; 9,8] | +3,3 [0,4; 5,9] | +5,7 [2,3; 8,3] | +3,2 [−0,5; 6,0] |
| M − BM25 (cùng k) | +13,7 [11,6; 15,7] | +12,9 [9,6; 15,9] | −10,9 [−12,6; −9,0] | −17,5 [−19,3; −14,7] |
| M − PhoBERT | +10,0 [7,6; 12,4] | +8,4 [5,1; 11,5] | −11,3 [−13,7; −9,0] | −18,0 [−20,5; −15,5] |
| M − BM25 2k | −0,6 [−3,1; +1,5] | **−5,1 [−8,7; −2,1]** | −9,9 [−12,1; −7,7] | −17,0 [−19,4; −14,3] |
| ME − toàn văn | −10,2 [−11,6; −8,9] | −19,5 [−21,3; −17,4] | +7,2 [3,7; 9,6] | +3,7 [0,2; 6,3] |
| M − toàn văn | −8,1 [−9,9; −6,6] | −14,4 [−16,7; −12,3] | −9,9 [−12,3; −7,5] | −17,5 [−20,2; −14,8] |

## 4. Chỗ F1 và ACC-LLM cho kết luận khác chiều (G1.4)

Khác chiều = dấu ý nghĩa thống kê (CI loại 0 và dấu) khác nhau giữa hai độ đo. Có **hai** ô như vậy ở 4× trong các cặp trên:

1. **Đoạn đơn, M − BM25 2k:** F1 cho "hòa" (−0,6 [−3,1; +1,5]) nhưng ACC-LLM cho BM25 2k **hơn** M 5,1 điểm [−8,7; −2,1].
   Nghĩa là: kết luận "memory thuần ngang văn bản gấp đôi ngân sách" theo F1 không bền; theo ACC-LLM, văn bản 2k hơn.
   (Đây là so sánh với văn bản có ngân sách gấp đôi, không phải cùng ngân sách.)
2. **Long, ME − PhoBERT:** F1 cho ME hơn (+5,7 [2,3; 8,3]) nhưng ACC-LLM thì không loại được 0 (+3,2 [−0,5; +6,0]).
   Khẳng định "ME hơn PhoBERT ở Long" chỉ giữ được theo F1.

**Đoạn đơn 4×, F1 và EM ngược nhau (câu hỏi của người dùng):** M có F1 cao hơn BM25 cùng ngân sách (65,4 so với 51,7) nhưng
EM thấp hơn một chút (30,1 so với 31,1 — hai CI chồng nhau nhiều). ACC-LLM đứng về phía F1: M − BM25 = +12,9 [9,6; 15,9].
Vậy ưu thế của memory thuần so với văn bản cùng ngân sách ở đoạn đơn **không phải là nhiễu của F1**; EM không phản ánh được
điều đó vì memory thuần trả lời đúng ý nhưng ít khi trùng khít từ-ngữ. Lưu ý ACC-LLM của M còn thấp hơn BM25 2k (§4.1).

**Kết luận không đổi ở cả hai độ đo:** RQ1 vẫn FAIL — ME ngang prompt ở Long (ΔF1 +0,43; ΔACC −0,41; cả hai CI chứa 0).
ME hơn prompt rất nhiều ở đoạn đơn, ME kém M ở đoạn đơn và vượt xa M ở Long (cùng chiều ở cả hai độ đo).

## 5. Phân tích In/Out và router (HẬU NGHIỆM — đã làm sau khi biết gate FAIL, không phải xác nhận)

In = đáp án vàng nằm trong các câu BM25 của ME (`gold_flags_r4.json`). Đoạn đơn: 789/2653 In (29,7%); Long: 2411/2653 In (90,9%).
Tương tác = (hiệu ở Out) − (hiệu ở In).

| Cặp | Thiết lập | Tương tác F1 [CI] | Tương tác ACC [CI] |
|---|---|---|---|
| ME − prompt | đoạn đơn | +40,9 [38,1; 43,2] | +50,1 [46,2; 53,3] |
| ME − prompt | Long | +8,3 [3,6; 14,0] | +12,3 [8,0; 17,9] |
| ME − M | đoạn đơn | −15,6 [−18,6; −12,7] | −20,6 [−24,3; −16,6] |
| ME − M | Long | −26,9 [−32,2; −21,1] | −34,2 [−41,1; −28,8] |
| ME − PhoBERT | đoạn đơn | +2,4 [−0,8; +5,9] | −3,5 [−7,2; +0,4] |
| ME − PhoBERT | Long | −33,1 [−41,0; −24,9] | −40,4 [−49,6; −31,7] |
| ME − BM25 2k | đoạn đơn | −7,1 [−11,6; −2,6] | −14,0 [−19,0; −9,1] |
| ME − BM25 2k | Long | −22,2 [−25,5; −18,5] | −27,8 [−34,5; −21,7] |

- ME − prompt: tương tác dương, CI loại 0 ở cả hai độ đo và cả hai thiết lập. Cùng chiều với giả thuyết "memory bù đúng chỗ bộ
  chọn câu bỏ sót" nhưng đây là **thăm dò hậu nghiệm**; H-R1 phải kiểm trên dữ liệu mới.
- ME − PhoBERT đoạn đơn: F1 (+2,4, CI chứa 0) và ACC (−3,5, CI chứa 0) khác dấu nhưng đều không có ý nghĩa.

Router "ME nếu câu trả lời của ME nằm trong bằng chứng (`aie`), ngược lại M" (không tham số; như `paper_numbers.py:221`):

| | Chuyển sang M | Router F1 | Router ACC | Router − M (F1 / ACC) | Router − BM25 2k (F1 / ACC) | Router − prompt (F1 / ACC) |
|---|---|---|---|---|---|---|
| Đoạn đơn | 71,3% | 67,7 | 72,3 | +2,3 [1,4; 3,1] / +2,6 [1,5; 3,7] | +1,6 [−0,7; 3,5] / **−2,5 [−5,9; +0,2]** | +27,6 / +36,3 |
| Long | 14,6% | 68,2 | 72,7 | +16,4 / +19,5 | +6,5 [3,5; 9,0] / +2,5 [−0,4; 5,4] | −0,2 [−2,1; 1,6] / **−2,1 [−3,6; −0,4]** |

- Router − M (đoạn đơn): dương và có ý nghĩa ở cả hai độ đo (H-R2a ứng viên).
- Router so với BM25 2k (đoạn đơn): F1 +1,6 (n.s.) nhưng ACC −2,5 (n.s.): **dấu đảo chiều giữa hai độ đo**; dưới δ = 2,0 F1 /
  0,02 ACC đã định hướng cho H-R2b thì khoảng tin cậy ACC [−5,9; +0,2] chưa loại được việc router kém BM25 2k quá δ.
- Router so với prompt (Long): F1 hòa nhưng ACC −2,1 [−3,6; −0,4] — theo ACC, router **kém** prompt một chút.

## 6. Giới hạn và việc chưa làm

- Chưa chấm 8×, 16× và MLQA (quyết định tiết kiệm API/thời gian). Cache còn ~52 000 bộ ba; muốn thu thêm thì chạy
  `python scripts/icisn/judge_all.py 16` (~6 giờ cho phần còn lại ở 150 lời gọi/phút) rồi `judge_collect.py`.
- Chưa phân tích G1.3 cho mẫu MLQA và chưa có bảng 8×/16×; `analyze_judge.py --ratios 8 16` sẵn sàng sau khi thu nhãn.
- Nhãn tham chiếu do agent gán rồi người dùng soát (một người soát). Mẫu hiệu chỉnh chỉ 60 câu → κ có CI rộng (chưa tính).
- Người chấm chính cũng có thể thiên vị về độ dài/diễn đạt; ACC-LLM của M cao hơn F1 của nó ở đoạn đơn (69,7 so với 65,4) gợi ý
  người chấm nới tay với câu trả lời thiếu từ nối. Chưa có kiểm tra con người ngoài 60 câu.
- Quyết định kỹ thuật không lệch đăng ký: 5 bộ ba lỗi 429 lúc chấm lần đầu được chấm lại bằng cùng prompt (`--fill`);
  giới hạn tần suất 140 lời gọi/phút thêm vào `llm.py` (không ảnh hưởng nội dung lời gọi).
- Mọi so sánh ở §3–§5 là cho 4× một seed, fp16 không liên quan (dự đoán lấy từ H100 bf16).
