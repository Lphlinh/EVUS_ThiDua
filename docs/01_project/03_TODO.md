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

## M04
- [ ] Tổng hợp năm học
- [ ] Xếp loại năm học
- [ ] Xuất Excel năm học
- [ ] Báo cáo theo giáo viên
- [ ] Báo cáo theo tổ chuyên môn
