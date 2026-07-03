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
- Thống nhất quy ước lưu tài liệu:
  - Repository Git chỉ lưu source code, file cấu hình, tài liệu Markdown chính thức và tài nguyên cần thiết cho chương trình.
  - File ZIP, DOCX, PDF, bản trung gian và bản sao lưu lưu trong backup/.
  - Có thể phân nhóm backup/Business/, backup/Docs_Update/ hoặc nhóm khác khi cần.
- Thống nhất cấu trúc mã nguồn chuẩn trong app/:
  - auth/: đăng nhập, xác thực, phân quyền.
  - components/: thành phần giao diện dùng chung.
  - models/: mô hình dữ liệu.
  - pages/: các màn hình Streamlit.
  - services/: Google Sheets, PDF, Excel và nghiệp vụ liên quan.
  - utils/: hàm tiện ích không chứa nghiệp vụ chính.
- Đã tạo commit baseline:
  - Commit: 1af9e39
  - Message: Baseline: Initialize EVUS_ThiDua project
- Đã tạo repository GitHub:
  - https://github.com/Lphlinh/EVUS_ThiDua.git
- Đã push nhánh main lên GitHub thành công.
- Đã cập nhật .gitignore để loại trừ dữ liệu nhạy cảm và thư mục backup.
- Đã commit và push cập nhật tài liệu/rules:
  - Commit: d6a516b
  - Message: docs: update project rules and project log
- Đã tạo Google Spreadsheet dữ liệu chính:
  - Tên: EVUS_ThiDua_Data
  - Spreadsheet ID: 14QZmgiaZZnhhd_j0v-imBQu258FXm3MB4acjv1razd0
- Đã tạo Google Cloud Project mới ngoài Organization để cho phép tạo JSON key cho Service Account.
- Đã bật Google Sheets API và Google Drive API.
- Đã tạo Service Account:
  - evus-thidua@evus-thidua.iam.gserviceaccount.com
- Đã chia sẻ Google Sheet cho Service Account với quyền Editor.
- Đã kiểm tra kết nối Google Sheets bằng gspread thành công, trả về tên spreadsheet: EVUS_ThiDua_Data.
- Ghi nhận sự cố bảo mật: nội dung service_account.json đã bị hiển thị trong trao đổi. Quyết định xử lý:
  - Xóa JSON key cũ trên Google Cloud.
  - Tạo JSON key mới.
  - Ghi đè config/service_account.json.
  - Kiểm thử lại kết nối Google Sheets.

## Quyết định dữ liệu đã thống nhất
- Danh sách worksheet chuẩn:
  - DM_GiaoVien
  - DM_TieuChi
  - TH_ThiDua
  - CT_ThiDua
  - TongHop_ThiDua
  - Audit_Log
  - System_Config
- Dùng mô hình Header-Detail:
  - TH_ThiDua: 1 dòng = 1 phiếu tháng của 1 giáo viên.
  - CT_ThiDua: 1 dòng = 1 tiêu chí trong 1 phiếu.
- TongHop_ThiDua không nhập tay; chỉ do hệ thống sinh hoặc cập nhật tự động từ dữ liệu gốc.
- Không lưu họ tên, tổ, email, chức vụ trong bảng nghiệp vụ TH_ThiDua và CT_ThiDua; chỉ lưu Mã GV. Thông tin hiển thị lấy từ DM_GiaoVien.
- Primary Key:
  - DM_GiaoVien: Mã GV.
  - DM_TieuChi: Mã TC.
  - TH_ThiDua.ID = Năm học + "_" + Tháng + "_" + Mã GV. Ví dụ: 2026-2027_09_GV001.
  - CT_ThiDua.ID = ID Phiếu + "_" + Mã TC. Ví dụ: 2026-2027_09_GV001_TC01.
  - Audit_Log.ID dùng UUID hoặc timestamp do chương trình sinh.
- TH_ThiDua có 2 khóa nghiệp vụ:
  - Khóa GV: giáo viên không được sửa khi TRUE.
  - Khóa BGH: BGH không được sửa khi TRUE.
- Audit_Log chỉ ghi thao tác quan trọng, không ghi thao tác xem dữ liệu.
- System_Config lưu trạng thái phiếu, vai trò, năm học hiện hành, tháng chấm hiện hành, hạn nộp và danh mục xếp loại.
- DM_TieuChi lưu giới hạn Min-Max, trọng số, có tính vào tổng hay không, loại tiêu chí AUTO/MANUAL/HYBRID và quy tắc gợi ý.

## Quy tắc làm việc bổ sung đã thống nhất
- AI được chủ động áp dụng các giải pháp kỹ thuật tốt nếu an toàn và không ảnh hưởng kiến trúc, dữ liệu hoặc nghiệp vụ.
- AI chỉ dừng để trao đổi khi vấn đề có ảnh hưởng đến kiến trúc, dữ liệu, nghiệp vụ, bảo mật hoặc khả năng bảo trì lâu dài.
- Các bước kỹ thuật trung gian trình bày ngắn gọn.
- Khi yêu cầu người dùng thao tác, phải ghi rõ thao tác cụ thể; cuối bước có thể chỉ ghi: Gõ 1 để tiếp tục.
- Khi tạo file mới, phải ghi rõ đường dẫn đầy đủ và tên file.
- Nếu thay đổi nhiều file hoặc nội dung dài, AI phải xuất ZIP đúng cấu trúc dự án.
- AI không được nói đã cập nhật khi chưa tạo file/ZIP tương ứng để người dùng áp dụng.


## 2026-07-03 (M02)
- Bắt đầu M02 theo quy trình đọc 4 tài liệu dự án.
- Thống nhất ưu tiên xử lý môi trường phát triển trước khi viết thêm chức năng.
- Ghi nhận kế hoạch di chuyển .venv sang ổ đĩa local để khắc phục hiện tượng chậm khi đặt trong Google Drive.
