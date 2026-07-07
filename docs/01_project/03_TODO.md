# TODO

## M01
- [x] Khởi tạo dự án
- [x] Kết nối GitHub
- [x] Kết nối Google Sheets
- [x] Baseline + push GitHub

## M02
- [x] Tạo dịch vụ đọc Google Sheets
- [x] Đọc danh mục giáo viên `DM_GiaoVien`
- [x] Thiết kế luồng đăng nhập cơ bản
- [x] Đăng nhập bằng dữ liệu `DM_GiaoVien`
- [x] Đọc danh mục tiêu chí `DM_TieuChi`
- [ ] Chuẩn hóa dữ liệu `DM_TieuChi` từ mẫu phiếu tháng
- [x] Thiết kế nghiệp vụ tạo phiếu `TH_ThiDua`
- [x] Thiết kế nghiệp vụ sinh chi tiết `CT_ThiDua`
- [x] Thiết kế nghiệp vụ Form chấm điểm
- [x] Thiết kế nghiệp vụ lưu chi tiết `CT_ThiDua`
- [x] Thiết kế nghiệp vụ tính tổng điểm
- [x] Thiết kế nghiệp vụ khóa phiếu sau khi giáo viên hoàn thành
- [x] Thiết kế nghiệp vụ cho giáo viên xem lại phiếu đã khóa
- [x] Thiết kế nghiệp vụ xuất PDF phiếu giáo viên
- [ ] Đặc tả kỹ thuật M02
- [ ] Lập trình model `TH_ThiDua`
- [ ] Lập trình model `CT_ThiDua`
- [ ] Lập trình service tạo phiếu
- [ ] Lập trình service sinh chi tiết phiếu
- [ ] Lập trình form chấm điểm *(giữ nền giao diện v14, chưa tiếp tục refactor rộng)*
- [x] Lập trình lưu dữ liệu `CT_ThiDua` *(PASS bản v14.7: lưu, đọc lại, chống trùng CT_ThiDua)*
- [x] Lập trình tính tổng điểm *(PASS: tổng toàn phiếu, GROUP, SECTION chỉ tính ITEM)*
- [x] Lập trình xác nhận nộp và khóa phiếu *(PASS: cảnh báo, nộp lần 2, khóa GV, đọc lại đúng)*
- [ ] Lập trình xem lại phiếu
- [ ] Lập trình xuất PDF
- [x] Kiểm thử local M02 *(PASS lưu điểm thành phần: đổi điểm → Lưu → đăng xuất → đăng nhập lại)*
- [ ] Commit + push M02

### M02 - Kiểm thử lưu điểm thành phần v14.7
- [x] Kiểm thử sửa 1 tiêu chí → Lưu → đăng xuất → đăng nhập.
- [x] Kiểm thử sửa nhiều tiêu chí cùng lúc → Lưu.
- [x] Kiểm thử sửa điểm rồi trả về điểm mặc định → Lưu.
- [x] Đối chiếu `CT_ThiDua.DiemGV` trên Google Sheets sau khi mở lại phiếu.
- [ ] Trạng thái nút Lưu/Xác nhận.
- [x] Tổng theo GROUP.
- [ ] Sticky Header.
- [x] Tối ưu tốc độ nhập liệu *(Google Sheets cache: 34.71s → 0.21s).*


### M02 - Hiệu năng và nộp phiếu
- [x] Cache `gspread.Client`.
- [x] Cache Spreadsheet.
- [x] Cache Worksheet.
- [x] Cache `read_sheet_records()`.
- [x] Tối ưu tốc độ mở phiếu *(34.71s → 0.21s)*.
- [x] Hiển thị tổng theo GROUP.
- [x] Hiển thị tổng theo SECTION.
- [x] Hoàn thiện cảnh báo thiếu giải trình bằng mã hiển thị.
- [x] Hoàn thiện luồng nộp phiếu.
- [x] Khóa phiếu sau khi nộp.
- [x] Chuẩn hóa đọc `TH_ThiDua`.
- [x] Áp dụng quy tắc Trace-first khi xử lý lỗi chưa rõ nguyên nhân.

### Pilot hardening - Hiệu năng luồng Giáo viên 2026-07-07
- [x] Đối chiếu luồng BGH nhanh với luồng GV chậm.
- [x] Đo sâu `thi_dua_service.get_phieu()`.
- [x] Đo sâu `thi_dua_service.get_chi_tiet_phieu()`.
- [x] Đo vòng chạy `render_teacher_score_page()` để loại trừ rerun bất thường.
- [x] Đo cấp thấp Google Sheets: `get_gspread_client()`, `open_spreadsheet()`, `get_worksheet()`, `worksheet.get_all_values()`.
- [x] Xác định nguyên nhân chính nằm ở lớp Google Sheets API, không nằm ở nghiệp vụ M02/M03.
- [x] Tối ưu Worksheet Catalog Cache để tránh gọi `spreadsheet.worksheet()` riêng lẻ nhiều lần.
- [x] Bổ sung warm-up Google Sheets sau đăng nhập.
- [x] Gỡ các bộ đo tạm và giữ bản sạch sau tối ưu.
- [x] Chốt không tiếp tục tối ưu hiệu năng nếu chưa có bằng chứng mới.

## M03
- [x] Màn hình BGH
- [x] BGH xem phiếu theo tháng
- [x] BGH chỉnh sửa điểm thi đua
- [x] Ghi `Audit_Log` khi BGH chỉnh sửa
- [x] Chốt tháng
- [x] Tổng hợp tháng
- [x] Xuất Excel toàn trường theo tháng


### M03 - Trạng thái kiểm thử hiện tại
- [x] Điều hướng theo vai trò Giáo viên/BGH.
- [x] Tạo và đăng nhập tài khoản BGH kiểm thử.
- [x] BGH xem danh sách phiếu theo tháng.
- [x] Khử trùng danh sách phiếu theo `TH_ThiDua.ID` khi dữ liệu test có dòng trùng.
- [x] BGH mở phiếu giáo viên.
- [x] BGH nhập `DiemBGH`.
- [x] BGH nhập `GhiChuBGH` bằng form dùng chung, không còn lỗi phím `c`.
- [x] BGH lưu điểm và ghi chú xuống Google Sheets.
- [x] Đọc lại điểm/ghi chú BGH sau đăng xuất/đăng nhập.
- [x] Kiểm thử riêng dòng `Audit_Log` khi BGH chỉnh sửa.
- [x] Kiểm thử nhiều giáo viên, gồm giáo viên mới tạo.
- [x] Chốt tháng.
- [x] Cảnh báo giáo viên chưa nộp/chưa có phiếu trước khi chốt tháng.
- [x] Tổng hợp tháng.
- [x] Tự tạo worksheet `TongHop_ThiDua` nếu chưa có.
- [x] Kiểm thử chạy lại tổng hợp tháng không tạo dòng trùng.
- [x] Kiểm thử phục hồi `TH_ThiDua.ID` khi bị sai nhưng đủ dữ liệu hợp lệ.
- [x] Xuất Excel tháng.
- [x] Kiểm thử Excel lấy dữ liệu từ `TongHop_ThiDua`, không đọc lại `CT_ThiDua`.


## Pilot v1.0-beta
- [x] Thống nhất triển khai thực tế ít nhất 02 tháng trước khi phát triển M04.
- [x] Chuẩn hóa đăng nhập theo vai trò: `GV` và `BGH`.
- [x] Giáo viên đăng nhập bằng `GV` + `Mã GV`.
- [x] Ban Giám hiệu đăng nhập bằng `BGH` + mật khẩu ban đầu `BGH123abc456`.
- [x] Chuyển ô nhập tài khoản sang chọn `Giáo viên` / `Ban Giám hiệu`.
- [x] Bổ sung khu vực `Quản trị hệ thống` cho BGH.
- [x] Bổ sung cấu hình ngày cuối tự chấm.
- [x] Bổ sung chức năng khởi tạo mật khẩu cho tài khoản mới.
- [x] Loại bỏ nút đặt lại mật khẩu toàn bộ.
- [x] Tạo tài liệu hướng dẫn sử dụng nhanh.
- [ ] Tạo Git tag `v1.0-beta`.
- [ ] Gửi link GitHub/Release cho trường.

### Pilot - Theo dõi vận hành
- [x] Thống nhất chuyển sang cho trường chạy thực tế trong khoảng 02 tháng.
- [x] Thống nhất đóng băng chức năng trong giai đoạn Pilot, không phát triển chức năng mới nếu không thật sự bắt buộc.
- [ ] Ghi nhận phản ánh thực tế từ giáo viên.
- [ ] Ghi nhận phản ánh thực tế từ Ban Giám hiệu.
- [ ] Phân loại phản ánh: bug / giao diện / nghiệp vụ / hiệu năng.
- [ ] Gom bản vá theo phiên bản nhỏ `v1.0.1`, `v1.0.2`, ... nếu cần.
- [ ] Sau ít nhất 02 tháng, tổng kết Pilot trước khi quyết định M04.

### Pilot - Hiệu năng
- [x] Hiệu năng luồng Giáo viên đạt mức chấp nhận được sau tối ưu 2026-07-07.
- [x] Không tiếp tục tối ưu Google Sheets nếu không có bằng chứng mới.
- [ ] Theo dõi phản ánh hiệu năng trong vận hành thực tế.
- [ ] Chỉ mở lại điều tra hiệu năng khi dữ liệu tăng mạnh, cache không hoạt động, hoặc người dùng phản ánh chậm bất thường.


### Pilot (chạy thử nghiệm) - Xuất Excel tháng mẫu mới
- [x] Thiết kế mẫu Excel tháng mới.
- [x] Sheet `TongHop_Thang` mở rộng theo từng tiêu chí.
- [x] Sheet `TongHop_Thang` dùng điểm chính thức theo quy tắc: có `DiemBGH` thì dùng `DiemBGH`, không có thì dùng `DiemGV`.
- [x] Mỗi giáo viên có một sheet phiếu chi tiết trong file Excel tháng.
- [x] Kiểm thử xuất Excel mẫu mới và đối chiếu với dữ liệu BGH đã duyệt.
- [x] Xuất Excel tháng mẫu mới PASS bằng dữ liệu thực tế và đúng kỳ vọng nghiệp vụ.

## M04
- [ ] Tổng hợp năm học
- [ ] Xếp loại năm học
- [ ] Xuất Excel năm học
- [ ] Báo cáo theo giáo viên
- [ ] Báo cáo theo tổ chuyên môn
Đánh dấu hoàn thành:

### Pilot - Giao diện Giáo viên
- [x] Thu gọn Header.
- [x] Thu gọn thông tin phiếu.
- [x] Tách khối thao tác.
- [x] Cảnh báo thiếu giải trình trong khu vực thao tác.
- [x] Hoàn thiện luồng Lưu.
- [x] Hoàn thiện luồng Xác nhận nộp.
- [x] Hoàn thiện luồng Đồng ý/Hủy.
- [x] Hoàn thiện giao diện Pilot Giáo viên.

Thêm mục ưu tiên tiếp theo:

### Pilot (chạy thử nghiệm) - Kiểm thử Ban Giám hiệu
- [x] Kiểm thử hồi quy giao diện BGH sau các thay đổi dùng chung.
- [x] Kiểm thử sửa điểm BGH.
- [x] Kiểm thử lưu và đọc lại.
- [x] Kiểm thử Chốt tháng.
- [x] Kiểm thử Tổng hợp tháng.
- [x] Kiểm thử Xuất Excel.

## Trạng thái bàn giao Pilot (chạy thử nghiệm) - 2026-07-07
- [x] M02 Giáo viên PASS.
- [x] M03 Ban Giám hiệu PASS.
- [x] Chốt tháng PASS.
- [x] Tổng hợp tháng PASS.
- [x] Xuất Excel tháng mẫu mới PASS.
- [x] Thống nhất chuyển sang giai đoạn vận hành thực tế tại trường trong khoảng 02 tháng.
- [x] Thống nhất chỉ theo dõi vận hành và xử lý bug / hiệu năng / phản hồi cần thiết trong giai đoạn Pilot.
- [ ] Sau 02 tháng, tổng kết dữ liệu vận hành trước khi quyết định M04.
