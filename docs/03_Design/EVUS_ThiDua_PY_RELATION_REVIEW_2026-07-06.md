# EVUS_ThiDua - Rà soát liên kết mã Python

Ngày rà soát: 2026-07-06  
Phạm vi: toàn bộ file `.py` trong dự án, loại trừ `backup/`, `.git/`, `__pycache__/`.

## 1. Mục tiêu

Rà soát các file Python để lưu lại mối liên quan giữa:

- Trang giao diện Streamlit;
- Form dùng chung;
- Service nghiệp vụ;
- Google Sheets service;
- Bảng dữ liệu `TH_ThiDua`, `CT_ThiDua`, `DM_TieuChi`, `DM_GiaoVien`;
- Các hàm có nguy cơ ảnh hưởng chéo giữa Giáo viên và BGH.

Nguyên tắc sau rà soát: trước khi sửa một lỗi phải tra tài liệu này để biết hàm nào đang được nhiều nơi dùng chung.

---

## 2. Luồng tổng quan

```text
app.py
  -> login_page.render_login_page()
  -> nếu role BGH: bgh_score_page.render_bgh_score_page()
  -> nếu role GV : teacher_score_page.render_teacher_score_page()
```

```text
teacher_score_page.py
  -> score_form_component.render_score_form(mode='teacher')
  -> thi_dua_service.get_phieu()
  -> thi_dua_service.create_phieu_for_teacher()
  -> thi_dua_service.get_chi_tiet_phieu()
  -> thi_dua_service.save_teacher_scores()
  -> thi_dua_service.validate_before_submit()
  -> thi_dua_service.submit_phieu()
```

```text
bgh_score_page.py
  -> score_form_component.render_score_form(mode='bgh')
  -> thi_dua_service.get_chi_tiet_phieu()
  -> thi_dua_service.save_bgh_scores()
  -> thi_dua_service.finalize_month()
  -> thi_dua_service.summarize_month()
  -> thi_dua_service.build_monthly_excel_export()
```

```text
thi_dua_service.py
  -> google_sheets_service.read_sheet_records()
  -> google_sheets_service.get_worksheet()
  -> criteria_service.get_all_criteria() / get_item_criteria()
  -> audit_service.write_audit_log()
```

---

## 3. Bản đồ trách nhiệm theo file

| File | Vai trò | Ghi chú rủi ro |
|---|---|---|
| `app.py` | Điều hướng theo vai trò | Không chứa nghiệp vụ điểm. Không sửa nếu chỉ lỗi GV/BGH form. |
| `app/auth/login_page.py` | Giao diện đăng nhập | Ảnh hưởng session user/role. |
| `app/pages/teacher_score_page.py` | Luồng GV: tạo phiếu, lưu, xác nhận nộp, readonly | Rủi ro cao vì dùng session state và gọi submit/save. |
| `app/pages/bgh_score_page.py` | Luồng BGH: xem, sửa điểm, chốt, tổng hợp, xuất Excel, quản trị | Rủi ro cao vì dùng cùng form và service với GV. |
| `app/components/score_form_component.py` | Form điểm dùng chung GV/BGH | Rủi ro rất cao. Sửa UI ở đây có thể ảnh hưởng cả GV và BGH. |
| `app/services/thi_dua_service.py` | Lõi nghiệp vụ thi đua | Rủi ro rất cao. Các hàm dùng chung nhiều luồng. |
| `app/services/google_sheets_service.py` | Đọc/ghi/cache Google Sheets | Rủi ro cao. Sai cache hoặc ghi theo thứ tự cột sẽ gây sai dữ liệu. |
| `app/services/criteria_service.py` | Đọc tiêu chí `DM_TieuChi` | Ảnh hưởng form và sinh `CT_ThiDua`. |
| `app/services/teacher_service.py` | Đọc giáo viên | Ảnh hưởng đăng nhập, danh sách BGH. |
| `app/services/account_service.py` | Khởi tạo password hash | Chỉ ảnh hưởng quản trị tài khoản. |
| `app/services/config_service.py` | Cấu hình hạn tự chấm | Ảnh hưởng quyền tạo phiếu. |
| `app/services/audit_service.py` | Ghi nhật ký | Không quyết định điểm, nhưng mọi thao tác quan trọng gọi qua đây. |

---

## 4. Nhóm hàm phải quản lý như API nội bộ

### 4.1. Nhóm Header `TH_ThiDua`

Các hàm liên quan:

```text
get_phieu()
get_header_by_id()
create_phieu_for_teacher()
_append_th_row_by_sheet_headers()
update_header_fields()
_canonicalize_th_record()
_get_header_map()
_canonical_header_name()
is_teacher_allowed_to_edit()
submit_phieu()
finalize_month()
summarize_month()
```

Quy tắc:

- Không ghi `TH_ThiDua` bằng thứ tự cột cố định nếu Sheet có thể đổi thứ tự.
- Khi append dòng mới phải ghi theo header thực tế của Sheet.
- `TrangThai`, `KhoaGV`, `KhoaBGH`, `NgayNop`, `TongDiem` là trường nhạy cảm.
- `is_teacher_allowed_to_edit()` không được chỉ dựa vào `KhoaGV`; phải hiểu đúng `TrangThai = 3,4,5`.

### 4.2. Nhóm Detail `CT_ThiDua`

Các hàm liên quan:

```text
get_chi_tiet_phieu()
generate_chi_tiet_from_tieu_chi()
sync_chi_tiet_from_tieu_chi()
_dedupe_ct_records()
_canonicalize_ct_record()
calculate_total_score()
save_teacher_scores()
save_bgh_scores()
```

Quy tắc:

- Chỉ dòng `ITEM` được tính tổng.
- Không sinh trùng `CT_ThiDua.ID`.
- Giáo viên chỉ ghi `DiemGV`, `GhiChuGV`.
- BGH chỉ ghi `DiemBGH`, `GhiChuBGH`.
- Điểm chính thức: nếu `DiemBGH` có giá trị thì dùng `DiemBGH`, ngược lại dùng `DiemGV`.

### 4.3. Nhóm Form dùng chung

Các hàm liên quan:

```text
render_score_form()
_render_teacher_score_form()
_render_bgh_score_form()
_prepare_rows()
_build_parent_totals()
_render_live_total()
_attach_live_total_and_sticky_header()
```

Quy tắc:

- Sửa form GV phải kiểm tra BGH vì dùng chung component.
- Sửa form BGH phải kiểm tra GV vì dùng chung component.
- Tổng điểm hiển thị trong form phải cùng quy tắc với `thi_dua_service.calculate_total_score()`.
- JavaScript chỉ hỗ trợ hiển thị, không được làm nguồn chính thức cho tổng điểm.

---

## 5. Phân tích sự cố hiện tại

### 5.1. Lỗi đã xác định và xử lý

Lỗi tạo phiếu mới bị khóa sau khi bấm Lưu.

Nguyên nhân đã xác định:

```text
create_phieu_for_teacher()
```

trước đó append `TH_ThiDua` theo thứ tự `TH_HEADERS`, trong khi Google Sheets thực tế có thêm/đổi thứ tự cột. Hậu quả là dữ liệu bị lệch cột, `NgayTao` có thể rơi vào `NgayNop`, làm logic đọc phiếu hiểu nhầm đã nộp.

Hướng sửa đúng:

```text
_append_th_row_by_sheet_headers()
```

append theo header thực tế của worksheet.

### 5.2. Lỗi BGH đang thấy

Hiện tượng:

```text
Tổng điểm trên màn hình BGH: 96
Tổng điểm dưới form: 100
```

Điều này cho thấy đang tồn tại hai nguồn tính tổng:

```text
bgh_score_page._calculate_total_score(details)  -> tổng trên
score_form_component._render_bgh_score_form()   -> tổng dưới
```

Trong `score_form_component.py`, form BGH tính `total += diem_bgh` từ ô nhập hiện hành. Sau đó `_cap_total(total)` giới hạn tối đa 100.

Trong `bgh_score_page.py`, tổng trên tính từ `details` hiện có trong Google Sheets theo quy tắc điểm chính thức.

Rủi ro: form BGH đang hiển thị tổng từ dữ liệu đang nhập trên giao diện, còn metric phía trên lấy từ dữ liệu đã lưu. Hai tổng này có thể khác nhau trước khi bấm Lưu. Nếu muốn thống nhất, phải chốt quy tắc hiển thị:

- Cách A: tổng trên luôn là tổng đã lưu; tổng dưới là tổng đang nhập. Khi đó phải đổi nhãn cho rõ.
- Cách B: chỉ hiển thị một tổng duy nhất trong form BGH, bỏ/đổi tổng phía trên.
- Cách C: sau khi BGH chỉnh ô điểm, metric trên cũng cập nhật realtime. Cách này phức tạp hơn và dễ gây lỗi.

Khuyến nghị an toàn: chọn Cách A hoặc B, không dùng JavaScript để điều khiển dữ liệu chính thức.

---

## 6. Ma trận ảnh hưởng khi sửa lỗi

| Khi sửa | Bắt buộc kiểm tra | Không được sửa kèm |
|---|---|---|
| `teacher_score_page.py` | Lưu GV, nộp GV, đăng nhập lại, xem readonly | Không sửa BGH/form/service nếu không có bằng chứng |
| `bgh_score_page.py` | Mở phiếu, sửa điểm BGH, ghi chú BGH, lưu, đọc lại, tổng điểm | Không sửa GV submit/save |
| `score_form_component.py` | Test cả GV và BGH | Không sửa service, không sửa Google Sheets |
| `save_teacher_scores()` | CT_ThiDua, TH_ThiDua.TongDiem, không đổi TrangThai | Không sửa BGH |
| `save_bgh_scores()` | DiemBGH, GhiChuBGH, TongDiem, TrangThai=4 | Không sửa GV |
| `_canonicalize_th_record()` | Trạng thái GV, BGH, chốt tháng, tổng hợp tháng | Không thêm suy luận mơ hồ từ `NgayNop` nếu không có `KhoaGV` |
| `google_sheets_service.py` cache | Mọi luồng đọc/ghi | Không sửa nghiệp vụ |

---

## 7. Checklist bắt buộc trước khi sửa code

1. Xác định lỗi thuộc nhóm nào:
   - GV page;
   - BGH page;
   - form chung;
   - service TH;
   - service CT;
   - Google Sheets cache;
   - dữ liệu Sheet.
2. Liệt kê hàm bị ảnh hưởng.
3. Kiểm tra hàm đó có được cả GV và BGH dùng chung không.
4. Nếu dùng chung, phải có test cho cả hai vai trò.
5. Chỉ sửa một nhóm nguyên nhân.
6. Sau sửa phải ghi rõ rollback file nào.

---

## 8. Bộ test hồi quy tối thiểu sau mọi bản vá

### GV

```text
GV mới -> mở phiếu -> Lưu -> TrangThai vẫn 2 -> TongDiem đúng -> vẫn sửa được
GV thiếu giải trình -> Xác nhận nộp -> cảnh báo -> Đồng ý lần 2 -> nộp được
GV đã nộp -> đăng nhập lại -> Chỉ xem -> không sửa được
```

### BGH

```text
BGH -> mở phiếu đã nộp -> thấy điểm GV
BGH -> nhập Điểm BGH + Ghi chú BGH -> Lưu
Đăng nhập lại -> đọc đúng DiemBGH/GhiChuBGH
Tổng điểm chính thức trong TH_ThiDua khớp calculate_total_score()
```

### Chốt/Tổng hợp/Xuất Excel

```text
Chốt tháng chỉ chốt TrangThai 3/4
Tổng hợp chỉ lấy TrangThai 5
Xuất Excel chỉ lấy TongHop_ThiDua
```

---

## 9. Đề xuất lưu lâu dài trong dự án

Đưa tài liệu này vào:

```text
docs/03_Design/PY_RELATION_MAP.md
```

Đưa bản machine-readable vào:

```text
docs/03_Design/py_dependency_map.json
```

Cập nhật `PROJECT_LOG` sau khi thầy thống nhất:

```text
2026-07-06 - Pilot hardening: Rà soát liên kết Python và thiết lập bản đồ phụ thuộc nội bộ trước khi sửa tiếp lỗi BGH.
```

Cập nhật `TODO`:

```text
[ ] Chuẩn hóa quy tắc hiển thị tổng điểm BGH: tổng đã lưu và tổng đang nhập.
[ ] Thêm checklist hồi quy GV/BGH trước mọi bản vá Pilot.
```
