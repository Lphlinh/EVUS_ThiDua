# PROJECT_RULES

## Mục tiêu
Xây dựng phần mềm ổn định, đơn giản, dễ bảo trì và dễ mở rộng.

1. Không suy luận khi chưa có dữ liệu.
2. Hiểu nghiệp vụ trước khi viết code.
3. Không xuất code khi chưa thống nhất giải pháp.
4. Không thay đổi Google Sheets khi chưa phân tích ảnh hưởng.
5. Google Sheets là nguồn dữ liệu chính.
6. Excel chỉ dùng để nhập/xuất dữ liệu.
7. Mọi thay đổi phải nêu: ảnh hưởng, cách kiểm tra, rollback.
8. Ưu tiên an toàn hơn tốc độ.
9. Luôn kiểm thử local trước Production.
10. Không sửa trực tiếp Production.
11. Một thay đổi chỉ giải quyết một vấn đề.
12. Ưu tiên giải pháp đơn giản.
13. Không tạo dữ liệu trùng (01 giáo viên + 01 tháng = 01 bản ghi).
14. Không xóa dữ liệu khi có thể cập nhật.
15. Backup trước thay đổi lớn.
16. Chỉ kết luận từ code, dữ liệu hoặc nghiệp vụ đã xác nhận.
17. Thiếu thông tin phải hỏi lại.
18. Ghi quyết định quan trọng vào PROJECT_LOG.
19. Không mở rộng phạm vi khi chưa thống nhất.
20. Sau khi kiểm thử PASS mới commit và push GitHub.
21. Nếu phát hiện vấn đề có thể ảnh hưởng tới kiến trúc, dữ liệu hoặc khả năng bảo trì lâu dài, phải dừng viết code và trao đổi trước khi tiếp tục.
22. Khi AI chỉnh sửa tài liệu dự án, AI phải xuất file ZIP có đúng cấu trúc thư mục trong project; người dùng giải nén ZIP vào đúng thư mục gốc dự án để cập nhật.
23. Không tự sửa trực tiếp tài liệu, mã nguồn hoặc cấu trúc dữ liệu trong project khi chưa có xác nhận.
