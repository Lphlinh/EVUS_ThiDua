# PROJECT_LOG

## 2026-07-02
- Khởi tạo dự án EVUS_ThiDua.
- Project Root:
  G:\My Drive\AI\AI_giao_duc\Au-Viet-My\EVUS_ThiDua
- Phát triển độc lập với hệ thống chấm công.
- Triển khai trên subdomain của trường.
- Google Sheets là nguồn dữ liệu chính.
- Một giáo viên được chấm một lần mỗi tháng.

## 2026-07-03
- Bắt đầu phiên làm việc đầu tiên của dự án EVUS_ThiDua.
- Đã kiểm tra và xác nhận môi trường phát triển local:
  - VS Code mở đúng thư mục dự án.
  - VS Code đã Trust Folder.
  - Git đã cài đặt: 2.53.0.windows.2.
  - Đã khởi tạo Git repository local.
  - Đã đổi nhánh mặc định từ master sang main.
  - Python đã cài đặt: 3.13.13.
  - Đã tạo và kích hoạt môi trường ảo .venv.
  - Đã cài dependencies từ requirements.txt.
  - Streamlit đã chạy local thành công.
- Ghi nhận cảnh báo VS Code liên quan Google Cloud CLI và Gemini Code Assist không ảnh hưởng đến EVUS_ThiDua ở giai đoạn hiện tại.
- Đã đọc tài liệu nghiệp vụ ThiDuaGVEVUS.docx và xác định chức năng chính: giáo viên tự chấm điểm thi đua hằng tháng.
- Thống nhất nghiệp vụ bổ sung:
  - Một số tiêu chí hệ thống tự tính chỉ là điểm gợi ý.
  - Giáo viên được quyền điều chỉnh điểm trước khi nộp.
  - Khi giáo viên bấm Hoàn thành, hệ thống phải hiển thị cảnh báo rằng sau khi xác nhận thì phiếu sẽ bị khóa.
  - Sau khi giáo viên xác nhận lưu, phiếu chuyển trạng thái đã nộp/đã khóa.
  - Giáo viên không được chỉnh sửa phiếu đã khóa, nhưng vẫn được mở xem.
  - Giáo viên có thể tải phiếu đã nộp dưới dạng PDF.
  - BGH có quyền xem và sửa điểm thi đua của giáo viên.
  - Mỗi tháng BGH có thể xuất bảng chấm điểm thi đua toàn trường dạng Excel.
  - File Excel tháng dự kiến gồm mỗi giáo viên một sheet và có thể có sheet tổng hợp phục vụ BGH.
- Thống nhất đề xuất bổ sung nghiệp vụ:
  - Cần có trạng thái phiếu: chưa tạo, đang nhập, đã nộp, BGH đã chỉnh sửa, đã chốt.
  - Nên có nhật ký chỉnh sửa (Audit Log) cho các thao tác quan trọng như nộp phiếu, BGH sửa điểm, chốt tháng, mở khóa.
  - Nên có cơ chế khóa/chốt dữ liệu theo tháng để hạn chế thay đổi sau khi tổng hợp.
- Bổ sung quy tắc làm việc:
  - Khi AI chỉnh sửa tài liệu dự án, AI phải xuất file ZIP chứa đúng cấu trúc thư mục tương ứng trong project.
  - Người dùng giải nén ZIP vào đúng thư mục gốc dự án để ghi đè/cập nhật tài liệu.
  - Không tự sửa trực tiếp file trong project khi chưa có xác nhận.
