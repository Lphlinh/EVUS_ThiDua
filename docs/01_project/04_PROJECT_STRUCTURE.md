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
