# PROJECT_RULES

## Mục tiêu
Xây dựng phần mềm ổn định, đơn giản, dễ bảo trì và dễ mở rộng.

## Quy tắc chung
1. Không suy luận khi chưa có dữ liệu.
2. Hiểu nghiệp vụ trước khi viết code.
3. Không thay đổi kiến trúc, cấu trúc dữ liệu hoặc Google Sheets khi chưa thống nhất.
4. Google Sheets là nguồn dữ liệu chính.
5. Excel chỉ dùng để nhập/xuất dữ liệu hoặc làm biểu mẫu nghiệp vụ.
6. Ưu tiên an toàn và khả năng bảo trì hơn tốc độ.
7. Không mở rộng phạm vi khi chưa thống nhất.
8. Một thay đổi chỉ giải quyết một nhóm vấn đề rõ ràng.
9. Không xóa dữ liệu khi có thể cập nhật.
10. Backup trước thay đổi lớn.
11. Chỉ kết luận từ code, dữ liệu hoặc nghiệp vụ đã xác nhận.
12. Thiếu thông tin nghiệp vụ, dữ liệu, bảo mật hoặc kiến trúc thì phải hỏi lại.

## Quy tắc làm việc với người dùng
1. AI được chủ động xử lý các vấn đề kỹ thuật thông thường nếu phương án rõ ràng, an toàn và không ảnh hưởng kiến trúc, dữ liệu, nghiệp vụ hoặc bảo mật.
2. Không trình bày dài các bước kỹ thuật trung gian.
3. Chỉ dừng để trao đổi khi vấn đề ảnh hưởng đến:
   - kiến trúc;
   - mô hình dữ liệu;
   - nghiệp vụ;
   - bảo mật;
   - khả năng bảo trì lâu dài;
   - quy trình sử dụng của người dùng.
4. Khi cần người dùng thao tác, phải ghi rõ thao tác cụ thể.
5. Khi tạo file mới, phải ghi rõ đường dẫn đầy đủ và tên file.
6. Nếu thay đổi nhiều file hoặc nội dung dài, phải xuất ZIP đúng cấu trúc dự án để người dùng giải nén vào thư mục gốc.
7. Không được nói đã cập nhật, đã tạo file hoặc đã tạo ZIP khi chưa thực sự tạo.

## Quy tắc Git
1. Sau khi kiểm thử PASS mới commit và push GitHub.
2. Không commit file chứa khóa bí mật hoặc thông tin xác thực, đặc biệt:
   - `config/service_account.json`
   - `.streamlit/secrets.toml`
   - `.env`
3. Không commit file test tạm, log tạm, `__pycache__`, hoặc file sinh tự động không cần thiết.
4. File ZIP bàn giao, DOCX, PDF, bản trung gian và bản sao lưu không phải tài liệu chính thức thì lưu trong `backup/`.

## Quy tắc dữ liệu
1. Không tạo dữ liệu trùng: 01 giáo viên + 01 tháng = 01 phiếu thi đua.
2. Bảng nghiệp vụ chỉ lưu mã định danh cần thiết, không lặp lại thông tin danh mục.
3. `DM_GiaoVien` là nguồn thông tin giáo viên.
4. `DM_TieuChi` là nguồn sinh chi tiết phiếu `CT_ThiDua`.
5. `TH_ThiDua` là Header; `CT_ThiDua` là Detail.
6. Giáo viên chấm trên `CT_ThiDua`; `TH_ThiDua` lưu trạng thái và tổng hợp.
7. `Audit_Log` chỉ ghi thao tác quan trọng, không ghi thao tác xem dữ liệu.

## Quy tắc tài liệu
1. Quyết định quan trọng phải ghi vào `PROJECT_LOG`.
2. Cấu trúc hiện hành phải ghi vào `PROJECT_STRUCTURE`.
3. Việc cần làm phải ghi vào `TODO`.
4. Quy tắc làm việc phải ghi vào `PROJECT_RULES`.
5. Bối cảnh khởi động phiên phải ghi vào `BOOT_CONTEXT`.

## Bổ sung quy tắc sửa lỗi giao diện/nghiệp vụ M02

1. Khi một bản sửa làm mất chức năng nhập liệu hoặc làm sai dữ liệu, phải rollback về bản ổn định gần nhất trước khi sửa tiếp.
2. Không refactor đồng thời giao diện, session state, service lưu dữ liệu và cách tính tổng nếu mục tiêu chỉ là sửa một lỗi lưu dữ liệu.
3. Không dùng HTML/JavaScript thay thế control nhập liệu chính khi chưa có kiểm thử chứng minh dữ liệu được ghi đúng vào Google Sheets.
4. Khi sửa luồng lưu, phải kiểm tra đủ chu trình: nhập điểm → lưu → đăng xuất → đăng nhập lại → đối chiếu Google Sheets.
5. Khi thêm bẫy lỗi, thông báo phải chỉ rõ thiếu cột, sai ID dòng hoặc không tìm thấy dữ liệu liên quan.

## Quy tắc quản lý phụ thuộc mã nguồn

1. Trước khi sửa bất kỳ hàm hoặc file nào, phải tra cứu:
   - `docs/03_Design/PY_RELATION_MAP.md`
   - `docs/03_Design/evus_py_dependency_map.json`

2. Phải xác định rõ:
   - hàm gọi đến hàm đang sửa;
   - hàm được gọi bởi hàm đang sửa;
   - màn hình bị ảnh hưởng;
   - service dùng chung;
   - bảng Google Sheets liên quan.

3. Chỉ sau khi xác định đầy đủ phạm vi ảnh hưởng mới được sửa mã nguồn.

4. Sau mỗi bản sửa phải kiểm thử hồi quy đúng các chức năng có liên quan theo bản đồ phụ thuộc.

5. Không sửa theo từng lỗi riêng lẻ khi chưa xác định đầy đủ các mối liên quan của hàm hoặc module đó.

6. Nếu phát hiện một hàm được cả Giáo viên và Ban Giám hiệu dùng chung thì bắt buộc kiểm thử cả hai vai trò trước khi commit.

7. Khi thêm hoặc thay đổi hàm dùng chung hoặc hàm nghiệp vụ quan trọng, phải cập nhật lại:
   - `docs/03_Design/PY_RELATION_MAP.md`
   - `docs/03_Design/evus_py_dependency_map.json`

8. Nếu bản sửa có nguy cơ ảnh hưởng chéo giữa Giáo viên và Ban Giám hiệu, phải dừng lại để xác định phạm vi kiểm thử trước khi viết code.

