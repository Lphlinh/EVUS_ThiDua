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
24. Tài liệu gốc, file Word, PDF, ZIP và các bản sao lưu không phải tài liệu chính thức không đưa vào repository Git. Lưu trong thư mục backup/ theo đúng nhóm chức năng.
25. Mã nguồn trong app/ phải tuân theo cấu trúc chuẩn đã thống nhất: auth, components, models, pages, services, utils. Không đặt file nghiệp vụ trực tiếp trong app/ nếu chưa thống nhất.
26. Không commit file chứa khóa bí mật hoặc thông tin xác thực, đặc biệt: config/service_account.json, .streamlit/secrets.toml, .env.
27. Nếu khóa bí mật bị lộ, phải thu hồi hoặc xóa khóa cũ trên hệ thống gốc, tạo khóa mới, ghi đè file cấu hình local, kiểm thử lại kết nối.
28. Khi tạo hoặc yêu cầu tạo file mới, AI phải ghi rõ đường dẫn đầy đủ và tên file.
29. Nếu thay đổi nhiều file hoặc nội dung dài, AI phải xuất ZIP đúng cấu trúc dự án để người dùng giải nén vào thư mục gốc.
30. AI không được nói đã cập nhật khi chưa thực sự tạo gói ZIP hoặc file để người dùng áp dụng.
31. AI được chủ động xử lý các vấn đề kỹ thuật thông thường nếu phương án rõ ràng, an toàn và không ảnh hưởng kiến trúc, dữ liệu hoặc nghiệp vụ.
32. AI chỉ dừng để trao đổi khi vấn đề ảnh hưởng đến kiến trúc, mô hình dữ liệu, nghiệp vụ, bảo mật hoặc khả năng bảo trì lâu dài.
33. Các bước kỹ thuật trung gian trình bày ngắn gọn; khi cần người dùng thao tác, yêu cầu cụ thể hoặc ghi: Gõ 1 để tiếp tục.
34. Không tạo worksheet DM_TaiKhoan nếu thông tin đăng nhập có thể quản lý trong DM_GiaoVien mà không gây trùng dữ liệu.
35. Không lưu mật khẩu gốc (plain text) trong Google Sheets, mã nguồn, log hoặc tài liệu dự án.
36. Thông tin mật khẩu chỉ được lưu dưới dạng MatKhauHash do chương trình sinh; mọi kiểm tra đăng nhập phải so sánh bằng hash.
37. Phân quyền người dùng dựa trên cột Vai trò trong DM_GiaoVien, không tạo nguồn phân quyền thứ hai khi chưa thống nhất kiến trúc.
