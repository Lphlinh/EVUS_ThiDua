# PROJECT_STRUCTURE

> Tài liệu mô tả trạng thái hiện hành của dự án EVUS_ThiDua.
>
> `PROJECT_STRUCTURE` không ghi lịch sử thay đổi và không thay thế `PROJECT_LOG`.

---

## 1. Project Root

```text
G:\My Drive\AI\AI_giao_duc\Au-Viet-My\EVUS_ThiDua
```

---

## 2. Tài liệu nền tảng bắt buộc

Khi bắt đầu phiên làm việc, AI phải đọc theo thứ tự:

```text
docs/01_Project/00_BOOT_CONTEXT.md
docs/01_Project/01_PROJECT_RULES.md
docs/01_Project/04_PROJECT_STRUCTURE.md
docs/01_Project/02_PROJECT_LOG.md
docs/01_Project/03_TODO.md
```

Vai trò:

- `00_BOOT_CONTEXT.md`: bối cảnh khởi động.
- `01_PROJECT_RULES.md`: quy tắc làm việc.
- `04_PROJECT_STRUCTURE.md`: cấu trúc và quy ước hiện hành.
- `02_PROJECT_LOG.md`: lịch sử quyết định.
- `03_TODO.md`: kế hoạch công việc.

---

## 3. Cấu trúc thư mục chuẩn

```text
EVUS_ThiDua/
├── app/
├── assets/
├── backup/
├── config/
├── data/
├── docs/
├── logs/
├── tests/
├── .streamlit/
├── app.py
├── README.md
├── requirements.txt
├── run_local.bat
├── backup_project.bat
└── .gitignore
```

Không xem `.git/`, `.venv/`, `__pycache__/` là một phần của cấu trúc nghiệp vụ.

---

## 4. Cấu trúc app

```text
app/
├── auth/
├── components/
├── models/
├── pages/
├── services/
└── utils/
```

Quy ước:

- `auth/`: đăng nhập, xác thực, phân quyền.
- `components/`: thành phần giao diện dùng chung.
- `models/`: mô hình dữ liệu.
- `pages/`: màn hình Streamlit.
- `services/`: xử lý nghiệp vụ, Google Sheets, PDF, Excel.
- `utils/`: hàm tiện ích không chứa nghiệp vụ chính.

Không đặt file nghiệp vụ trực tiếp trong `app/` nếu chưa thống nhất.

---

## 5. Cấu trúc docs

```text
docs/
├── 01_Project/
├── 02_Meeting/
├── 03_Design/
├── 04_API/
├── 05_Test/
└── 06_Release/
```

### 5.1. `docs/01_Project/`

Tài liệu quản lý dự án:

```text
00_BOOT_CONTEXT.md
01_PROJECT_RULES.md
02_PROJECT_LOG.md
03_TODO.md
04_PROJECT_STRUCTURE.md
99_ProjectTree/project_tree.txt
```

### 5.2. `docs/02_Meeting/`

Biên bản họp, ghi chú trao đổi chính thức.

### 5.3. `docs/03_Design/`

Tài liệu thiết kế và biểu mẫu nghiệp vụ chuẩn:

- mẫu phiếu thi đua tháng;
- mẫu tổng hợp thi đua năm;
- thiết kế dữ liệu;
- thiết kế giao diện;
- ghi chú nghiệp vụ đã chuẩn hóa.

### 5.4. `docs/04_API/`

Tài liệu API, endpoint, tích hợp ngoài nếu có.

### 5.5. `docs/05_Test/`

Tài liệu kiểm thử, test cases, checklist kiểm thử.

### 5.6. `docs/06_Release/`

Release notes, ghi chú phát hành.

---

## 6. Cập nhật cây thư mục

Nguồn chuẩn phản ánh cây thư mục thực tế:

```text
docs/01_Project/99_ProjectTree/project_tree.txt
```

Cập nhật bằng lệnh PowerShell từ thư mục gốc dự án:

```powershell
tree /F /A > docs\01_Project\99_ProjectTree\project_tree.txt
```

Sau khi cập nhật cây thư mục, nếu có thay đổi cấu trúc chính thức thì cập nhật `PROJECT_STRUCTURE`.

---

## 7. Cấu trúc backup

`backup/` chỉ dùng lưu trữ, không phải tài liệu chính thức.

Dùng cho:

- ZIP bàn giao;
- bản sao lưu;
- file trung gian;
- import/export tạm;
- backup trước refactor.

Không dùng `backup/` làm nguồn chuẩn nghiệp vụ nếu tài liệu đó cần được dự án tham chiếu thường xuyên.

---

## 8. Cấu trúc Google Sheets

Google Sheets chính:

```text
EVUS_ThiDua_Data
```

Worksheet chuẩn:

```text
DM_GiaoVien
DM_TieuChi
TH_ThiDua
CT_ThiDua
TongHop_ThiDua
Audit_Log
System_Config
```

Google Sheets là nguồn dữ liệu chính.

---

## 9. Quan hệ dữ liệu

```text
DM_GiaoVien
    ↓
TH_ThiDua
    ↓
CT_ThiDua
    ↓
TongHop_ThiDua
```

`Audit_Log` ghi nhật ký thao tác quan trọng.

`System_Config` lưu cấu hình hệ thống.

---

## 10. Quy ước đặt tên bảng

```text
DM_*  : danh mục
TH_*  : header / tổng hợp phiếu
CT_*  : chi tiết
```

---

## 11. Khóa chính và ID

- `DM_GiaoVien`: `MaGV`
- `DM_TieuChi`: `MaTC`
- `TH_ThiDua.ID`: `NamHoc_Thang_MaGV`
- `CT_ThiDua.ID`: `IDPhieu_MaTC`
- `Audit_Log.ID`: UUID hoặc timestamp do chương trình sinh

---

## 12. Quy ước nghiệp vụ hiện hành

- Mỗi giáo viên có tối đa 01 phiếu thi đua cho mỗi tháng.
- Tháng chấm mặc định là tháng trước so với ngày hiện tại.
- Giao diện không cần hiển thị riêng "Năm học" nếu `MM/YYYY` đã đủ rõ.
- Không lưu họ tên, tổ, email, chức vụ trong bảng nghiệp vụ; chỉ lưu `MaGV`.
- Thông tin hiển thị của giáo viên lấy từ `DM_GiaoVien`.
- `DM_TieuChi` là nguồn sinh `CT_ThiDua`.
- `TH_ThiDua` chỉ lưu thông tin Header, trạng thái, tổng điểm, khóa.
- Giáo viên chấm điểm trên `CT_ThiDua`.
- Sau khi giáo viên hoàn thành, phiếu bị khóa phía giáo viên.
- BGH có quyền xem và chỉnh sửa điểm theo quy tắc phân quyền.
- Thao tác quan trọng phải ghi `Audit_Log`.

---


## 12.1. Cấu trúc TH_ThiDua

`TH_ThiDua` là bảng Header của phiếu thi đua tháng.

Khóa chính:

```text
ID = NamHoc_Thang_MaGV
```

Cột chuẩn:

| Cột | Ý nghĩa |
|---|---|
| ID | Khóa chính của phiếu |
| NamHoc | Năm học |
| Thang | Tháng chấm |
| MaGV | Mã giáo viên, khóa đến `DM_GiaoVien` |
| TrangThai | Trạng thái phiếu, dùng mã số 1-5 |
| TongDiem | Tổng điểm chính thức hiện hành |
| KhoaGV | Khóa quyền chỉnh sửa của giáo viên |
| KhoaBGH | Khóa quyền chỉnh sửa của BGH |
| NgayTao | Thời điểm tạo phiếu |
| NgayCapNhat | Thời điểm cập nhật cuối |
| NgayNop | Thời điểm giáo viên nộp phiếu gần nhất |
| NguoiCapNhatCuoi | Người cập nhật cuối |
| NguoiNop | Giáo viên nộp phiếu |
| GhiChuBGH | Ghi chú cấp phiếu của BGH nếu có |
| LanNop | Số lần giáo viên đã nộp phiếu |
| LanMoKhoa | Số lần BGH đã mở khóa phiếu |

Trạng thái phiếu:

| Mã | Trạng thái |
|---:|---|
| 1 | Chưa tạo |
| 2 | Đang chấm |
| 3 | Đã nộp |
| 4 | BGH đã chỉnh sửa |
| 5 | Đã chốt |

Quy tắc:

- Một giáo viên chỉ có tối đa 01 phiếu trong 01 tháng.
- `TH_ThiDua` không lưu chi tiết điểm từng tiêu chí.
- Khi tạo phiếu, `LanNop = 0`, `LanMoKhoa = 0`.
- Khi giáo viên nộp phiếu thành công, `LanNop = LanNop + 1`.
- Khi BGH mở khóa thành công, `LanMoKhoa = LanMoKhoa + 1`.

## 12.2. Cấu trúc CT_ThiDua

`CT_ThiDua` là bảng Detail của phiếu thi đua tháng.

Khóa chính:

```text
ID = IDPhieu_MaTC
```

Cột chuẩn:

| Cột | Ý nghĩa |
|---|---|
| ID | Khóa chính của dòng chi tiết |
| IDPhieu | Khóa đến `TH_ThiDua.ID` |
| MaTC | Khóa đến `DM_TieuChi.MaTC` |
| DiemMacDinh | Điểm gợi ý lấy từ `DM_TieuChi` |
| DiemGV | Điểm giáo viên tự chấm |
| DiemBGH | Điểm BGH điều chỉnh nếu có |
| GhiChuGV | Giải trình của giáo viên |
| GhiChuBGH | Nhận xét hoặc lý do điều chỉnh của BGH |
| NgayCapNhat | Thời điểm cập nhật cuối của dòng |
| NguoiCapNhat | Người cập nhật cuối của dòng |

Quy tắc:

- Chỉ sinh dòng `CT_ThiDua` cho tiêu chí có `DM_TieuChi.Loai = ITEM`.
- Không sinh dòng chi tiết cho `GROUP` và `SECTION`.
- Khi sinh phiếu, `DiemGV = DiemMacDinh`.
- Giáo viên chỉ được sửa `DiemGV` và `GhiChuGV`.
- BGH chỉ được sửa `DiemBGH` và `GhiChuBGH`.
- Không thêm, xóa hoặc đổi khóa dòng chi tiết khi phiếu đã được tạo.
- Nếu thay đổi tiêu chí trong `DM_TieuChi`, thay đổi chỉ áp dụng cho các phiếu sinh sau thời điểm cập nhật.

## 12.3. Quy tắc điểm chính thức

Điểm chính thức của một dòng chi tiết được xác định như sau:

```text
Nếu DiemBGH có giá trị
    dùng DiemBGH
Ngược lại
    dùng DiemGV
```

Quy tắc bổ sung:

- `DiemBGH` chỉ lưu khi khác `DiemGV`.
- Nếu BGH đồng ý với điểm giáo viên, để `DiemBGH` rỗng.
- Khi `DiemGV != DiemMacDinh`, giáo viên bắt buộc nhập `GhiChuGV`.
- Nếu `DiemGV = DiemMacDinh`, không bắt buộc giải trình.
- Tổng điểm phiếu bằng tổng điểm chính thức của toàn bộ dòng `CT_ThiDua` thuộc phiếu.
- Kết quả tổng được cập nhật vào `TH_ThiDua.TongDiem`.

## 12.4. Luồng nghiệp vụ M02

Luồng giáo viên:

```text
Đăng nhập
    ↓
Kiểm tra phiếu theo tháng
    ↓
Nếu chưa có và còn hạn 01-05
    ↓
Tạo TH_ThiDua
    ↓
Sinh CT_ThiDua từ DM_TieuChi
    ↓
Mở form chấm điểm
    ↓
Lưu nhiều lần nếu cần
    ↓
Xác nhận nộp
    ↓
Khóa phiếu giáo viên
    ↓
BGH xử lý
```

Luồng sau hạn:

- Sau ngày 05, giáo viên chưa có phiếu thì hệ thống không tự tạo phiếu.
- BGH có quyền tạo phiếu sau hạn hoặc mở quyền chấm bổ sung.
- Mọi thao tác sau hạn của BGH phải ghi `Audit_Log`.

Luồng lưu:

- Nút `Lưu` ghi ngay các thay đổi xuống Google Sheets.
- Chỉ ghi các dòng thay đổi trong `CT_ThiDua`.
- Cập nhật `TH_ThiDua.TongDiem`, `NgayCapNhat`, `NguoiCapNhatCuoi`.
- Không ghi `Audit_Log` khi chỉ lưu tạm.

Luồng nộp:

- Khi giáo viên xác nhận nộp, hệ thống lưu lần cuối nếu còn thay đổi.
- Cập nhật trạng thái `Đã nộp`.
- Khóa quyền chỉnh sửa của giáo viên.
- Ghi `Audit_Log`.

Luồng mở khóa:

- Chỉ BGH được mở khóa.
- Khi mở khóa, giáo viên vẫn nhìn thấy `DiemBGH` và `GhiChuBGH` nếu trước đó BGH đã chỉnh sửa.
- Giáo viên chỉ được sửa phần dữ liệu của giáo viên.
- Mọi thao tác mở khóa phải ghi `Audit_Log`.

## 12.5. Quy tắc xem lại phiếu và xuất PDF

- Giáo viên được xem lại phiếu đã nộp, không được chỉnh sửa.
- BGH được xem phiếu theo phân quyền.
- PDF được sinh từ dữ liệu gốc, không sinh từ giao diện web.
- Nguồn sinh PDF:
  - `TH_ThiDua`
  - `CT_ThiDua`
  - `DM_GiaoVien`
  - `DM_TieuChi`
- Tên file PDF:
  ```text
  ThiDua_<Thang>_<MaGV>.pdf
  ```
- PDF cần có thông tin đối chiếu:
  - `IDPhieu`
  - `LanNop`
  - `NgayNop`

## 13. File không được commit

Không commit:

```text
config/service_account.json
.streamlit/secrets.toml
.env
__pycache__/
*.pyc
test_*.py tạm ở thư mục gốc
log tạm
ZIP bàn giao
file backup
```

---

## 14. Ghi chú về môi trường

- `.venv/` không phải thành phần nghiệp vụ.
- Nếu `.venv/` nằm trong project, không đưa vào Git.
- Ưu tiên đặt virtual environment ở ổ local ngoài Google Drive để tránh chậm và lỗi đồng bộ.

---

## 15. Ghi chú kỹ thuật M02 - Form chấm điểm

### 15.1. Nguyên tắc giao diện nhập điểm

- Form chấm điểm phải giữ control nhập liệu thật của Streamlit hoặc component tương đương có trạng thái nhập liệu rõ ràng.
- Không thay thế ô nhập điểm bằng HTML tĩnh nếu chưa có cơ chế ghi nhận dữ liệu ổn định.
- CSS chỉ dùng để trình bày; không dùng JavaScript để tính tổng hoặc điều khiển dữ liệu chính khi chưa thống nhất.

### 15.2. Nguyên tắc tính tổng

- Tổng điểm chính thức chỉ tính từ các dòng chi tiết `CT_ThiDua` tương ứng với tiêu chí `DM_TieuChi.Loai = ITEM`.
- Không cộng dòng `GROUP`, `SECTION`, dòng tổng nhóm hoặc dòng chỉ dùng để hiển thị.
- Điểm chính thức từng dòng vẫn theo quy tắc:

```text
Nếu DiemBGH có giá trị
    dùng DiemBGH
Ngược lại
    dùng DiemGV
```

### 15.3. Nguyên tắc lưu điểm giáo viên

- Nút `Lưu` phải cập nhật điểm thành phần vào `CT_ThiDua`, không chỉ cập nhật `TH_ThiDua.TongDiem`.
- Sau khi lưu, dữ liệu cần còn đúng khi đăng xuất và đăng nhập lại.
- Khi có lỗi cấu trúc cột hoặc không tìm thấy dòng chi tiết, hệ thống phải báo lỗi rõ thay vì bỏ qua im lặng.

### 15.4. Trạng thái bản ổn định gần nhất

- Bản giao diện dùng làm nền hiện tại: `v14`.
- Bản sửa mục tiêu luồng lưu điểm thành phần: `v19`.
- Không dùng tiếp các bản `v15`, `v16`, `v17`, `v18` làm nền phát triển.
