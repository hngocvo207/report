## Thứ tự đọc

1. Đọc file 00 để nắm toàn bộ dự án và năm quyết định cần mentor phê duyệt.
2. Đọc file 02 và file 03 để đánh giá các quyết định về chia tập và mô hình.
3. Tra file 06 khi cần kiểm tra một nhận định cụ thể.

Các file 01, 04 và 05 là phần chi tiết, đọc khi cần.

## Danh mục file

| File | Nội dung |
|---|---|
| 00_OVERVIEW.md | Tổng quan: bài toán, đầu vào và đầu ra, phương pháp, vấn đề lớn nhất, quyết định cần phê duyệt |
| 01_PROBLEM_AND_DATA.md | Bài toán, nhãn, bộ dữ liệu MulDiGraph, cách chia tập, sơ đồ luồng dữ liệu, bảng input/output |
| 02_SPLIT_AND_LEAKAGE_AUDIT.md | Các giao thức đánh giá đã dùng, phân tích từng loại rò rỉ dữ liệu, checklist đầu vào, giao thức đề xuất |
| 03_MODEL_PROPOSAL.md | Baseline, vấn đề còn tồn tại, mô hình đề xuất, ablation, rủi ro |
| 04_PUBLIC_CODE_AND_REPRODUCIBILITY.md | Mã nguồn công khai liên quan, license, kế hoạch tái lập |
| 05_EXPERIMENT_PLAN.md | Câu hỏi nghiên cứu, danh sách thí nghiệm, tiêu chí kết luận |
| 06_EVIDENCE_AND_OPEN_ISSUES.md | Bảng mã bằng chứng, mâu thuẫn với tài liệu cũ, câu hỏi còn mở, lệnh tái lập, trạng thái nhiệm vụ |
| audit_scripts/ | Fact sheet, script audit dữ liệu, log kết quả, hai checker |
| .audit_progress.md | Nhật ký tiến độ kiểm toán: module nào đọc sâu, module nào chỉ kiểm kê |

## Quy ước

- Số liệu theo định dạng quốc tế: dấu chấm thập phân, dấu phẩy phân cách hàng nghìn.
- Mỗi nhận định quan trọng có một trong bốn nhãn: Đã xác minh, Suy luận, Đề xuất, Chưa xác định.
- Mã bằng chứng dạng E1, E2 trỏ tới một dòng trong bảng bằng chứng của file 06. Bảng đó ghi file, dòng code và mức xác minh.
- Đường dẫn file chỉ xuất hiện trong file 06 và README này, để các file 00 đến 05 đọc liền mạch.
- V3-sạch là tên của giao thức đánh giá chính. Giao thức chia tài khoản theo thời điểm giao dịch đầu tiên, rồi chỉ cho mô hình thấy giao dịch xảy ra tới 30 ngày sau thời điểm đó. File 01, mục 3 và 4 định nghĩa chi tiết.

## Thư mục audit_scripts

| File | Vai trò |
|---|---|
| facts.md | Fact sheet: mọi con số dùng trong docs, mỗi số kèm file nguồn |
| audit_data.py | Kiểm tra dữ liệu thật: shape, giá trị thiếu, nhãn theo tập, địa chỉ trùng, cạnh trùng, bất biến thời gian, bậc nút |
| audit_degree_artifact.py | Đo ảnh hưởng của tài khoản bậc 1 lên diện tích dưới đường Precision-Recall và ROC-AUC |
| derive_facts.py | Tính các số suy ra (phần trăm, trung bình) từ output audit |
| public_repos.sh | Tra license và ngày cập nhật của repo công khai qua GitHub API |
| check_research_docs.py | Checker nội dung: đủ file, nguồn của metric, mã bằng chứng, đường dẫn, dấu câu |
| *.log, *_out.json | Output của các script trên, là nguồn của fact sheet |

## Chạy lại kiểm tra

Chạy từ gốc repo Dynamic_Fusion. Các script audit cần Python có torch, numpy và scikit-learn. Môi trường ảo trong repo hiện không có torch.

```bash
python3 docs/research/audit_scripts/audit_data.py > docs/research/audit_scripts/audit_data.log
python3 docs/research/audit_scripts/audit_degree_artifact.py > docs/research/audit_scripts/audit_degree_artifact.log
python3 docs/research/audit_scripts/derive_facts.py > docs/research/audit_scripts/derive_facts.log
bash docs/research/audit_scripts/public_repos.sh > docs/research/audit_scripts/public_repos.log

# checker nội dung
python3 docs/research/audit_scripts/check_research_docs.py . docs/research

# checker ngôn ngữ (skill vietnamese nằm trong workspace, ngoài repo)
VIET=../.claude/vietnamese/scripts/viet.py
python3 $VIET facts docs/research/audit_scripts/facts.md
for f in docs/research/0*.md; do
  python3 $VIET check "$f" --audience thay-co --markdown-ok --facts docs/research/audit_scripts/facts.md
done
```

Khi sửa một con số trong docs, cập nhật fact sheet trước rồi chạy lại cả hai checker. Không sửa số chỉ để checker hết báo lỗi.

## Trạng thái

Bộ docs được viết ngày 2026-10-12. Tại thời điểm đó, cả bảy file 00 đến 06 qua checker ngôn ngữ và checker nội dung. Các file Markdown cũ của repo không bị sửa. Các điểm còn thiếu bằng chứng và các việc cần làm tiếp nằm ở file 06, mục 4, 6 và 7.
