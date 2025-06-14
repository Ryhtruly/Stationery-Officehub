## HỆ THỐNG QUẢN LÝ VĂN PHÒNG PHẨM

<p align="center"> <img src="https://res.cloudinary.com/dafqftdol/image/upload/v1748925317/SnapBG.ai_1747709355469_rkbxk6.png" alt="Logo Dự Án" width="300"/> </p> <p align="center"> <a href="#gioi-thieu">Giới thiệu</a> • <a href="#tinh-nang-chinh">Tính năng chính</a> • <a href="#cong-nghe-su-dung">Công nghệ</a> • <a href="#cai-dat-va-su-dung">Cài đặt</a> • <a href="#dong-gop">Đóng góp</a>  </p>

<a id="gioi-thieu"></a>
## Giới thiệu
Hệ thống Quản lý Văn phòng phẩm là ứng dụng giúp quản lý, mua bán sản phẩm một cách có logic thay vì thủ công như cũ. Dự án nhằm xây dựn một hệ thống quản lý toàn diện cho cửa hàng văn phòng phẩm nói riêng và các cơ sở bản hàng khác nói chung, giúp tôi ưu hóa quy trì bán hàng, quản lý kho, chăm sóc khách hàng và theo dõi hiệu quả kinh doanh

<a id="tinh-nang-chinh"></a>
## Tính năng chính 

_Quản lý tài khoản_ :
- Đăng nhập/ Đăng xuất hệ thống
- Phân quyền người dùng
- Quản lí thông tin tài khoản

_Quản lý bán hàng_ :

- Tìm kiếm và hiển thị thông tin sản phẩm
- Lọc sản phẩm theo giá, theo tên ( từ A-Z và ngược lại)
- Lọc sản phẩm theo danh mục
- Thêm sản phẩm vào giỏ hàng
- Áp dụng mã khuyến mãi
- Thanh toán và xuất hóa đơn
- Quản lý đơn hàng

_Quản lý kho, quản lý sản phẩm_ :

- Thêm, sửa, xóa sản phẩm
- Nhập kho, thêm phiếu nhập
- Xem thông tin kho
- Theo dõi tồn kho
- Cập nhật số lượng tồn
- Thêm, sửa, xóa danh mục sản phẩm

_Quản lý khách hàng_ :

- Thêm, sửa thông tin khách hàng
- Phân loại khách hàng
- Chương trình khuyến mãi cho khách hàng dựa trên phân loại

_Quản lý nhân viên_ :

- Thêm, sửa thông tin nhân viên
- Cho dừng làm việc nhân viên

_Quản lý khuyến mãi_ :

- Tạo và quản lí chương trình khuyến mãi
- Áp dụng khuyến mãi theo nhóm sản phẩm
- Khuyến mãi theo thời gian

_Báo cáo và thống kê_ :

- Báo cáo doanh thu ( theo ngày ), có thể chọn từ ngày này tới ngày khác để xem thống kê tổng
- Các loại biểu đồ hiển thị theo vùng, cột, đường
- Phân tích tổng doanh thu
- Xuất báo cáo

_Phản hồi và góp ý_ :

- Gửi báo lỗi đến nhà phát triển
- Đóng góp ý kiến cải thiện hệ thống

<a id="cong-nghe-su-dung"></a>
## Công nghệ

_Công nghệ sử dụng_ :

- Ngôn ngữ lập trình : Python
- Framework UI : PyQt5
- Cơ sở dữ liệu : Microsoft SQl Server
- Mô hình truy cap liệu : DAO Pattern

_Công cụ phát triển_ :

- IDE : Visual Studio Code, Pycharm
- Quản lí mã nguồn : GitHub
- Thiết kế giao diện : Qt Designer
- Tạo báo cáo : ReportLab

_Yêu cầu hệ thống_ :

- Python 3.8 hoặc cao hơn
- SQL Server 2019
- 4GB RAM trở lên
- Hệ điều hành: Windows 10/11

_Kiến trúc ứng dụng_ :

- Mô hình : MVC ( Model - View _ Controller)
- Giao diện : Desktop Application
- Kết nối CSDL : Pyodbc
- Xử lý báo cáo : ReportLab, Matplotlib
- API RESTful : Flask
- Upload hình ảnh : Cloudinary

<a id="cai-dat-va-su-dung"></a>
## Cài đặt 

_Cài đặt môi trường_ :

1. Cài đặt Python :
- Tải Python 3.8 hoặc cao hơn từ [python.org](https://www.python.org/downloads/).
- Chay file cài đặt, đánh dầu tùy chọn "Add Python to Path"
- Nhấn "Install Now" và chờ quá trình cài đặt hoàn tất
- Kiểm tra cài đặt bằng cách mở Command Prompt và gõ : python --version

2. Cài đặt MS SQL Server :
- Tải [Microsoft SQL Server 2019 Express](https://www.microsoft.com/en-us/sql-server/sql-server-downloads) từ trang chủ Microsoft.
- Chọn **SQL Server Express** hoặc **Developer Edition**.
- Tải và chạy file cài đặt (ví dụ: `SQL2019-SSEI-Expr.exe`).
- Chọn **Basic** installation, giữ mặc định hoặc đặt tên instance (ví dụ: `SQLEXPRESS`).
- Ghi lại **Connection String** (ví dụ: `Server=localhost\SQLEXPRESS;Database=master;Trusted_Connection=True;`).

3. Cài đặt các thư viện Python cần thiết 
- Mở **Terminal** trên IDE đã được cài đặt trước đó và thực hiện lệnh sau : `pip install -r requirements.txt`
- Sau đó các thư viện cần thiết sẽ được cài đặt

_Thiết lập cơ sở dữ liệu_ :

1. **Cài đặt SQL Server Management Studio (SSMS):**
   - Tải SSMS từ: [SSMS Downloads](https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms).
   - Cài đặt và mở SSMS.
   - Kết nối đến server SQL Server bạn đã cài đặt ở bước trước (thường là `localhost\SQLEXPRESS`) bằng **Windows Authentication**.

2. **Tạo và thiết lập cơ sở dữ liệu:**
   - Mở SSMS và kết nối đến server.
   - Mở file `setup/setup_database.sql` trong thư mục dự án.
   - Copy toàn bộ nội dung file và dán vào một query mới trong SSMS (File > New > Query).
   - Nhấn **Execute** (hoặc phím F5) để chạy script.
     - Script sẽ tạo cơ sở dữ liệu `Stationery`, các bảng cần thiết, và chèn dữ liệu mẫu ( chú ý dữ liệu đã được có trong file setup, bạn có thể chỉnh sửa tùy ý dựa trên chức năng có trên ứng dụng.

       3. **Kiểm tra cơ sở dữ liệu:**
          - Sau khi chạy script, kiểm tra xem cơ sở dữ liệu `Stationery` đã được tạo chưa bằng cách mở rộng mục **Databases** trong SSMS.
            - Mở rộng `Stationery` > **Tables** để xem các bảng như `Accounts`, `Products`, `Employees`, v.v.
              - Nếu không có lỗi, bạn đã thiết lập thành công cơ sở dữ liệu.

                4. **Cấu hình kết nối cơ sở dữ liệu trong ứng dụng:**
                   - Mở file `.env` trong dự án ( hoặc tạo nếu như không có ).
                     - Sửa connection string để khớp với SQL Server của bạn. Ví dụ:
                       ```python
                           DB_SERVER=MSI\SQLEXPRESS
                           DB_NAME=Stationery
                           DB_USERNAME=sa
                           DB_PASSWORD=123
                           CLOUDINARY_CLOUD_NAME=dpbfb6hai
                           CLOUDINARY_API_KEY=536479469775784
                           CLOUDINARY_API_SECRET=LXFgaRYj07-SAWCAcCzu9OcbgSo ( các set up cho service cùng lúc )
              

_Đăng nhập_ :

- Tài khoản admin : Username : `admin` , Password : `admin123`
- Tài khoản nhân viên : Username : `employee1`, Password : `emp123`
- Các dữ liệu trên sẽ hoạt động nếu như bạn setup đúng database
- Bạn hoàn toàn có thể chỉnh sửa 


<a id="dong-gop"></a>
## Đóng góp

Chúng tôi rất hoan nghênh mọi ý kiến đóng góp, báo lỗi hoặc đề xuất cải tiến từ người dùng để hệ thống ngày càng hoàn thiện hơn! Nếu bạn có bất kỳ ý kiến nào, vui lòng gửi email đến:

- Email: [n22dccn089@student.ptithcm.edu.vn](mailto:n22dccn089@student.ptithcm.edu.vn) - Lê Hữu Trí
- Email: [n22dccn088@student.ptithcm.edu.vn](mailto:n22dccn089@student.ptithcm.edu.vn) - Đỗ Xuân Trí
- Email: [n22dccn089@student.ptithcm.edu.vn](mailto:n22dccn094@student.ptithcm.edu.vn) - Nguyễn Minh Tú

Khi gửi email, xin vui lòng:
- Đặt tiêu đề email theo định dạng: `[Đóng góp] - <Tiêu đề ý kiến>` (ví dụ: `[Đóng góp] - Lỗi hiển thị danh sách sản phẩm`).
- Cung cấp thông tin chi tiết về ý kiến, lỗi gặp phải (nếu có), hoặc đề xuất của bạn.
- Nếu có lỗi, hãy mô tả chi tiết (kèm ảnh chụp màn hình nếu được) và phiên bản hệ điều hành bạn đang sử dụng.

Cảm ơn bạn đã đóng góp để giúp dự án ngày càng tốt hơn!

## Giấy phép

Dự án **OfficeHub © 2025** được phát triển bởi nhóm sinh viên N22DCCN (Lê Hữu Trí, Đồ Xuân Trí, Nguyễn Minh Tú). Mọi quyền sở hữu trí tuệ thuộc về nhóm tác giả.

Dự án được phát hành dưới **Giấy phép MIT (MIT License)**. Điều này có nghĩa là bạn có thể tự do sử dụng, sao chép, chỉnh sửa và phân phối mã nguồn, miễn là giữ nguyên thông tin bản quyền và không sử dụng tên dự án "OfficeHub" cho mục đích thương mại mà không có sự cho phép từ nhóm tác giả.

- Xem chi tiết giấy phép tại: [MIT License](https://opensource.org/licenses/MIT).

Nếu bạn muốn sử dụng "OfficeHub" cho mục đích thương mại hoặc cần thêm thông tin, vui lòng liên hệ qua email: [n22dccn089@student.ptithcm.edu.vn](mailto:n22dccn089@student.ptithcm.edu.vn).