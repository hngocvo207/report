# Tổng quan nghiên cứu phát hiện tài khoản lừa đảo trên Ethereum

Số liệu theo định dạng quốc tế. Mã bằng chứng dạng E1 tra trong file 06.

> Ba con số chính đo trên cùng một tập kiểm tra. Tập này gồm 487,855 tài khoản, trong đó có 233 tài khoản lừa đảo. Metric chính là diện tích dưới đường Precision-Recall (area under the precision-recall curve, AUPRC).
>
> - 0.531 ± 0.036: AUPRC của mô hình tốt nhất khi đã bỏ rò rỉ dữ liệu, so với 0.360 ± 0.004 của baseline dạng bảng.
> - 0.417 xuống 0.360: cùng baseline đó, AUPRC giảm khoảng 14% khi bỏ các đặc trưng nhìn thấy tương lai. Các con số cũ của dự án vì vậy không dùng làm kết quả.
> - 0.9372: ROC-AUC (diện tích dưới đường ROC, đo khả năng xếp tài khoản lừa đảo lên trên tài khoản thường) của một baseline chỉ đếm số giao dịch. ROC-AUC vì vậy không phân biệt được các mô hình trên bộ dữ liệu này.

## 1. Bài toán

Nghiên cứu này xếp hạng các tài khoản Ethereum mới theo nguy cơ lừa đảo trực tuyến (phishing), chỉ dùng giao dịch trong 30 ngày đầu của tài khoản. Nhãn 1 là tài khoản lừa đảo đã xác nhận, nhãn 0 là mọi tài khoản còn lại [Đã xác minh, E2]. Bộ dữ liệu MulDiGraph có 2,973,489 tài khoản, 13,551,303 giao dịch và 1165 tài khoản lừa đảo, tức 0.039% [Đã xác minh, E1].

## 2. Lý do cần giải quyết

Dự án bắt đầu bằng việc tái hiện bài báo Dynamic Feature Fusion, vốn công bố F1-score 94.71% mà không nêu đủ cách chia tập. F1-score lấy trung bình theo số mẫu của hai lớp, nên gần như chỉ phản ánh lớp tài khoản thường. Bản tái hiện học một biểu diễn riêng cho từng tài khoản đã biết. Trên tập kiểm tra cũ, 98.8% tài khoản nằm ngoài tập đã học. AUPRC khi đó chỉ đạt 0.124 [Suy luận, E20, E21]. Bài toán thực tế là cảnh báo tài khoản mới sau 30 ngày hoạt động, nên cách đánh giá phải chặn mọi thông tin chưa có tại lúc dự đoán.

## 3. Đầu vào và đầu ra

Đầu vào của mô hình tốt nhất cắt tại thời điểm dự đoán T_v, bằng thời điểm giao dịch đầu tiên cộng 30 ngày [Đã xác minh, E5, E9]. Đầu vào gồm 18 đặc trưng hành vi của tài khoản và của láng giềng, cộng cấu trúc giao dịch 2 bước quanh tài khoản. Đầu ra là xác suất lừa đảo. Ngưỡng cảnh báo được chọn trên tập kiểm định [Đã xác minh, E12]. File 01 có sơ đồ luồng dữ liệu và bảng input/output.

## 4. Phương pháp hiện tại

Tài khoản được chia theo thời điểm giao dịch đầu tiên thành ba tập không trùng nhau, với hai mốc 2018-05-18 và 2018-06-18 [Đã xác minh, E3, E4]. Báo cáo gọi cách chia này cộng ràng buộc T_v là V3-clean.

Mô hình tốt nhất là mạng nơ-ron đồ thị (graph neural network, GNN) hai lớp, tổng hợp thông tin từ cả phía gửi lẫn phía nhận. Mỗi tài khoản được chấm trên đồ thị riêng tại T_v của nó. Bộ lấy mẫu láng giềng không dùng nhãn [Đã xác minh, E9, E10]. Kết quả là trung bình 5 seed (giá trị khởi tạo ngẫu nhiên). Baseline so sánh là gradient boosting (GBM) chỉ dùng đặc trưng của chính tài khoản [Đã xác minh, E14, E15].

## 5. Vấn đề lớn nhất

Các con số cũ của dự án đều chứa rò rỉ dữ liệu (data leakage), tức mô hình thấy thông tin chưa có tại lúc dự đoán. Ba nguồn đã được đo [Đã xác minh, E14, E17, E18].

- Đặc trưng tính trên toàn bộ lịch sử tài khoản.
- Tập kiểm định được chấm trên đồ thị có giao dịch của giai đoạn kiểm tra.
- Kết quả 0.538 dùng nhãn tập kiểm định khi chọn đặc trưng, chạy lại 5 seed chỉ còn 0.422 ± 0.046.

V3-sạch đã bỏ ba nguồn này. Kiểm toán phát hiện thêm một rủi ro mới do cách thu thập dữ liệu đi 2 bước từ tài khoản lừa đảo. Tại T_v, 68.06% tài khoản thường chỉ có một giao dịch, so với 3.95% tài khoản lừa đảo [Đã xác minh, E23]. Riêng số giao dịch cho ROC-AUC 0.9372 nhưng AUPRC chỉ 0.0123. Khi bỏ các tài khoản có một giao dịch, GBM vẫn đạt AUPRC 0.3845. AUPRC vì vậy vẫn dùng được, còn ROC-AUC thì không.

Các giới hạn còn mở gồm thiếu thời điểm gán nhãn và tập kiểm tra ít tài khoản lừa đảo [Đã xác minh, E32]. Mã nguồn của quy trình V3-sạch cũng chưa được đưa vào git [Đã xác minh, E30].

## 6. Quyết định cần mentor phê duyệt

1. Chọn V3-sạch làm giao thức chính và ngừng báo cáo các con số cũ như kết quả. File 02 có thêm hai phương án thay thế.
2. Đặc trưng của 93.62% tài khoản tập kiểm định kéo dài sang giai đoạn kiểm tra [Đã xác minh, E25]. Mentor chọn cắt tại ranh giới hay giữ nguyên và ghi là giới hạn.
3. Dùng AUPRC làm metric chính, thêm AUPRC trên tập con bỏ tài khoản có một giao dịch. ROC-AUC chỉ là metric phụ.
4. Ưu tiên GNN có thêm thời gian và số tiền trên từng cạnh, chạy cùng bản kết hợp với GBM. Ngừng nhánh mô hình ngôn ngữ vì nhánh này chưa lần nào vượt GNN đơn lẻ [Đề xuất, E19, E21].
5. Repo chứa bản sao mã FraudGT, một mô hình phát hiện gian lận công khai, trong khi repo gốc không có license. Phần này không được công bố khi chưa có phép của tác giả [Đã xác minh, E31].

File 02 đến 06 lần lượt trình bày chia tập và rò rỉ, mô hình, mã nguồn công khai, kế hoạch thí nghiệm và bằng chứng.
