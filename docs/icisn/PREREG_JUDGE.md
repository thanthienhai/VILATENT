# PREREG_JUDGE — đăng ký trước người chấm LLM (ACC-LLM)

Khóa ngày 2026-11-07, **trước** mọi lời gọi chấm trên dự đoán thật và trước khi gán nhãn tham chiếu.
SHA-256 của file này ghi trong `docs/icisn/PREREG_JUDGE.sha256` (tính trên đúng nội dung file này). Prompt nằm trong
`docs/icisn/judge_prompt.json`; SHA-256 của nó ghi ở mục 1. Mã chấm: `scripts/icisn/llm.py`, `scripts/icisn/judge.py`.

## 1. Prompt chấm (khóa)

Đầu vào chỉ gồm câu hỏi, các đáp án vàng và câu trả lời (không có đoạn văn, không có tên hệ, không có F1/EM).
Nội dung đầy đủ trong `docs/icisn/judge_prompt.json` (`version: judge_v1`), SHA-256 của file đó:

JUDGE_PROMPT_SHA256: ghi trong `docs/icisn/PREREG_JUDGE.sha256` (dòng thứ hai)

Tóm tắt: một thông điệp hệ thống ("chỉ trả lời một từ") và một thông điệp người dùng gồm câu hỏi, danh sách đáp án vàng
(mỗi dòng một đáp án khác nhau, thứ tự theo dữ liệu), câu trả lời, ba quy tắc chấm (ĐÚNG: cùng thông tin với ít nhất một
đáp án vàng, cho phép diễn đạt khác/dài/ngắn nếu không mâu thuẫn hay thêm thực thể khác; SAI: thiếu ý chính, thực thể/số
khác, mâu thuẫn, không trả lời; chỉ dựa vào câu hỏi và đáp án vàng) và yêu cầu đáp một từ: ĐÚNG hoặc SAI.
Câu trả lời dài hơn 1000 ký tự bị cắt ở 1000 ký tự trước khi chấm.

## 2. Người chấm và tham số

- Người chấm chính: `DeepSeek-V4.1-Flash`. Người chấm phụ: `Qwen3.8-27B`.
- Nhiệt độ 0, `max_tokens` 8, tắt thinking (DeepSeek: `chat_template_kwargs.thinking=false`; Qwen:
  `chat_template_kwargs.enable_thinking=false`). Đã kiểm trên câu đùa: cả hai trả "ĐÚNG", không có token suy luận.
- Một lời gọi cho mỗi bộ ba (câu hỏi, danh sách đáp án vàng, câu trả lời) khác nhau; kết quả dùng chung cho mọi dòng
  có cùng bộ ba (cache). Không gộp nhiều câu vào một lời gọi.
- Người chấm phụ **chỉ chạy trên mẫu hiệu chỉnh 60 câu** (quyết định của người dùng 2026-11-07) và trên dự đoán xác nhận
  ở Giai đoạn 3/4 (báo kèm). Không chạy trên toàn bộ dự đoán cũ.

## 3. Luật phân tích câu trả lời của người chấm

- Chuẩn hóa: NFC, bỏ khoảng trắng đầu/cuối, chữ hoa, bỏ ký tự không phải chữ cái. Bắt đầu bằng `ĐÚNG` hoặc `DUNG` → 1.
  Bắt đầu bằng `SAI` → 0. Mọi trường hợp khác là **không hợp lệ**: tính 0, đếm và báo tỉ lệ không hợp lệ cho từng người
  chấm. Không gọi lại để lấy kết quả khác.
- Lỗi mạng/máy chủ: thử lại tối đa 6 lần với chờ tăng dần. Hết lượt thì dừng và báo, không đoán nhãn.

## 4. Luật cho câu trả lời rỗng hoặc không đọc được (không qua người chấm)

- Câu trả lời rỗng, hoặc không chứa chữ cái/chữ số nào → ACC-LLM = 0, nhãn nguồn `rule_empty`.
- Dòng có cờ `unreadable = true` trong file dự đoán (định nghĩa của `vilatent/metrics.py:is_unreadable`) → ACC-LLM = 0,
  nhãn nguồn `rule_unreadable`.
- Các dòng này **không** được tính vào tỉ lệ đồng ý của người chấm và được đếm riêng trong báo cáo.

## 5. Hiệu chỉnh (60 câu)

- Mẫu phân tầng theo hệ × thiết lập: thiết lập ∈ {đoạn đơn, Long} trên tập test ViQuAD ở 4×; hệ ∈ {full, none, truncation,
  bm25, bm25_x2, phobert, llmlingua2, prompt_bm25_f2, vilatent_m, vilatent_me_f2} → 20 tầng × 3 câu, lấy ngẫu nhiên
  đơn giản trong tầng, seed 0, loại câu trả lời rỗng/không đọc được. MLQA không nằm trong mẫu hiệu chỉnh.
- Nhãn tham chiếu do agent gán **mù** (chưa xem đầu ra của bất kỳ người chấm LLM nào), vào `human_audit_60.csv`; người
  dùng soát lại. Nếu người dùng sửa nhãn, báo κ theo nhãn đã sửa là chính, nhãn của agent là thứ yếu.
- Báo: Cohen κ giữa từng người chấm và nhãn tham chiếu, κ giữa hai người chấm, tỉ lệ đồng ý, bảng nhầm lẫn.
- **Ngưỡng định trước:** κ(người chấm chính, tham chiếu) ≥ 0,60 thì ACC-LLM là độ đo chính thức ở Giai đoạn 5; thấp
  hơn thì ACC-LLM vẫn tính nhưng gắn nhãn thăm dò và bài không dựa vào nó để tuyên bố "đạt". Prompt **không** được sửa sau
  khi thấy kết quả hiệu chỉnh; nếu muốn dùng prompt khác phải tạo `judge_v2`, đăng ký lại và báo rõ.

## 6. Tính lại bảng với ACC-LLM (G1.3)

- Phạm vi: mọi `*.jsonl` dự đoán trong `results/paper/test` và `results/paper/mlqa` (kể cả các shard MLQA).
  Không ghi đè `results/paper/`; kết quả ghi vào `results/icisn/judge/`.
- ACC-LLM của một dòng ∈ {0,1}. Các bảng tính lại: bảng test (trung bình ACC-LLM theo hệ × tỉ lệ × thiết lập), hiệu số
  ghép cặp (ME−prompt, ME−M, M−văn bản cùng ngân sách…), và In/Out theo `scripts/gold_split.py`. Phần In/Out là hậu
  nghiệm và gắn nhãn như vậy.
- Bootstrap ghép cặp theo **bài** (khóa `title`, nếu rỗng thì `cluster`; hàm `vilatent.stats`), 10 000 lần, seed 0.
- G1.4: báo mọi ô mà F1 và ACC-LLM cho kết luận khác chiều (khác dấu hiệu số, hoặc một độ đo có CI loại 0 còn độ đo kia
  thì không), đặc biệt đoạn đơn 4× (F1 và EM đang ngược chiều).

## 7. Điều không thay đổi sau khi khóa

Prompt, người chấm, tham số, luật mục 3–4, thiết kế mẫu mục 5, ngưỡng κ và các luật mục 6. Mọi sai khác sẽ được ghi vào
báo cáo với nhãn "lệch khỏi đăng ký".
