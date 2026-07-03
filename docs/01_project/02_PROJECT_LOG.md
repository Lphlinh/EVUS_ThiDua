# PROJECT_LOG

## 2026-07-02
- Khởi tạo dự án EVUS_ThiDua.
- Project Root:
  `G:\My Drive\AI\AI_giao_duc\Au-Viet-My\EVUS_ThiDua`
- Phát triển độc lập với hệ thống chấm công.
- Triển khai trên subdomain của trường.
- Google Sheets là nguồn dữ liệu chính.
- Một giáo viên được chấm một lần mỗi tháng.

## 2026-07-03
- Kiểm tra và xác nhận môi trường phát triển local:
  - VS Code mở đúng thư mục dự án.
  - VS Code đã Trust Folder.
  - Git đã cài đặt.
  - Đã khởi tạo Git repository local.
  - Đã đổi nhánh mặc định sang `main`.
  - Python đã cài đặt.
  - Đã tạo môi trường ảo.
  - Đã cài dependencies.
  - Streamlit chạy local thành công.
- Đã đọc tài liệu nghiệp vụ `ThiDuaGVEVUS.docx`.
- Xác định chức năng chính: giáo viên tự chấm điểm thi đua hằng tháng.
- Thống nhất nghiệp vụ:
  - Một số tiêu chí hệ thống tự tính chỉ là điểm gợi ý.
  - Giáo viên được quyền điều chỉnh điểm trước khi nộp.
  - Khi giáo viên bấm hoàn thành, hệ thống phải cảnh báo phiếu sẽ bị khóa.
  - Phiếu đã khóa không cho giáo viên sửa, nhưng cho mở xem.
  - Giáo viên có thể tải phiếu đã nộp dưới dạng PDF.
  - BGH có quyền xem và sửa điểm thi đua.
  - BGH có thể xuất bảng chấm điểm thi đua toàn trường theo tháng.
- Thống nhất cần có:
  - trạng thái phiếu;
  - khóa GV;
  - khóa BGH;
  - Audit_Log;
  - cơ chế chốt tháng.
- Đã tạo repository GitHub:
  `https://github.com/Lphlinh/EVUS_ThiDua.git`
- Đã tạo Google Spreadsheet dữ liệu chính:
  - Tên: `EVUS_ThiDua_Data`
  - Spreadsheet ID: `14QZmgiaZZnhhd_j0v-imBQu258FXm3MB4acjv1razd0`
- Đã tạo Service Account:
  `evus-thidua@evus-thidua.iam.gserviceaccount.com`
- Đã chia sẻ Google Sheet cho Service Account với quyền Editor.
- Đã kiểm tra kết nối Google Sheets thành công.
- Ghi nhận sự cố bảo mật do JSON key từng bị hiển thị; quyết định xử lý:
  - xóa key cũ;
  - tạo key mới;
  - ghi đè file cấu hình local;
  - kiểm thử lại kết nối.

## 2026-07-04
- Hoàn thành bước kết nối Google Sheets Service.
- Đọc được `DM_GiaoVien`.
- Hoàn thành đăng nhập cơ bản bằng dữ liệu `DM_GiaoVien`.
- Đọc được `DM_TieuChi`.
- Chuyển trọng tâm từ giao diện sang lõi nghiệp vụ:
  - tạo phiếu `TH_ThiDua`;
  - sinh chi tiết `CT_ThiDua`;
  - lưu điểm;
  - tính tổng;
  - khóa phiếu;
  - ghi `Audit_Log`.
- Thống nhất tiêu đề phiếu:
  `Phiếu thi đua tháng MM/YYYY`, trong đó `MM/YYYY` là tháng trước so với ngày hiện tại.
- Thống nhất không cần hiển thị riêng "Năm học" trên giao diện nếu `MM/YYYY` đã đủ rõ.
- Bổ sung `04_PROJECT_STRUCTURE.md` làm tài liệu mô tả trạng thái hiện hành của dự án.
- Thống nhất `docs/01_Project/99_ProjectTree/project_tree.txt` là nguồn chuẩn phản ánh cây thư mục thực tế.
- Thống nhất khi bắt đầu phiên làm việc, AI phải đọc:
  1. `00_BOOT_CONTEXT.md`
  2. `01_PROJECT_RULES.md`
  3. `04_PROJECT_STRUCTURE.md`
  4. `02_PROJECT_LOG.md`
  5. `03_TODO.md`
- Thống nhất quy trình cập nhật cây thư mục:
  ```powershell
  tree /F /A > docs\01_Project\99_ProjectTree\project_tree.txt
  ```
- Thống nhất các mẫu nghiệp vụ chuẩn thuộc nhóm tài liệu thiết kế và nên quản lý trong `docs/03_Design/`.
