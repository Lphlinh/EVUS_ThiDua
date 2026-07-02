# EVUS_ThiDua

Hệ thống chấm điểm thi đua giáo viên, triển khai độc lập trên subdomain của trường.

## Công nghệ

- Python
- Streamlit
- Google Sheets
- VS Code

## Nguyên tắc

- Google Sheets là nguồn dữ liệu chính.
- Excel chỉ dùng để nhập/xuất báo cáo.
- Không sửa trực tiếp Production.
- Test local trước khi triển khai.
- Một giáo viên + một tháng = một bản ghi thi đua.

## Tài liệu dự án

Tài liệu chính nằm tại:

```text
docs/01_Project
```

Thứ tự đọc khi bắt đầu phiên làm việc:

1. `00_BOOT_CONTEXT.md`
2. `01_PROJECT_RULES.md`
3. `02_PROJECT_LOG.md`
4. `03_TODO.md`

## Chạy local

```bash
streamlit run app.py
```

Hoặc double click:

```text
run_local.bat
```
