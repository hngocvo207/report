# Kế hoạch thực nghiệm

Mã bằng chứng tra trong file 06. Mọi ô kết quả của thí nghiệm mới ghi "chưa chạy". Giao thức, mô hình và ablation được định nghĩa ở file 02, mục 6 và file 03.

## 1. Câu hỏi nghiên cứu

Năm câu hỏi dùng hai viết tắt. Mạng nơ-ron đồ thị (graph neural network, GNN) là mô hình học trên đồ thị giao dịch. Gradient boosting (GBM) là mô hình cây dùng đặc trưng dạng bảng.

| Mã | Câu hỏi | Giả thuyết |
|---|---|---|
| Câu 1 | Mỗi nguồn rò rỉ dữ liệu (data leakage) làm số liệu cao lên bao nhiêu trên MulDiGraph? | Rò rỉ đặc trưng đã đo được. Rò rỉ qua đồ thị kiểm tra đầy đủ chưa được đo riêng |
| Câu 2 | Thuộc tính cạnh theo thời gian có thêm tín hiệu cho GNN time-aware không? | H1 ở file 03 |
| Câu 3 | GBM và GNN có bổ sung cho nhau trên giao thức V3-sạch không? | H3 ở file 03 |
| Câu 4 | Kết quả có vững khi đổi cửa sổ quan sát, đổi giai đoạn kiểm tra và bỏ tài khoản bậc 1 không? | Thứ hạng giữa các mô hình giữ nguyên |
| Câu 5 | Chênh lệch với số công bố của các bài báo đến từ giao thức hay kiến trúc? | Phần lớn đến từ giao thức [Suy luận, E28, E29] |

## 2. Thiết lập chung

- Bộ dữ liệu: MulDiGraph, 2,973,489 tài khoản, 1165 tài khoản lừa đảo (file 01).
- Cách chia: V3-sạch cho Câu 1 đến Câu 4. Đánh giá cuốn chiếu cho Câu 4. Chia ngẫu nhiên có ràng buộc T_v cho Câu 5.
- Seed (giá trị khởi tạo ngẫu nhiên): 5 seed cho mọi mô hình huấn luyện.
- Metric chính, định nghĩa theo code đánh giá hiện có (E37): diện tích dưới đường Precision-Recall (area under the precision-recall curve, AUPRC). Metric phụ: Precision@100, Recall@1000, F1-score tại ngưỡng chọn trên tập kiểm định, AUPRC trên tập con bậc ít nhất 2.
- Kiểm định: bootstrap ghép cặp 1000 lần trên cùng tập kiểm tra cho mọi so sánh hai mô hình.
- Chọn siêu tham số: chỉ trên tập kiểm định. Tập kiểm tra chấm đúng một lần cho mỗi seed.

## 3. Tiêu chí kết luận

Một mô hình được coi là tốt hơn mô hình khác khi thỏa cả hai điều kiện [Đề xuất]:

1. Khoảng tin cậy 95% của chênh lệch AUPRC trong bootstrap ghép cặp không chứa 0.
2. Thứ hạng giữ nguyên trên tập con bậc ít nhất 2.

Chênh lệch trung bình nhỏ hơn độ lệch chuẩn qua seed được báo cáo là "không phân biệt được". Ví dụ, GNN hai chiều có và không có nhóm 3 chênh 0.022, nhỏ hơn độ lệch chuẩn 0.049 [Đã xác minh, E15].

## 4. Danh sách thí nghiệm

Bảng 1 liệt kê thí nghiệm theo thứ tự ưu tiên. Cột "Kết quả hiện có" chỉ ghi số đã chạy, ô chưa chạy ghi "chưa chạy".

Bảng 1. Thí nghiệm, baseline và kết quả hiện có

| Mã | Thí nghiệm | Câu hỏi | Baseline so sánh | Kết quả hiện có |
|---|---|---|---|---|
| X0 | Lưu xác suất kiểm tra của bốn biến thể GNN đã có, chấm lại trên tập con bậc ít nhất 2 | Câu 4 | GBM trên tập con: 0.3845 (seed 0) | chưa chạy |
| X1 | Bootstrap ghép cặp giữa GNN hai chiều có nhóm 3 và GBM bộ mới 23 cột | Câu 3 | Hai mô hình đã có: 0.531 ± 0.036 và 0.360 ± 0.004 | chưa chạy |
| X2 | Kết hợp muộn GNN và GBM, trọng số chọn trên tập kiểm định (phương án A) | Câu 3 | Từng mô hình riêng | chưa chạy |
| X3 | GNN time-aware có thuộc tính cạnh (phương án B) | Câu 2 | GNN hai chiều có nhóm 3: 0.531 ± 0.036 | chưa chạy |
| X4 | Ablation A1 đến A5 của phương án B (file 03, mục 6) | Câu 2, Câu 3 | X3 | chưa chạy |
| X5 | Cửa sổ 7 ngày thay cho 30 ngày, chỉ bộ mới 18 cột và GNN | Câu 4 | Cửa sổ 30 ngày | chưa chạy |
| X6 | Đánh giá cuốn chiếu với 3 cặp mốc | Câu 4 | V3-sạch một mốc | chưa chạy |
| X7 | Huấn luyện lại trên tập huấn luyện gộp tập kiểm định, giữ siêu tham số | Câu 4 | Huấn luyện trên tập huấn luyện | chưa chạy |
| X8 | GNN chấm trên đồ thị đầy đủ so với snapshot tại T_v, cùng một checkpoint | Câu 1 | GNN hai chiều có nhóm 3 chấm tại T_v | chưa chạy |
| X9 | FraudGT với bộ lấy mẫu V3-sạch, 5 seed | Câu 1, Câu 5 | FraudGT trên V3: 0.332 (1 seed) | chưa chạy |
| X10 | Temporal Graph Networks hoặc DyGFormer trên V3-sạch (phương án D) | Câu 5 | X3 | chưa chạy |
| X11 | Chia ngẫu nhiên có ràng buộc T_v cho GNN | Câu 5 | GBM chia ngẫu nhiên: 0.308 ± 0.011 | chưa chạy |

Thí nghiệm X8 đo riêng rò rỉ qua đồ thị cho Câu 1 [Đề xuất]. GBM không tham gia X8 vì GBM chỉ dùng đặc trưng của chính tài khoản.

## 5. Kết quả đã có làm mốc

Bảng 2 ghi lại các kết quả V3-sạch đã chạy, dùng làm mốc cho Bảng 1 [Đã xác minh, E14, E15, E22].

Bảng 2. Kết quả mốc trên V3-sạch, 5 seed

| Mô hình (nguồn E14, E15, E22) | AUPRC | Precision@100 | F1-score tại ngưỡng tập kiểm định |
|---|---:|---:|---:|
| Khoảng cách tới tài khoản lừa đảo của tập huấn luyện | 0.0010 | - | - |
| GBM, bộ mới 23 cột | 0.360 ± 0.004 | 0.68 | 0.416 |
| GNN hai chiều, thêm nhóm 3 | 0.531 ± 0.036 | 0.75 | 0.589 |

## 6. Tài nguyên

- Phần cứng: một GPU, không cần GPU cho GBM. Bước tính nhóm 3 tại T_v chạy trên CPU nhiều tiến trình và là bước tốn thời gian nhất của pipeline [Đã xác minh, E7].
- X0, X1, X2 dùng lại mô hình đã có, chỉ cần chạy lại với chế độ lưu xác suất.
- X3, X4 cần viết thêm phần tính thuộc tính cạnh từ mảng tiền tố đã có.
- X5 cần tính lại nhóm 1 và 2 với cửa sổ 7 ngày. Nhóm 3 có thể bỏ qua để giảm chi phí.
- X10 cần chuyển dữ liệu sang định dạng thư viện (file 04, mục 4.1).

## 7. Thứ tự đề xuất

Nhóm 1 gồm X0, X1, X2 và có chi phí thấp nhất. Nhóm 1 trả lời ngay Câu 3 và một phần Câu 4 [Đề xuất]. Nhóm 2 gồm X3, X4 và kiểm tra giả thuyết chính H1. Nhóm 3 gồm X5 đến X11 và kiểm tra độ vững cùng khả năng so sánh với bài báo. Mỗi nhóm chỉ bắt đầu khi nhóm trước đã có kết quả, để quyết định có tiếp tục nhánh mô hình hay không.
