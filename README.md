# NHAPMON_CNPM_NHOM-3_DUANQUANLYBANBILLIARDS
Xây dựng một phần mềm quản lý bàn billiards dễ sử dụng. Giúp vận hành hiệu quả, giảm sai sót thủ công, nâng cao trải nghiệm khách hàng và tạo nền tảng mở rộng trong tương lai.
# CÔNG NGHỆ SỬ DỤNG    
- Ngôn ngữ: python
- Công cụ: Github, Trello, VS Code,...

# HƯỚNG DẪN CÀI ĐẶT HỆ THỐNG    
DỰ ÁN: QUẢN LÝ BÀN BILLIARDS

1. Giới thiệu
Hệ thống Quản lý Bàn Billiards được xây dựng nhằm hỗ trợ chủ quán và nhân viên quản lý bàn chơi, thời gian sử dụng, tính tiền, quản lý hóa đơn và theo dõi tình trạng hoạt động của các bàn billiards một cách hiệu quả và chính xác.

3. Yêu cầu hệ thống  
2.1. Phần cứng  
    - CPU: Intel Core i3 trở lên
    - RAM: Tối thiểu 4GB (khuyến nghị 8GB)
    - Ổ cứng: Tối thiểu 5GB dung lượng trống
  
    2.2. Phần mềm  
    - Hệ điều hành: Windows 10 / Windows 11
    - Trình duyệt: Google Chrome hoặc Microsoft Edge
    - Phần mềm cần thiết:  
 Python 3.9+  
 MySQL / SQL Server (tùy hệ thống)  
 Git (nếu tải mã nguồn từ GitHub)  

3. Cài đặt môi trường
- Bước 1: Cài đặt Python
 Tải Python tại: https://www.python.org
 Trong quá trình cài đặt, tick chọn “Add Python to PATH”
- Bước 2: Cài đặt hệ quản trị cơ sở dữ liệu
 Cài đặt MySQL (hoặc hệ CSDL được sử dụng)
 Ghi nhớ:  
 Tên người dùng (username)  
 Mật khẩu  
 Cổng kết nối (thường là 3306)  

4. Cài đặt hệ thống
- Bước 3: Tải mã nguồn
 Clone từ GitHub: git clone <link-github-du-an>
 Hoặc giải nén file dự án được cung cấp.
- Bước 4: Cài đặt thư viện cần thiết
 Di chuyển vào thư mục dự án: cd QuanLyBanBilliards
- Bước 5: Cấu hình hệ thống
 Mở file cấu hình (config.py, .env hoặc tương đương)
 Cập nhật thông tin:  
DB_NAME = billiards_db  
DB_USER = root  
DB_PASSWORD = 123456  
DB_HOST = localhost  
DB_PORT = 3306  

5. Cài đặt cơ sở dữ liệu
- Bước 6: Tạo cơ sở dữ liệu
 Mở MySQL
 Tạo database:  CREATE DATABASE billiards_db
- Bước 7: Import dữ liệu  
Import file billiards_db.sql (nếu có)  
Hoặc chạy script tạo bảng được cung cấp trong dự án

6. Chạy hệ thống
- Bước 8: Khởi động chương trình
python main.py
Hoặc:
python app.py

7. Kiểm tra hoạt động
- Mở giao diện chính của hệ thống
Thử các chức năng:  
Thêm / sửa / xóa bàn billiards  
Mở bàn – đóng bàn  
Tính tiền theo thời gian chơi  
Lập hóa đơn

8. Xử lý lỗi thường gặp

9. Kết luận
- Hệ thống Quản lý Bàn Billiards sau khi cài đặt thành công sẽ giúp tối ưu hóa việc quản lý quán, giảm sai sót và nâng cao hiệu quả kinh doanh.

# Tên nhóm: nhóm 3
# Tên thành viên:
  - Đinh Hoàng Gia Bảo
  - Mai Huy Nhật
  - Văn Công Quyết
  - Nguyễn Ngọc Tân
  - Nguyễn Trường Giang
