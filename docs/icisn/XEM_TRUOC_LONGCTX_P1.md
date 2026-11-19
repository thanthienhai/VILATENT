# Xem trước P1 (ViQuAD-XL tổng hợp có điều khiển); chưa chạy mô hình đọc

- Mẫu: 605 câu hỏi (tối đa 32/bài đích); còn 533 sau khi loại 72 câu có đáp án trong bài nhiễu.
- Kho bài nhiễu: 67 bài, không dùng Wikipedia dài (đã nằm trong kho giai đoạn 1).
- Độ dài đo bằng token Qwen3.5-2B (khoảng 1,26 token/âm tiết trên 19 bài kiểm thử).
- Số câu hỏi mỗi ô (độ dài × vị trí × nhiễu): min 25, max 33, 18 ô.

| độ dài mục tiêu | số bài nhiễu (trung vị) | token thực (trung vị) |
|---|---|---|
| 16,000 | 4 | 17,219 |
| 32,000 | 9 | 35,249 |
| 64,000 | 15 | 67,453 |

## Ví dụ (một cho mỗi độ dài, nhiễu 'hard')

**Câu hỏi:** Việc cuộc hội đàm bí mật giữa Pháp và Mỹ đã dẫn đến những hệ quả gì?  
**Đáp án vàng:** dấy lên một làn sóng lớn của chủ nghĩa biệt lập chống lại Roosevelt  
**Ngữ cảnh:** 16,246 token, 1 bài; bài đích 'Franklin D. Roosevelt' ở vị trí 1/1 (start); nhiễu hard  
**Bài nhiễu gần nhất (đầu danh sách):** 

**Câu hỏi:** Sự bất cập trong việc truyền thông tin từ Washington đến các đảo Hawaii là gì?  
**Đáp án vàng:** thông điệp này không được đánh dấu "khẩn cấp" nào vì thế nó được gửi đi theo thứ tự nhận được như các thông điệp khác  
**Ngữ cảnh:** 39,400 token, 3 bài; bài đích 'Franklin D. Roosevelt' ở vị trí 3/3 (end); nhiễu hard  
**Bài nhiễu gần nhất (đầu danh sách):** Chiến tranh Vùng Vịnh; Canada

**Câu hỏi:** Liên đoàn Tự do Mỹ sau khi thành lập đã có những hành động gì nhắm vào tổng thống Roosevelt?  
**Đáp án vàng:** Họ tấn công Roosevelt một cách điên cuồng và so sánh ông với Marx và Lênin  
**Ngữ cảnh:** 65,683 token, 6 bài; bài đích 'Franklin D. Roosevelt' ở vị trí 3/6 (middle); nhiễu hard  
**Bài nhiễu gần nhất (đầu danh sách):** François Mitterrand; Chiến tranh Vùng Vịnh; Mahatma Gandhi; Mông Cổ; Canada
