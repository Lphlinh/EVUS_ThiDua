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
## 2026-07-04

- Thống nhất thời gian giáo viên tự chấm phiếu thi đua:
  - Từ ngày 01 đến ngày 05 hằng tháng.
- Khi giáo viên bấm "Xác nhận nộp phiếu":
  - Hệ thống phải hiển thị hộp thoại xác nhận.
  - Nội dung thông báo:

    "Sau khi xác nhận, phiếu thi đua được xem như đã được Thầy/Cô ký xác nhận và gửi về Ban Giám hiệu. Thầy/Cô sẽ không thể chỉnh sửa nội dung phiếu sau bước này.

    Thầy/Cô có chắc chắn muốn xác nhận và nộp phiếu không?"

- Sau khi giáo viên xác nhận:
  - Phiếu chuyển trạng thái "Đã nộp".
  - Khóa quyền chỉnh sửa của giáo viên.
  - Phiếu được chuyển đến Ban Giám hiệu để xem xét.
  - Ghi Audit_Log.
  ### Bổ sung quy trình sau thời hạn tự chấm

* Thời gian giáo viên tự chấm phiếu thi đua hằng tháng: **từ ngày 01 đến ngày 05**.

* Sau ngày 05:

  * Nếu giáo viên **chưa có phiếu**, hệ thống **không tự tạo phiếu**.
  * Hệ thống hiển thị thông báo:

    > Đã hết thời gian tự chấm phiếu thi đua của tháng này (từ ngày 01 đến ngày 05 hằng tháng). Nếu có lý do đặc biệt, Thầy/Cô vui lòng liên hệ Ban Giám hiệu để được xem xét mở quyền chấm bổ sung.

* Ban Giám hiệu có quyền xử lý các trường hợp đặc biệt:

  * Mở quyền chấm bổ sung cho giáo viên chưa có phiếu.
  * Tạo phiếu nếu giáo viên chưa có phiếu.
  * Mở khóa phiếu đã tạo khi cần cho phép giáo viên chỉnh sửa bổ sung.

* Mọi thao tác mở quyền, tạo phiếu sau thời hạn hoặc mở khóa của Ban Giám hiệu đều phải ghi vào `Audit_Log`, bao gồm:

  * Người thực hiện.
  * Thời gian thực hiện.
  * Giáo viên được tác động.
  * Lý do thực hiện.


## 2026-07-04 - M02: Chốt thiết kế nghiệp vụ phiếu thi đua tháng

- Thống nhất kiến trúc dữ liệu M02 gồm các worksheet chính:
  - `DM_GiaoVien`
  - `DM_TieuChi`
  - `TH_ThiDua`
  - `CT_ThiDua`
  - `TongHop_ThiDua`
  - `Audit_Log`
  - `System_Config`
- Thống nhất quan hệ dữ liệu:
  ```text
  DM_GiaoVien
        ↓
  TH_ThiDua
        ↓
  CT_ThiDua
        ↓
  TongHop_ThiDua
  ```
- Thống nhất bảng nghiệp vụ chỉ lưu mã định danh, không lặp lại thông tin danh mục.
- Thống nhất `DM_TieuChi` là nguồn duy nhất điều khiển:
  - sinh phiếu;
  - sinh giao diện;
  - sinh `CT_ThiDua`.
- Thống nhất `DM_TieuChi` có 3 loại:
  - `GROUP`
  - `SECTION`
  - `ITEM`
- Chỉ tiêu chí `ITEM` sinh dữ liệu trong `CT_ThiDua`.
- `GROUP` và `SECTION` chỉ dùng để hiển thị và tính tổng theo nhóm nếu cần.
- Không viết cứng tiêu chí trong mã nguồn.

### TH_ThiDua

- Thống nhất mỗi giáo viên có tối đa 01 phiếu thi đua trong 01 tháng.
- `TH_ThiDua` là Header của phiếu, không lưu chi tiết điểm từng tiêu chí.
- Khóa chính `TH_ThiDua.ID`:
  ```text
  NamHoc_Thang_MaGV
  ```
- Cấu trúc `TH_ThiDua` đã chốt:
  - `ID`
  - `NamHoc`
  - `Thang`
  - `MaGV`
  - `TrangThai`
  - `TongDiem`
  - `KhoaGV`
  - `KhoaBGH`
  - `NgayTao`
  - `NgayCapNhat`
  - `NgayNop`
  - `NguoiCapNhatCuoi`
  - `NguoiNop`
  - `GhiChuBGH`
  - `LanNop`
  - `LanMoKhoa`
- Trạng thái phiếu dùng mã số:
  - `1`: Chưa tạo
  - `2`: Đang chấm
  - `3`: Đã nộp
  - `4`: BGH đã chỉnh sửa
  - `5`: Đã chốt
- Khi tạo phiếu:
  - `TrangThai = 2`
  - `TongDiem = 0`
  - `KhoaGV = FALSE`
  - `KhoaBGH = FALSE`
  - `LanNop = 0`
  - `LanMoKhoa = 0`
- Khi giáo viên lưu:
  - cập nhật `TongDiem`;
  - cập nhật `NgayCapNhat`;
  - cập nhật `NguoiCapNhatCuoi`;
  - không đổi trạng thái phiếu.
- Khi giáo viên xác nhận nộp:
  - `TrangThai = 3`
  - `KhoaGV = TRUE`
  - `NgayNop = NOW()`
  - `NguoiNop = MaGV`
  - `LanNop = LanNop + 1`
  - ghi `Audit_Log`.
- Khi BGH mở khóa:
  - `TrangThai = 2`
  - `KhoaGV = FALSE`
  - `LanMoKhoa = LanMoKhoa + 1`
  - ghi `Audit_Log`.

### CT_ThiDua

- `CT_ThiDua` là Detail của phiếu.
- Mỗi dòng `CT_ThiDua` tương ứng 01 tiêu chí `ITEM` trong `DM_TieuChi`.
- Không sinh `CT_ThiDua` cho `GROUP` và `SECTION`.
- Khóa chính `CT_ThiDua.ID`:
  ```text
  IDPhieu_MaTC
  ```
- Cấu trúc `CT_ThiDua` đã chốt:
  - `ID`
  - `IDPhieu`
  - `MaTC`
  - `DiemMacDinh`
  - `DiemGV`
  - `DiemBGH`
  - `GhiChuGV`
  - `GhiChuBGH`
  - `NgayCapNhat`
  - `NguoiCapNhat`
- Khi sinh `CT_ThiDua`:
  - chỉ lấy `DM_TieuChi.Loai = ITEM`;
  - `DiemGV = DiemMacDinh`;
  - `DiemBGH = rỗng`;
  - `GhiChuGV = rỗng`;
  - `GhiChuBGH = rỗng`.
- Giáo viên chỉ được cập nhật:
  - `DiemGV`
  - `GhiChuGV`
- BGH chỉ được cập nhật:
  - `DiemBGH`
  - `GhiChuBGH`
- Không cho phép thêm, xóa hoặc đổi khóa dòng `CT_ThiDua` trong quá trình chấm.

### Quy tắc điểm

- `DiemMacDinh` là điểm gợi ý từ `DM_TieuChi`.
- Khi tạo phiếu, `DiemGV = DiemMacDinh`.
- Tiêu chí giữ nguyên điểm mặc định được xem là đã chấm.
- Giáo viên được phép lưu khi chưa rà soát hết tiêu chí.
- Khi `DiemGV != DiemMacDinh`, giáo viên bắt buộc nhập `GhiChuGV`.
- Nếu giáo viên sửa điểm rồi đưa lại bằng `DiemMacDinh`, không bắt buộc giải trình.
- `DiemBGH` chỉ lưu khi `DiemBGH != DiemGV`.
- Nếu BGH đồng ý với điểm giáo viên, để `DiemBGH` rỗng.
- Điểm chính thức:
  ```text
  Nếu DiemBGH có giá trị
      dùng DiemBGH
  Ngược lại
      dùng DiemGV
  ```
- `TH_ThiDua.TongDiem` là tổng điểm chính thức của toàn bộ dòng `CT_ThiDua` thuộc phiếu.

### Quy trình giáo viên

- Giáo viên đăng nhập.
- Hệ thống xác định tháng chấm mặc định là tháng trước so với ngày hiện tại.
- Nếu chưa có phiếu và còn trong thời gian từ ngày 01 đến ngày 05:
  - tự tạo `TH_ThiDua`;
  - tự sinh `CT_ThiDua` từ `DM_TieuChi`;
  - mở form chấm điểm.
- Nếu sau ngày 05 và giáo viên chưa có phiếu:
  - hệ thống không tự tạo phiếu;
  - hiển thị thông báo hết hạn;
  - giáo viên liên hệ BGH nếu cần mở quyền bổ sung.
- Giáo viên được bấm `Lưu` nhiều lần trong thời gian được phép.
- Nút `Lưu` ghi ngay xuống Google Sheets, chỉ ghi các dòng thay đổi, không ghi `Audit_Log`.
- Khi giáo viên bấm `Xác nhận nộp phiếu`, hệ thống hiển thị hộp thoại xác nhận đã thống nhất.
- Sau khi xác nhận nộp:
  - phiếu chuyển trạng thái `Đã nộp`;
  - khóa quyền chỉnh sửa của giáo viên;
  - ghi `Audit_Log`.

### Quy trình BGH

- BGH có quyền:
  - tạo phiếu sau thời hạn;
  - mở quyền chấm bổ sung;
  - mở khóa phiếu;
  - xem phiếu đã nộp;
  - chỉnh sửa điểm BGH;
  - chốt tháng.
- Mọi thao tác đặc biệt của BGH phải ghi `Audit_Log`.
- Khi BGH đã chỉnh sửa rồi mở khóa, giáo viên vẫn nhìn thấy:
  - `DiemGV`
  - `DiemBGH`
  - `GhiChuBGH`
- Giáo viên không được sửa dữ liệu của BGH.
- Sau khi chốt tháng:
  - `TrangThai = 5`
  - `KhoaGV = TRUE`
  - `KhoaBGH = TRUE`
  - tất cả chỉ xem.

### Form chấm điểm

- Form chấm điểm được sinh động từ `DM_TieuChi`.
- Hiển thị theo thứ tự:
  ```text
  GROUP
      SECTION
          ITEM
  ```
- Chỉ dòng `ITEM` có ô nhập liệu.
- Giáo viên được sửa `DiemGV` và `GhiChuGV` khi phiếu chưa khóa.
- BGH được sửa `DiemBGH` và `GhiChuBGH` theo phân quyền.
- Form tính tổng điểm tức thời từ dữ liệu đang có.
- Khi lưu, dữ liệu được ghi xuống Google Sheets theo quy tắc đã chốt.

### Xem lại phiếu và xuất PDF

- Giáo viên được xem lại phiếu đã nộp, nhưng không được chỉnh sửa.
- BGH được xem tất cả phiếu theo phân quyền.
- PDF được sinh từ dữ liệu:
  - `TH_ThiDua`
  - `CT_ThiDua`
  - `DM_GiaoVien`
  - `DM_TieuChi`
- PDF không sinh từ giao diện web.
- Tên file PDF:
  ```text
  ThiDua_<Thang>_<MaGV>.pdf
  ```
- PDF hiển thị mã đối chiếu gồm:
  - `IDPhieu`
  - `LanNop`
  - `NgayNop`

## 2026-07-04 - M02: Rà soát lỗi lưu điểm và rollback giao diện

- Ghi nhận quá trình tối ưu Form chấm điểm M02 phát sinh lỗi do refactor quá rộng.
- Các bản `v15`, `v16`, `v17`, `v18` không dùng tiếp vì làm sai hoặc làm mất ổn định một phần luồng nhập liệu:
  - có bản chỉ lưu tổng điểm nhưng không lưu điểm thành phần;
  - có bản cộng sai tổng do lẫn dữ liệu hiển thị hoặc dòng tổng nhóm;
  - có bản làm mất control nhập điểm ở cột `Tự chấm`;
  - có bản nhận diện sai cột `CT_ThiDua`.
- Thống nhất rollback giao diện về bản `EVUS_ThiDua_M02_Save_Fix_2026-07-04_v14.zip`, vì đây là bản còn giữ được giao diện nhập điểm cũ.
- Thống nhất nguyên tắc xử lý tiếp theo:
  - không refactor rộng khi chưa kiểm soát đủ luồng dữ liệu;
  - không chuyển control nhập điểm sang HTML tĩnh;
  - chỉ sửa đúng nơi gây lỗi;
  - ưu tiên sửa luồng lưu điểm thành phần trước, chưa tiếp tục sửa sticky header, màu nút hoặc tổng nhóm nếu chưa ổn định lưu dữ liệu.

## 2026-07-04 - M02: Bản sửa mục tiêu v19

- Tạo bản `EVUS_ThiDua_M02_Save_Targeted_Fix_2026-07-04_v19.zip` trên nền giao diện `v14`.
- Phạm vi v19:
  - giữ nguyên giao diện nhập điểm của `v14`;
  - chỉ sửa luồng lưu điểm thành phần `CT_ThiDua`;
  - bổ sung bẫy lỗi khi thiếu cột bắt buộc trong `CT_ThiDua`;
  - bổ sung bẫy lỗi khi không tìm thấy dòng chi tiết theo `ID`;
  - bắt lỗi khi lưu tại trang giáo viên để hiển thị thông báo rõ ràng thay vì làm app hỏng im lặng.
- Các file bị ảnh hưởng trong v19:
  - `app/services/thi_dua_service.py`;
  - `app/pages/teacher_score_page.py`;
  - `app/components/score_form_component.py` giữ nguyên theo v14.
- Trạng thái: chờ kiểm thử local từ người dùng theo kịch bản:
  1. Đổi một số điểm thành phần.
  2. Bấm `Lưu`.
  3. Đăng xuất.
  4. Đăng nhập lại.
  5. Kiểm tra điểm thành phần còn giữ đúng trong Form và trong Google Sheets.
- Chưa commit GitHub cho đến khi kiểm thử PASS.
## 2026-07-04 - M02: Hoàn thành sửa luồng lưu và đọc lại CT_ThiDua (v14.7)

- Hoàn thành sửa lỗi lưu điểm thành phần `CT_ThiDua.DiemGV`.
- Hoàn thành sửa lỗi đọc lại điểm giáo viên sau khi đăng xuất/đăng nhập.
- Hoàn thành sửa lỗi nhận diện các cột legacy của `CT_ThiDua`:
  - `Điểm gợi ý`
  - `Điểm GV chấm`
  - `Điểm BGH chỉnh`
- Chuyển luồng ghi từ nhiều `update_cell()` sang `batch_update()` để giảm số request Google Sheets.
- Bổ sung quy tắc: mở phiếu không được tự đồng bộ hoặc ghi lại `CT_ThiDua`; chỉ đọc dữ liệu hiện có.
- Bổ sung chống sinh trùng dòng chi tiết `CT_ThiDua` cho cùng `IDPhieu` và `MaTC`.
- Kiểm thử PASS:
  - sửa 1 tiêu chí → Lưu → đăng xuất → đăng nhập;
  - sửa nhiều tiêu chí cùng lúc;
  - sửa rồi trả về điểm mặc định.
- Xác nhận điểm thành phần được giữ đúng trong Google Sheets và hiển thị đúng khi mở lại phiếu.
- Bản bàn giao liên quan:
  - `EVUS_ThiDua_M02_v14_7_fix_read_saved_score.zip`.

## 2026-07-05 - M02: Hoàn thiện hiệu năng và luồng nộp phiếu

### Tối ưu hiệu năng

- Hoàn thành tối ưu Google Sheets.
- Cache:
  - `gspread.Client`
  - Spreadsheet
  - Worksheet
  - `read_sheet_records()`
- Thời gian mở phiếu:
  - trước tối ưu: khoảng 34.71 giây
  - sau tối ưu vòng 1: khoảng 4.80 giây
  - sau tối ưu vòng 2: khoảng 0.21 giây
- Kiểm thử PASS:
  - lưu điểm;
  - đăng xuất;
  - đăng nhập;
  - đọc lại dữ liệu;
  - không đọc dữ liệu cũ sau khi dùng cache.

### Hoàn thiện luồng nộp phiếu

- Giáo viên được cảnh báo khi còn tiêu chí thiếu giải trình.
- Cảnh báo sử dụng mã hiển thị, ví dụ `2.1b`, thay cho mã nội bộ `TCxxx`.
- Sau cảnh báo, giáo viên bấm `Đồng ý nộp` lần thứ hai thì vẫn cho phép nộp.
- Sau khi nộp:
  - `TrangThai = 3`;
  - `KhoaGV = TRUE`;
  - chế độ hiển thị là `Chỉ xem`;
  - giáo viên không chỉnh sửa được nữa.
- Đăng xuất và đăng nhập lại vẫn giữ đúng trạng thái đã nộp.
- Kiểm thử PASS.

### Chuẩn hóa đọc `TH_ThiDua`

- Chuẩn hóa header tiếng Việt và header chuẩn khi đọc `TH_ThiDua`.
- Bổ sung alias cho các trường nghiệp vụ quan trọng:
  - `Trạng thái phiếu` → `TrangThai`;
  - `Khóa GV` → `KhoaGV`;
  - `Ngày nộp` → `NgayNop`;
  - `Tổng điểm` → `TongDiem`;
  - `Người cập nhật` → `NguoiCapNhatCuoi`;
  - `Thời gian cập nhật` → `NgayCapNhat`.
- Giảm phụ thuộc vào tên cột cụ thể của Google Sheets.

### Quy tắc phát triển mới: Trace-first

- Khi chưa xác định được nguyên nhân lỗi:
  - không sửa nghiệp vụ ngay;
  - không sửa nhiều nơi cùng lúc;
  - bắt buộc thêm trace hoặc checkpoint theo đúng luồng xử lý.
- Quy trình chuẩn:

  ```text
  Trace
  → Xác định checkpoint lỗi
  → Sửa đúng một nguyên nhân
  → Bỏ trace
  → Kiểm thử
  → Bàn giao
  ```

- Quy tắc này áp dụng cho các lỗi nghiệp vụ, dữ liệu và luồng Google Sheets trong các hạng mục tiếp theo.

## 2026-07-06 - M03: Hoàn thành nền BGH xem và chỉnh điểm bằng form dùng chung

### M03.1 - BGH xem phiếu theo tháng

- Hoàn thành điều hướng theo vai trò:
  - `Vai trò = Giáo viên` vào màn hình giáo viên.
  - `Vai trò = BGH` vào màn hình Ban Giám hiệu.
- Tạo tài khoản kiểm thử BGH trong `DM_GiaoVien`.
- Hoàn thành màn hình BGH xem danh sách phiếu theo tháng.
- Danh sách phiếu đọc từ `TH_ThiDua`, ghép thông tin giáo viên từ `DM_GiaoVien`.
- Bổ sung chống hiển thị trùng phiếu theo `TH_ThiDua.ID` vì dữ liệu test có nhiều dòng cùng ID.
- BGH mở được phiếu giáo viên ở chế độ xem/chỉnh.
- Kiểm thử PASS:
  - đăng nhập được cả giáo viên và BGH;
  - BGH xem danh sách phiếu;
  - BGH mở được phiếu;
  - tổng điểm hiển thị đúng.

### M03.2 - BGH chỉnh điểm thi đua

- Bổ sung luồng BGH nhập:
  - `DiemBGH`;
  - `GhiChuBGH`.
- Bổ sung lưu điểm BGH xuống `CT_ThiDua`.
- Sau khi BGH lưu, cập nhật `TH_ThiDua`:
  - `TongDiem` theo điểm chính thức;
  - `TrangThai = 4` nếu BGH đã chỉnh sửa.
- Kiểm thử PASS:
  - nhập điểm BGH;
  - nhập ghi chú BGH;
  - lưu được xuống Google Sheets;
  - đăng xuất/đăng nhập lại vẫn đọc đúng dữ liệu đã lưu.

### Sự cố nhập ghi chú BGH và quyết định kiến trúc

- Phát sinh lỗi khi BGH nhập `GhiChuBGH` trong form tự dựng riêng ở `bgh_score_page.py`:
  - gõ chữ thường không ổn định;
  - gõ phím `c` làm xuất hiện hộp thoại Clear caches của Streamlit;
  - các bản vá bằng JavaScript và đổi layout không ổn định.
- Đã áp dụng quy tắc Trace-first:
  - kiểm tra ô nhập ngoài bảng;
  - kiểm tra ô nhập trong layout bảng;
  - xác định lỗi nằm ở cách tự dựng form BGH riêng, không nằm ở Google Sheets hay service lưu.
- Quyết định kiến trúc:
  - không tiếp tục duy trì form BGH tự dựng riêng;
  - mở rộng `app/components/score_form_component.py` thành component form thi đua dùng chung;
  - giáo viên và BGH cùng dùng một component, chỉ khác `mode` và quyền nhập.
- Bổ sung `mode` cho form:
  - `mode="teacher"`: giáo viên nhập `DiemGV`, `GhiChuGV`.
  - `mode="bgh"`: BGH xem `DiemGV`, `GhiChuGV`; nhập `DiemBGH`, `GhiChuBGH`.
- `bgh_score_page.py` chỉ còn nhiệm vụ:
  - kiểm tra quyền BGH;
  - chọn tháng;
  - chọn phiếu;
  - gọi form dùng chung;
  - gọi service lưu điểm BGH khi bấm lưu.
- Điều chỉnh thứ tự cột BGH đã chốt:

  ```text
  Điểm GV | Ghi chú GV | Điểm BGH | Ghi chú BGH
  ```

- Kiểm thử PASS sau khi dùng form chung:
  - BGH nhập được `abc` và chữ `c` trong ghi chú;
  - hết lỗi Clear caches;
  - lưu điểm và ghi chú BGH đúng;
  - đăng xuất/đăng nhập lại đọc đúng;
  - giao diện BGH thống nhất với phiếu giáo viên.

### Trạng thái sau M03.2C

- Hoàn thành:
  - Màn hình BGH.
  - BGH xem phiếu theo tháng.
  - BGH chỉnh sửa điểm thi đua.
- Chưa chốt hoàn thành:
  - kiểm thử riêng `Audit_Log` khi BGH chỉnh sửa;
  - chốt tháng;
  - tổng hợp tháng;
  - xuất Excel toàn trường theo tháng.
- Bản bàn giao liên quan:
  - `EVUS_ThiDua_M03_2C_shared_score_form.zip`;
  - `EVUS_ThiDua_M03_2C_bgh_column_order.zip`.

## 2026-07-06 - M03: Hoàn thành quy trình xử lý tháng

### M03.3 - Chốt tháng

- Hoàn thành chức năng Chốt tháng cho Ban Giám hiệu.
- Chỉ BGH được quyền chốt.
- Chốt theo từng tháng.
- Chỉ các phiếu có `TrangThai = 3` hoặc `TrangThai = 4` được chuyển sang `TrangThai = 5`.
- Phiếu chưa nộp hoặc chưa có phiếu không bị ép chốt.
- Trước khi chốt, hệ thống cảnh báo danh sách giáo viên chưa nộp hoặc chưa có phiếu.
- Sau khi chốt:
  - `KhoaGV = TRUE`;
  - `KhoaBGH = TRUE`;
  - giáo viên và BGH chỉ được xem.
- Ghi `Audit_Log` với hành động:
  - `BGH_FINALIZE_PHIEU`.
- Kiểm thử PASS:
  - phiếu đã nộp chuyển đúng trạng thái 5;
  - khóa GV và khóa BGH đúng;
  - giáo viên chưa nộp không bị ép chốt;
  - `Audit_Log` có dòng chốt tháng.

### M03.4 - Tổng hợp tháng

- Hoàn thành chức năng tổng hợp tháng.
- Nguồn dữ liệu:
  - `TH_ThiDua`;
  - `DM_GiaoVien`.
- Chỉ tổng hợp các phiếu đã chốt (`TrangThai = 5`).
- Kết quả ghi vào worksheet:
  - `TongHop_ThiDua`.
- Nếu chưa có worksheet `TongHop_ThiDua`, hệ thống tự tạo và ghi header chuẩn.
- Một giáo viên trong một tháng chỉ có một dòng tổng hợp.
- Chạy lại chỉ cập nhật dòng cũ, không tạo dòng trùng.
- Chuẩn hóa khóa:
  - `TongHop_ThiDua.ID = NamHoc_Thang_MaGV`.
- Sửa lỗi phát sinh trong quá trình kiểm thử:
  - `TongHop_ThiDua.ID` từng bị ghi sai thành `S`;
  - `TH_ThiDua.ID` từng bị hiển thị sai thành `S`;
  - bổ sung cơ chế kiểm tra và phục hồi `TH_ThiDua.ID` khi đủ dữ liệu hợp lệ và không trùng khóa.
- Ghi `Audit_Log` với hành động:
  - `BGH_SUMMARIZE_MONTH`.
- Kiểm thử PASS:
  - tạo được `TongHop_ThiDua`;
  - tổng hợp đúng phiếu đã chốt;
  - chạy lại không tạo dòng trùng;
  - ID tổng hợp đúng dạng `2025-2026_062026_GV001`;
  - `Audit_Log` có dòng tổng hợp tháng.

### M03.5 - Xuất Excel tháng

- Hoàn thành chức năng xuất Excel toàn trường theo tháng.
- Dữ liệu lấy trực tiếp từ `TongHop_ThiDua`.
- Không đọc lại `CT_ThiDua`.
- Không ghi thêm dữ liệu vào Google Sheets.
- Không tạo dòng trùng.
- Tên file xuất:
  ```text
  TongHop_ThiDua_Thang_MM_YYYY.xlsx
  ```
- Nội dung Excel gồm các cột:
  - `STT`;
  - `Mã GV`;
  - `Họ tên`;
  - `Tổ chuyên môn`;
  - `Tổng điểm`;
  - `Xếp loại`;
  - `Ghi chú`.
- Thống nhất giao diện:
  - nút Xuất Excel dùng màu đỏ như các thao tác nghiệp vụ chính;
  - sau khi xử lý xong nút trở về trạng thái ban đầu.
- Kiểm thử PASS:
  - xuất đúng file Excel;
  - dữ liệu lấy từ `TongHop_ThiDua`;
  - không đọc lại `CT_ThiDua`;
  - không ghi thêm Google Sheets;
  - không tạo dòng trùng.

### Trạng thái hoàn thành M03

- Hoàn thành toàn bộ M03:
  - M03.1: BGH xem phiếu theo tháng;
  - M03.2: BGH chỉnh điểm thi đua;
  - M03.3: Chốt tháng;
  - M03.4: Tổng hợp tháng;
  - M03.5: Xuất Excel toàn trường theo tháng.
- Luồng tháng đã kiểm thử PASS:

  ```text
  Giáo viên chấm
      ↓
  Nộp phiếu
      ↓
  BGH chỉnh điểm
      ↓
  Chốt tháng
      ↓
  Tổng hợp tháng
      ↓
  Xuất Excel tháng
  ```

- Bản bàn giao liên quan:
  - `EVUS_ThiDua_M03_3_Finalize_Month_v2.zip`;
  - `EVUS_ThiDua_M03_4_Summarize_Month_v5_fix_summary_id.zip`;
  - `EVUS_ThiDua_M03_4_v6_repair_TH_ID.zip`;
  - `EVUS_ThiDua_M03_5_Export_Excel_Month_v2_button_color.zip`.

## 2026-07-06 - Pilot v1.0-beta: Chuẩn bị triển khai thực tế

### Quyết định vận hành

- Thống nhất tạm dừng phát triển M04.
- Triển khai hệ thống cho giáo viên và Ban Giám hiệu sử dụng thực tế ít nhất 02 tháng.
- Trong giai đoạn Pilot chỉ xử lý:
  - lỗi phát sinh;
  - tối ưu hiệu năng;
  - cải thiện giao diện;
  - hoàn thiện thông báo và bẫy lỗi.
- Chưa phát triển thêm chức năng mới ngoài phạm vi vận hành thực tế.

### Chuẩn hóa đăng nhập

- Thống nhất tài khoản đăng nhập chung theo vai trò:
  - Giáo viên: `GV`.
  - Ban Giám hiệu: `BGH`.
- Giáo viên đăng nhập bằng:
  - Tài khoản: `GV`;
  - Mật khẩu ban đầu: `Mã GV`.
- Ban Giám hiệu đăng nhập bằng:
  - Tài khoản: `BGH`;
  - Mật khẩu ban đầu: `BGH123abc456`.
- Màn hình đăng nhập đổi từ ô nhập tự do sang chọn vai trò:
  - `Giáo viên`;
  - `Ban Giám hiệu`.
- Tài khoản hiển thị cố định theo lựa chọn, giúp giảm lỗi gõ sai `GV` hoặc `BGH`.

### Quản trị hệ thống cho BGH

- Bổ sung khu vực `Quản trị hệ thống` ở góc trên bên phải màn hình BGH.
- Bổ sung cấu hình thời hạn tự chấm:
  - mặc định hết ngày 05 hằng tháng;
  - BGH có thể điều chỉnh ngày cuối tự chấm;
  - cấu hình lưu trong `System_Config`.
- Bổ sung chức năng `Khởi tạo mật khẩu cho tài khoản mới`:
  - chỉ xử lý các tài khoản chưa có `MatKhauHash`;
  - không ghi đè mật khẩu đã có;
  - GV mới có mật khẩu ban đầu là `Mã GV`;
  - BGH có mật khẩu ban đầu là `BGH123abc456`;
  - ghi `Audit_Log` khi thực hiện.
- Loại bỏ nút `Đặt lại mật khẩu ban đầu` vì có nguy cơ reset toàn bộ mật khẩu ngoài ý muốn.

### Tài liệu và phát hành

- Tạo tài liệu hướng dẫn sử dụng nhanh cho giáo viên và Ban Giám hiệu.
- Thống nhất đóng gói/lưu trữ bản dự án v1.0-beta trước khi trường dùng thật.
- Thống nhất tạo mốc phát hành trên GitHub để trường tải và triển khai.

### Kiểm thử PASS

- BGH đăng nhập bằng tài khoản `BGH`.
- Giáo viên đăng nhập bằng tài khoản `GV` và mật khẩu là `Mã GV`.
- BGH lưu được ngày cuối tự chấm.
- Giáo viên có thể tự chấm khi thời hạn được BGH mở rộng.
- Chức năng khởi tạo mật khẩu cho tài khoản mới chỉ băm tài khoản chưa có hash.
- Giao diện `Quản trị hệ thống` được bố trí lại và tiêu đề màu đỏ.

### Trạng thái

- Hệ thống đủ điều kiện triển khai Pilot v1.0-beta cho trường sử dụng thực tế.
- Sau giai đoạn Pilot mới tổng hợp góp ý và quyết định các hạng mục tiếp theo trước khi phát triển M04.

## 2026-07-06 - Chuẩn hóa quy trình sửa lỗi theo bản đồ phụ thuộc mã nguồn

- Hoàn thành rà soát toàn bộ các file Python của dự án.
- Tạo và đưa vào dự án hai tài liệu nền:
  - `docs/03_Design/PY_RELATION_MAP.md`
  - `docs/03_Design/evus_py_dependency_map.json`
- Thống nhất sử dụng hai tài liệu này làm cơ sở xác định phạm vi ảnh hưởng trước khi sửa mã nguồn.
- Từ thời điểm này:
  - không sửa theo từng lỗi riêng lẻ khi chưa xác định quan hệ phụ thuộc;
  - phải xác định các hàm, màn hình, service và bảng Google Sheets liên quan;
  - phải kiểm thử hồi quy theo đúng phạm vi ảnh hưởng trước khi commit.
- Nếu một hàm được cả Giáo viên và Ban Giám hiệu dùng chung, bắt buộc kiểm thử cả hai vai trò trước khi commit.
- Mục tiêu:
  - giảm lỗi phát sinh chéo;
  - tăng khả năng bảo trì;
  - ổn định giai đoạn Pilot.

## 2026-07-07 - Pilot hardening: Tối ưu hiệu năng luồng Giáo viên

### Bối cảnh

- Giáo viên mở phiếu còn chậm hơn Ban Giám hiệu, trong khi các chức năng nghiệp vụ đã PASS.
- Thống nhất không phát triển chức năng mới, không chỉnh giao diện, không refactor rộng.
- Mục tiêu duy nhất: xác định nguyên nhân chậm của luồng Giáo viên và tối ưu an toàn, không ảnh hưởng các chức năng đã ổn định.

### Quy trình điều tra

- Đối chiếu `app/pages/bgh_score_page.py` với `app/pages/teacher_score_page.py`.
- Thiết lập đo nhiều tầng:
  - đo Google Sheets cấp cao;
  - đo sâu `thi_dua_service.get_phieu()`;
  - đo sâu `thi_dua_service.get_chi_tiet_phieu()`;
  - đo vòng chạy `render_teacher_score_page()` của Streamlit;
  - đo cấp thấp trong `google_sheets_service.py`.
- Xuất log TXT để kiểm tra đầy đủ thay vì chỉ xem một phần trên giao diện.

### Kết quả loại trừ

Đã loại trừ các nguyên nhân sau:

- `teacher_score_page.py` không tạo vòng lặp `st.rerun()` bất thường.
- `score_form_component.render_score_form()` chỉ mất khoảng 0.25-0.32 giây.
- `thi_dua_service.get_phieu()` xử lý nội bộ rất nhanh; thời gian chủ yếu nằm ở đọc dữ liệu.
- `thi_dua_service.get_chi_tiet_phieu()` xử lý lọc và khử trùng dữ liệu rất nhanh.
- Dữ liệu hiện tại nhỏ:
  - `TH_ThiDua`: khoảng 10-12 dòng;
  - `CT_ThiDua`: khoảng 207-231 dòng;
  - `DM_TieuChi`: khoảng 31-32 dòng.
- Không có bằng chứng cho thấy lỗi nằm ở nghiệp vụ M02/M03.

### Nguyên nhân xác định

- Thời gian chậm chủ yếu nằm ở lớp giao tiếp Google Sheets:
  - `client.open_by_key()` khi mở Spreadsheet lần đầu;
  - truy xuất worksheet lần đầu bằng API Google Sheets;
  - các lệnh `worksheet.get_all_values()` hoặc `worksheet.get()` khi chưa có cache dữ liệu dòng.
- Cache `read_sheet_records()` hoạt động đúng sau khi dữ liệu đã được đọc.
- Cache Spreadsheet và Worksheet hoạt động đúng, nhưng trước tối ưu mỗi worksheet vẫn có thể phát sinh lệnh API riêng.

### Bản tối ưu đã thực hiện

- Bổ sung Worksheet Catalog Cache trong `google_sheets_service.py`:
  - tải danh sách worksheet một lần bằng `spreadsheet.worksheets()`;
  - cache worksheet handle theo tên sheet;
  - tránh gọi `spreadsheet.worksheet()` riêng lẻ cho từng sheet.
- Bổ sung warm-up Google Sheets sau đăng nhập:
  - thực hiện sau khi `authenticate()` thành công;
  - làm nóng client/spreadsheet/worksheet catalog trước khi chuyển sang trang làm việc.
- Gỡ các bộ đo tạm sau khi chốt kết quả điều tra.
- Giữ lại phần tối ưu cache an toàn.

### Kết quả sau tối ưu

- `spreadsheet.worksheet()` không còn gọi riêng lẻ nhiều lần cho từng sheet trong luồng mở phiếu.
- Các sheet sau khi nạp catalog chuyển sang `get_worksheet cache hit`.
- Thời gian còn lại chủ yếu là giới hạn của Google Sheets API khi đọc dữ liệu lần đầu.
- Tốc độ hiện tại được thống nhất là chấp nhận được cho giai đoạn Pilot.

### Quyết định

- Dừng tối ưu hiệu năng tại đây để tránh rủi ro ảnh hưởng các chức năng đã PASS.
- Không tiếp tục sửa `teacher_score_page.py`, `thi_dua_service.py` hoặc `google_sheets_service.py` nếu không có bằng chứng mới.
- Trong giai đoạn Pilot, chỉ điều tra lại hiệu năng nếu:
  - dữ liệu tăng mạnh;
  - người dùng phản ánh chậm bất thường;
  - log cho thấy cache không hoạt động;
  - thay đổi kiến trúc dữ liệu hoặc cách đọc Google Sheets.

### File liên quan

- `app/services/google_sheets_service.py`
- `app/auth/login_page.py`
- `app/pages/teacher_score_page.py`
- `app/pages/bgh_score_page.py`
- `app/services/thi_dua_service.py`

### Bản bàn giao liên quan

- `EVUS_ThiDua_ServiceTrace_GetPhieu_CT_Perf_2026-07-07.zip`
- `EVUS_ThiDua_ServiceTrace_TXT_GetPhieu_CT_2026-07-07.zip`
- `EVUS_ThiDua_StreamlitRerunTrace_2026-07-07.zip`
- `EVUS_ThiDua_GoogleSheetsLowLevelTrace_2026-07-07.zip`
- `EVUS_ThiDua_WorksheetCatalogCache_2026-07-07.zip`
- `EVUS_ThiDua_LoginGoogleSheetsWarmup_2026-07-07.zip`
- `EVUS_ThiDua_CleanAfterPerformanceOptimization_2026-07-07.zip`
## 2026-07-07 - Pilot v1.0-beta: Hoàn thiện giao diện Giáo viên

- Hoàn thiện giao diện M02 theo hướng ưu tiên trải nghiệm người dùng.
- Thu gọn Header ứng dụng.
- Thu gọn thông tin phiếu thành một khối tóm tắt.
- Tách khu vực thao tác khỏi bảng điểm.
- Bổ sung khu vực xác nhận nộp phiếu độc lập.
- Bổ sung danh sách tiêu chí còn thiếu giải trình ngay trong khu vực thao tác.
- Hoàn thiện kiểm tra thiếu giải trình dựa trên dữ liệu hiện hành của form.
- Giữ nguyên toàn bộ nghiệp vụ M02; chỉ thay đổi giao diện.
- Khối thao tác và cảnh báo hoạt động ổn định.
- Giao diện Giáo viên được xem là hoàn thành cho Pilot, chuyển sang kiểm thử hồi quy Ban Giám hiệu.

## 2026-07-07 - Hoàn thiện giao diện Ban Giám hiệu và kiểm thử hồi quy

- Hoàn thiện giao diện Ban Giám hiệu cho Pilot (chạy thử nghiệm), theo hướng gọn và tối ưu diện tích màn hình.
- Thu gọn khối thông tin người dùng BGH ở Header.
- Bố trí lại khối điều khiển BGH thành 2 bảng:
  - Bảng thiết lập chung gồm `Thông tin chấm điểm thi đua` và `Quản trị hệ thống`.
  - Bảng thao tác xử lý tháng gồm `Chọn phiếu xử lý`, `Chốt tháng`, `Tổng hợp tháng`, `Xuất Excel tháng`.
- Bỏ bảng `Danh sách phiếu tháng` khỏi luồng chính để giảm chiều cao giao diện.
- Thu gọn khu vực `Chi tiết phiếu`.
- Giữ nguyên dòng tiêu đề 7 cột của bảng chi tiết phiếu BGH.
- Bọc riêng phần tiêu chí BGH vào vùng cuộn, chỉ phần tiêu chí cuộn, không tạo thêm dòng tiêu đề mới.
- Không thay đổi nghiệp vụ, Google Sheets, service lưu điểm, chốt tháng, tổng hợp tháng hoặc xuất Excel hiện hành.
- Kiểm thử hồi quy Ban Giám hiệu: PASS.
  - Mở phiếu: PASS.
  - Sửa điểm BGH: PASS.
  - Lưu và đọc lại: PASS.
  - Chốt tháng: PASS.
  - Tổng hợp tháng: PASS.
  - Xuất Excel: PASS.
- Kiểm thử hồi quy Giáo viên sau khi chạm `score_form_component.py`: PASS.
  - Mở phiếu: PASS.
  - Nhập điểm: PASS.
  - Lưu: PASS.
  - Đọc lại: PASS.
  - Nộp phiếu: PASS.
  - Phiếu đã nộp chỉ xem: PASS.
- Quyết định: không tiếp tục sửa giao diện GV/BGH nếu không phát hiện lỗi mới.

## 2026-07-07 - Chốt định hướng mẫu Excel tháng mới

- Thống nhất cần bổ sung mẫu Excel tháng mới sau khi hoàn tất kiểm thử hồi quy giao diện.
- Sheet `TongHop_Thang` sẽ mở rộng theo từng tiêu chí, gồm các cột thông tin giáo viên, tổng điểm và các cột tiêu chí như `1.1`, `1.2`, `1.3`, ...
- Mỗi giáo viên sẽ có một sheet riêng trong file Excel tháng để xem phiếu chi tiết.
- Quy tắc điểm ở các cột tiêu chí của sheet tổng hợp:
  - Nếu có `DiemBGH` thì dùng `DiemBGH`.
  - Nếu không có `DiemBGH` thì dùng `DiemGV`.
- Đây là điểm chính thức sau khi BGH duyệt, dùng cho báo cáo tháng.
- Phạm vi triển khai dự kiến: chỉ sửa phần xuất Excel, không thay đổi Google Sheets và không thay đổi nghiệp vụ chấm điểm.

