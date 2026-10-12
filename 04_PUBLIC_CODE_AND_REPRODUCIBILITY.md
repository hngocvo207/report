# Mã nguồn công khai và khả năng tái lập

Mã bằng chứng tra trong file 06. License, ngày push gần nhất và số issue mở được tra qua GitHub API trong lần audit này và lưu lại trong log [Đã xác minh, E31]. "Không có license" nghĩa là repo không có file license nào ở thư mục gốc.

## 1. Kết luận

Ba thư viện nền (PyG, scikit-learn, LightGBM) có license MIT hoặc BSD và đang được bảo trì, nên dùng nguyên được [Đã xác minh, E31]. Các repo gốc của bài báo về phát hiện lừa đảo trên Ethereum (Dynamic_Feature, LMAE4Eth, FraudGT, BERT4ETH) không có file license. Repo hiện tại chứa một bản sao mã FraudGT, nên không được công bố lại phần này khi chưa có sự đồng ý của tác giả [Đã xác minh, E31].

Code được công khai không có nghĩa là dữ liệu được phép công khai. Điều khoản sử dụng bộ dữ liệu MulDiGraph của XBlock chưa được xác minh [Chưa xác định: trang XBlock không hiển thị điều khoản khi truy cập tự động]. Cần đọc trực tiếp hoặc hỏi nhóm XBlock trước khi phân phối lại dữ liệu hay đặc trưng dẫn xuất.

## 2. Bốn mức sử dụng

| Mức | Nghĩa | Điều kiện |
|---|---|---|
| Dùng nguyên | Cài như thư viện, không sửa mã | License cho phép sử dụng |
| Fork | Sao chép repo để sửa riêng | License cho phép sửa đổi |
| Chỉnh sửa | Sửa mã và giữ trong repo của dự án | License cho phép sửa đổi và yêu cầu giữ thông báo bản quyền |
| Công bố lại | Đưa mã đã sửa lên kho công khai | License cho phép phân phối lại |

Repo không có license thì mặc định chỉ được đọc và chạy nội bộ. Fork công khai, chỉnh sửa rồi công bố lại đều cần sự cho phép của tác giả.

## 3. Ứng viên

Bảng 1 liệt kê các ứng viên theo vai trò trong nghiên cứu.

Bảng 1. Mã nguồn công khai liên quan

| Tên | URL | Vai trò | License | Push gần nhất | Mức sử dụng tối đa |
|---|---|---|---|---|---|
| PyTorch Geometric | https://github.com/pyg-team/pytorch_geometric | Thư viện GNN, đang dùng | MIT | 2026-10-06 | Công bố lại |
| scikit-learn | https://github.com/scikit-learn/scikit-learn | Baseline gradient boosting (GBM), metric | BSD-3-Clause | 2026-10-10 | Công bố lại |
| LightGBM | https://github.com/lightgbm-org/LightGBM | GBM thay thế để tinh chỉnh công bằng | MIT | 2026-10-11 | Công bố lại |
| XGBoost | https://github.com/dmlc/xgboost | GBM thay thế | Apache-2.0 | 2026-10-11 | Công bố lại kèm thông báo |
| Temporal Graph Networks (TGN) | https://github.com/twitter-research/tgn | Baseline đồ thị động (phương án D) | Apache-2.0 | 2024-05-28 | Fork, chỉnh sửa, công bố lại kèm thông báo |
| DyGLib | https://github.com/yule-BUAA/DyGLib | Bộ mô hình đồ thị động có phân loại nút | MIT | 2023-09-28 | Công bố lại |
| Temporal Graph Benchmark | https://github.com/shenyangHuang/TGB | Khung đánh giá đồ thị theo thời gian, tham khảo giao thức | MIT | 2026-07-27 | Công bố lại |
| GraphMAE | https://github.com/THUDM/GraphMAE | Tiền huấn luyện đồ thị, đã dùng ở pipeline cũ | MIT (file license, API không nhận dạng) | 2023-04-12 | Công bố lại |
| TLmGNN | https://github.com/lincozz/TLmGNN | Baseline bài báo, chưa chạy | Apache-2.0 | 2025-05-02 | Fork, chỉnh sửa, công bố lại kèm thông báo |
| FraudGT | https://github.com/junhongmit/FraudGT | Baseline graph transformer, đã chạy | Không có | 2025-06-05 | Chỉ chạy nội bộ |
| LMAE4Eth | https://github.com/lmae4eth/LMAE4Eth | Baseline bài báo, đã tái hiện | Không có | 2025-12-12 | Chỉ chạy nội bộ |
| Dynamic_Feature | https://github.com/dcszhang/Dynamic_Feature | Mã của bài báo Dynamic Feature Fusion | Không có | 2025-01-19 | Chỉ chạy nội bộ |
| BERT4ETH | https://github.com/git-disl/BERT4ETH | Baseline transformer trên chuỗi giao dịch | Không có | 2024-06-21 | Chỉ chạy nội bộ |
| PC-GNN | https://github.com/PonderLY/PC-GNN | Nguồn ý tưởng của sampler dùng nhãn cũ | Không có | 2021-12-26 | Chỉ đọc tham khảo |

Repo Dynamic_Feature có mô tả trùng với README của dự án, nên nhiều khả năng là mã chính thức của bài báo [Suy luận, E31]. README của dự án ghi license MIT, nhưng cả repo này lẫn repo gốc đều không có file license [Đã xác minh, E31].

PhishEye là một hệ thống phát hiện lừa đảo trên Ethereum bằng học tương phản (contrastive learning) trên đồ thị theo thời gian, có đánh giá chia theo thời gian. Mã nằm trên một kho ẩn danh [Chưa xác định: chưa xác minh online nội dung và license của kho mã PhishEye].

## 4. Đánh giá từng ứng viên chính

### 4.1. TGN và DyGLib

- Phần tái sử dụng: bộ lấy mẫu láng giềng theo thời gian, các mô hình TGN, GraphMixer, DyGFormer.
- Yêu cầu dữ liệu: danh sách cạnh có thời điểm, nhãn nút theo thời điểm.
- Thay đổi để tích hợp: chuyển mảng cạnh sang định dạng của thư viện, gán nhãn tại T_v cho từng tài khoản đích, dùng lại cách chia V3.
- Rủi ro giao thức: hai thư viện mặc định đánh giá theo dòng sự kiện. Thư viện dự đoán tại mỗi giao dịch, không dự đoán tại T_v. Cần sửa vòng đánh giá để chỉ chấm mỗi tài khoản một lần tại T_v, nếu không sẽ không so sánh được với V3-sạch.
- Bảo trì: DyGLib không có push từ 2023-09-28, TGN từ 2024-05-28. Có thể gặp xung đột phiên bản thư viện.

### 4.2. FraudGT

- Phần tái sử dụng: SparseNodeGT, cấu hình cho bộ dữ liệu ETH.
- Đã chạy trong dự án trên hai giao thức. Trên V3, diện tích dưới đường Precision-Recall đạt 0.332 với 1 seed. Đồ thị kiểm tra là đồ thị đầy đủ, nên FraudGT được lợi từ giao dịch sau T_v [Đã xác minh, E27].
- Thay đổi để tích hợp: thay bộ lấy mẫu bằng bộ lấy mẫu V3-sạch, chạy 5 seed.
- License: không có. Không đưa bản sao FraudGT lên kho công khai.

### 4.3. LMAE4Eth và TLmGNN

- LMAE4Eth được tái hiện trên chia ngẫu nhiên và đạt F1-score 0.2799, so với 0.8960 bài báo công bố [Đã xác minh, E28]. Bản tái hiện dùng mô hình ngôn ngữ nhỏ hơn bài báo và tự dựng bước chia tập vì repo gốc không có.
- TLmGNN chưa chạy trong dự án [Đã xác minh, E28]. Thiết kế dùng đồ thị vocab theo tài khoản nên có cùng rủi ro transductive như tri_model [Suy luận, E20].
- Rủi ro giao thức chung: cả hai bài báo dùng chia ngẫu nhiên. Cả hai không công bố cách chia đủ chi tiết để tái lập.

## 5. Kế hoạch tái lập kết quả của dự án

Kết quả V3-sạch tái lập được từ dữ liệu gốc, nhưng hiện chưa an toàn về mặt lưu trữ. Toàn bộ thư mục chứa pipeline sạch và kết quả chưa được git theo dõi [Đã xác minh, E30]. Thư viện PyG không có trong danh sách phụ thuộc [Đã xác minh, E30].

Thứ tự tái lập gồm sáu bước. File 06, mục 5 ghi lệnh cụ thể.

1. Chuyển đồ thị gốc thành mảng cạnh và tạo nhãn.
2. Tạo cách chia V3 theo t_first.
3. Tính bộ mới 18 cột và bộ mới 23 cột tại T_v. Bước nhóm 3 tốn thời gian nhất và chạy song song nhiều tiến trình.
4. Chạy GBM với 5 seed.
5. Dựng mảng tiền tố cho đồ thị theo thời gian, rồi chạy bốn biến thể GNN với 5 seed.
6. Tổng hợp kết quả và chạy các script audit của báo cáo này.

Bốn việc cần làm trước khi gửi kết quả ra ngoài [Đề xuất]:

- Đưa toàn bộ code của pipeline sạch và các file kết quả JSON vào git.
- Bổ sung PyG vào danh sách phụ thuộc, ghi phiên bản đã dùng.
- Lưu mã băm của dữ liệu gốc và của các file đặc trưng để kiểm tra đầu vào khi chạy lại.
- Lưu xác suất kiểm tra của mọi mô hình để chấm lại trên tập con và chạy bootstrap ghép cặp.
