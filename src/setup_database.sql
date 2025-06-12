-- Tạo cơ sở dữ liệu
CREATE DATABASE Stationery;
GO

USE Stationery;
GO

-- Tạo các bảng
CREATE TABLE dbo.Accounts (
    id_account int NOT NULL,
    username varchar(50) NOT NULL,
    password varchar(50) NOT NULL,
    id_emp int NULL,
    id_ad int NULL,
    role varchar(20) NOT NULL,
    is_active bit NULL,
    created_at datetime NULL
);

CREATE TABLE dbo.Admin (
    id_ad int NOT NULL,
    fullname nvarchar(100) NOT NULL,
    address nvarchar(200) NULL,
    phone varchar(15) NULL,
    email varchar(100) NULL
);

CREATE TABLE dbo.Bill (
    id_bill int NOT NULL,
    id_cust int NULL,
    id_emp int NOT NULL,
    total float NOT NULL,
    date datetime NOT NULL
);

CREATE TABLE dbo.Bill_detail (
    id_bill int NOT NULL,
    id_prod int NOT NULL,
    quantity int NOT NULL,
    price float NOT NULL,
    discount float NULL
);

CREATE TABLE dbo.Card (
    rank nvarchar(20) NOT NULL,
    discount float NOT NULL
);

CREATE TABLE dbo.Categories (
    id_category int NOT NULL,
    name nvarchar(50) NULL
);

CREATE TABLE dbo.Customers (
    id_cust int NOT NULL,
    fullname nvarchar(100) NOT NULL,
    phone varchar(10) NULL,
    rank nvarchar(20) NOT NULL,
    register_date date NULL
);

CREATE TABLE dbo.Employees (
    id_emp int NOT NULL,
    fullname nvarchar(100) NOT NULL,
    address nvarchar(100) NULL,
    phone varchar(15) NULL,
    salary float NULL,
    email varchar(100) NULL,
    status int NOT NULL
);

CREATE TABLE dbo.Import (
    id_imp int NOT NULL,
    id_emp int NOT NULL,
    date datetime NOT NULL
);

CREATE TABLE dbo.Import_detail (
    id_imp int NOT NULL,
    id_prod int NOT NULL,
    quantity int NOT NULL,
    price float NOT NULL
);

CREATE TABLE dbo.Products (
    id_prod int NOT NULL,
    name nvarchar(50) NOT NULL,
    unit nvarchar(20) NULL,
    price float NOT NULL,
    description nvarchar(100) NULL,
    id_category int NOT NULL,
    price_import float NULL,
    image_url nvarchar(255) NULL,
    promotion_price float NULL
);

CREATE TABLE dbo.Promotion (
    id_prom int NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    name varchar(255) NULL
);

CREATE TABLE dbo.Promotion_detail (
    id_prom int NOT NULL,
    id_category int NOT NULL,
    percent_discount float NOT NULL
);

CREATE TABLE dbo.Warehouse (
    id_warehouse int NOT NULL,
    name nvarchar(50) NOT NULL,
    address nvarchar(100) NULL,
    phone varchar(10) NULL
);

CREATE TABLE dbo.Warehouse_Product (
    id_warehouse int NOT NULL,
    id_prod int NOT NULL,
    inventory int NOT NULL
);

-- Thêm khóa chính
ALTER TABLE dbo.Accounts ADD CONSTRAINT PK__Accounts__B2C7C7837CAF304A PRIMARY KEY (id_account);
ALTER TABLE dbo.Admin ADD CONSTRAINT PK__Admin__01482935E3F66273 PRIMARY KEY (id_ad);
ALTER TABLE dbo.Bill ADD CONSTRAINT PK__Bill__C56081F5F64360F8 PRIMARY KEY (id_bill);
ALTER TABLE dbo.Bill_detail ADD CONSTRAINT PK__Bill_det__E5BAB57250215D83 PRIMARY KEY (id_bill, id_prod);
ALTER TABLE dbo.Card ADD CONSTRAINT PK_Card_rank PRIMARY KEY (rank);
ALTER TABLE dbo.Categories ADD CONSTRAINT PK__Categori__E548B67313BC5499 PRIMARY KEY (id_category);
ALTER TABLE dbo.Customers ADD CONSTRAINT PK__Customer__170C743653528C56 PRIMARY KEY (id_cust);
ALTER TABLE dbo.Employees ADD CONSTRAINT PK__Employee__D52A94EFA436B017 PRIMARY KEY (id_emp);
ALTER TABLE dbo.Import ADD CONSTRAINT PK__Import__D62AA42CA384AD76 PRIMARY KEY (id_imp);
ALTER TABLE dbo.Import_detail ADD CONSTRAINT PK__Import_d__F6F090ABB54F8366 PRIMARY KEY (id_imp, id_prod);
ALTER TABLE dbo.Products ADD CONSTRAINT PK__Products__0DA3487393E843CD PRIMARY KEY (id_prod);
ALTER TABLE dbo.Promotion ADD CONSTRAINT PK__Promotio__0DA348442BBD50D7 PRIMARY KEY (id_prom);
ALTER TABLE dbo.Promotion_detail ADD CONSTRAINT PK__Promotio__23F7C3233CBCD390 PRIMARY KEY (id_prom, id_category);
ALTER TABLE dbo.Warehouse ADD CONSTRAINT PK__Warehous__BBAE61063143A6AB PRIMARY KEY (id_warehouse);
ALTER TABLE dbo.Warehouse_Product ADD CONSTRAINT PK__Warehous__9B745581E310A052 PRIMARY KEY (id_warehouse, id_prod);

-- Thêm khóa ngoại
ALTER TABLE dbo.Accounts ADD CONSTRAINT FK__Accounts__id_ad__236943A5 FOREIGN KEY (id_ad) REFERENCES dbo.Admin (id_ad);
ALTER TABLE dbo.Accounts ADD CONSTRAINT FK__Accounts__id_emp__22751F6C FOREIGN KEY (id_emp) REFERENCES dbo.Employees (id_emp);
ALTER TABLE dbo.Bill ADD CONSTRAINT FK_Bill_Customers_id_cust FOREIGN KEY (id_cust) REFERENCES dbo.Customers (id_cust);
ALTER TABLE dbo.Bill ADD CONSTRAINT FK_Bill_Employees_id_emp FOREIGN KEY (id_emp) REFERENCES dbo.Employees (id_emp);
ALTER TABLE dbo.Bill_detail ADD CONSTRAINT FK_Bill_detail_Bill_id_bill FOREIGN KEY (id_bill) REFERENCES dbo.Bill (id_bill);
ALTER TABLE dbo.Bill_detail ADD CONSTRAINT FK_Bill_detail_Products_id_prod FOREIGN KEY (id_prod) REFERENCES dbo.Products (id_prod);
ALTER TABLE dbo.Customers ADD CONSTRAINT FK_Customers_Card_rank FOREIGN KEY (rank) REFERENCES dbo.Card (rank);
ALTER TABLE dbo.Import ADD CONSTRAINT FK_Import_Employees_id_emp FOREIGN KEY (id_emp) REFERENCES dbo.Employees (id_emp);
ALTER TABLE dbo.Import_detail ADD CONSTRAINT FK_Import_detail_Import_id_imp FOREIGN KEY (id_imp) REFERENCES dbo.Import (id_imp);
ALTER TABLE dbo.Import_detail ADD CONSTRAINT FK_Import_detail_Products_id_prod FOREIGN KEY (id_prod) REFERENCES dbo.Products (id_prod);
ALTER TABLE dbo.Products ADD CONSTRAINT FK_Products_Categories_id_category FOREIGN KEY (id_category) REFERENCES dbo.Categories (id_category);
ALTER TABLE dbo.Promotion_detail ADD CONSTRAINT FK__Promotion__id_ca__46693276 FOREIGN KEY (id_category) REFERENCES dbo.Categories (id_category);
ALTER TABLE dbo.Promotion_detail ADD CONSTRAINT FK__Promotion__id_pr__45750E3D FOREIGN KEY (id_prom) REFERENCES dbo.Promotion (id_prom);
ALTER TABLE dbo.Warehouse_Product ADD CONSTRAINT FK_Warehouse_Product_Products_id_prod FOREIGN KEY (id_prod) REFERENCES dbo.Products (id_prod);
ALTER TABLE dbo.Warehouse_Product ADD CONSTRAINT FK_Warehouse_Product_Warehouse_id_warehouse FOREIGN KEY (id_warehouse) REFERENCES dbo.Warehouse (id_warehouse);

-- Chèn dữ liệu mẫu

-- Insert data into Accounts table
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (1, 'admin', '123456', NULL, 1, 'Admin', 1, '2025-04-21 12:16:10.637');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (2, 'employee1', '123', 1, NULL, 'Employee', 1, '2025-04-21 12:16:10.637');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (3, 'employee', '123', 1, NULL, 'Employee', 1, '2025-04-21 12:19:27.437');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (4, 'tranthibinh', '123456', 2, NULL, 'Employee', 1, '2025-04-21 12:19:27.447');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (5, 'phamvancuong', '123456', 3, NULL, 'Employee', 1, '2025-04-21 12:19:27.447');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (7, 'hoangvanem', '123456', 5, NULL, 'Employee', 1, '2025-04-21 12:19:27.447');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (8, 'ngothiphuong', '123456', 6, NULL, 'Employee', 1, '2025-04-21 12:19:27.450');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (9, 'truongvangiap', '123456', 7, NULL, 'Employee', 1, '2025-04-21 12:19:27.450');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (10, 'lythihuong', '123456', 8, NULL, 'Employee', 1, '2025-04-21 12:19:27.450');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (11, 'dovanich', '123456', 9, NULL, 'Employee', 1, '2025-04-21 12:19:27.450');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (12, 'nguyenthikim', '123', 10, NULL, 'Employee', 1, '2025-04-21 12:19:27.450');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (13, 'tranvanlam', '123456', 11, NULL, 'Employee', 1, '2025-04-21 12:19:27.450');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (14, 'phamthiminh', '1234567890', 12, NULL, 'Employee', 1, '2025-04-21 12:19:27.450');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (15, 'levannam', '123456', 13, NULL, 'Employee', 1, '2025-04-21 12:19:27.450');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (16, 'hoangthioanh', '123456', 14, NULL, 'Employee', 1, '2025-04-21 12:19:27.450');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (17, 'ngovanphuc', '123456', 15, NULL, 'Employee', 1, '2025-04-21 12:19:27.450');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (18, 'truongthiquynh', '123456', 16, NULL, 'Employee', 1, '2025-04-21 12:19:27.450');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (19, 'lyvanrong', '123456', 17, NULL, 'Employee', 1, '2025-04-21 12:19:27.450');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (20, 'dothisen', '123456', 18, NULL, 'Employee', 0, '2025-04-21 12:19:27.450');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (21, 'nguyenvantam', '123', 19, NULL, 'Employee', 1, '2025-04-21 12:19:27.450');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (22, 'tranthiuyen', '123456', 20, NULL, 'Employee', 1, '2025-04-21 12:19:27.450');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (25, 'nhanvien99', '123', 99, NULL, 'employee', 1, '2025-04-28 20:12:13.193');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (26, 'nhanvien100', '123456', 100, NULL, 'employee', 1, '2025-04-28 20:51:57.733');
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at) VALUES (27, 'lehuutri', 'lehuutri20', 101, NULL, 'employee', 1, '2025-06-03 00:41:21.613');

-- Insert data into Admin table
INSERT INTO dbo.Admin (id_ad, fullname, address, phone, email) VALUES (1, N'Nguyễn Văn Admin', N'123 Lê Lợi, HCm', '0901234568', 'admin@email.com');

-- Insert data into Bill table
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (1, 1, 3, 350000, '2023-01-15 10:30:00.000');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (3, 8, 5, 180000, '2023-01-18 09:15:00.000');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (4, 10, 11, 430000, '2023-01-20 16:30:00.000');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (5, 15, 12, 275000, '2023-01-22 11:20:00.000');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (6, 3, 3, 30400, '2025-05-04 11:38:13.863');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (7, 6, 3, 1700, '2025-05-04 12:13:32.870');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (8, NULL, 3, 20000, '2025-05-05 14:05:17.703');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (9, 6, 3, 9500, '2025-05-05 15:44:18.580');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (10, NULL, 3, 20000, '2025-05-05 22:39:16.060');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (11, NULL, 3, 120000, '2025-05-17 18:21:18.270');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (12, NULL, 3, 4500, '2025-05-17 18:22:38.197');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (13, NULL, 3, 4500, '2025-05-17 20:30:26.043');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (14, 10, 3, 17000, '2025-05-19 10:33:27.863');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (15, 13, 3, 64845, '2025-05-19 10:42:24.240');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (16, NULL, 3, 12000, '2025-05-19 15:35:37.843');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (17, NULL, 11, 20000, '2025-05-19 15:41:10.753');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (18, NULL, 1, 35000, '2025-05-19 16:00:32.553');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (19, NULL, 1, 28000, '2025-05-19 16:16:52.617');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (20, NULL, 1, 12000, '2025-05-19 16:28:37.990');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (21, NULL, 1, 31500, '2025-05-19 16:57:43.083');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (22, NULL, 1, 85000, '2025-05-19 17:00:25.430');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (23, NULL, 1, 12000, '2025-05-19 17:14:25.413');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (24, NULL, 1, 166750, '2025-05-19 17:17:58.603');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (25, NULL, 1, 78300, '2025-05-19 21:12:21.843');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (26, NULL, 1, 78300, '2025-05-19 21:12:46.497');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (27, NULL, 1, 30000, '2025-05-20 15:50:22.383');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (28, NULL, 1, 25000, '2025-05-20 15:50:43.240');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (29, NULL, 1, 60000, '2025-05-20 15:51:04.900');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (30, 12, 1, 26172.5, '2025-06-03 22:28:05.290');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (31, NULL, 2, 25000, '2025-06-04 08:09:59.000');
INSERT INTO dbo.Bill (id_bill, id_cust, id_emp, total, date) VALUES (32, 1, 2, 21250, '2025-06-04 08:10:38.577');


INSERT INTO dbo.Bill_detail (id_bill, id_prod, quantity, price, discount) VALUES
(1, 1, 20, 5000, 0),
(1, 3, 10, 15000, 0),
(1, 6, 2, 85000, 0),
(3, 2, 20, 3000, 0),
(3, 10, 10, 8000, 0),
(4, 15, 6, 35000, 0.1),
(4, 18, 5, 30000, 0),
(5, 7, 10, 12000, 0),
(5, 16, 10, 12000, 0.05),
(6, 23, 1, 10000, 0.05),
(6, 24, 1, 20000, 0.05),
(6, 26, 1, 2000, 0.05),
(7, 12345, 2, 1000, 0.15),
(8, 1, 4, 5000, 0),
(9, 23, 1, 10000, 0.05),
(10, 25, 1, 20000, 0),
(11, 77, 1, 100000, 0),
(11, 679, 1, 20000, 0),
(12, 1, 1, 4500, 0),
(13, 1, 1, 4500, 0),
(14, 234, 1, 20000, 0.15),
(15, 1, 1, 4500, 0.1),
(15, 7, 1, 10800, 0.1),
(15, 15, 1, 29750, 0.1),
(15, 18, 1, 27000, 0.1),
(21, 1, 1, 4500, 0),
(21, 18, 1, 27000, 0),
(22, 6, 1, 85000, 0),
(24, 6, 1, 85000, 0),
(24, 13, 1, 25000, 0),
(24, 15, 1, 29750, 0),
(24, 18, 1, 27000, 0),
(25, 5, 1, 40500, 0),
(25, 7, 1, 10800, 0),
(25, 18, 1, 27000, 0),
(26, 5, 1, 40500, 0),
(26, 7, 1, 10800, 0),
(26, 18, 1, 27000, 0),
(27, 13, 1, 25000, 0),
(27, 77, 1, 5000, 0),
(28, 13, 1, 25000, 0),
(29, 19, 1, 30000, 0),
(29, 12345, 1, 30000, 0),
(30, 67, 1, 2550, 0.05),
(30, 77, 1, 5000, 0.05),
(30, 560, 1, 20000, 0.05),
(31, 77, 1, 5000, 0),
(31, 560, 1, 20000, 0),
(32, 77, 1, 5000, 0.15),
(32, 560, 1, 20000, 0.15);

INSERT INTO dbo.Card (rank, discount) VALUES
(N'Bronze', 0.05),
(N'Diamond', 0.25),
(N'Gold', 0.15),
(N'Platinum', 0.2),
(N'Silver', 0.1);

INSERT INTO dbo.Categories (id_category, name) VALUES
(1, N'Bút Viết'),
(2, N'Vở sổ'),
(3, N'Dụng cụ học tập'),
(4, N'Giấy in'),
(5, N'Keo dán'),
(6, N'Dụng cụ văn phòng'),
(7, N'Lưu Trữ'),
(8, N'Thiết bị văn phòng'),
(10, N'Quà tặng'),
(11, N'Pin'),
(12, N'Phụ kiện'),
(13, N'Máy tính'),
(14, N'Toán');

INSERT INTO dbo.Customers (id_cust, fullname, phone, rank, register_date) VALUES
(1, N'Lê Hữu Trí', '0901234567', N'Bronze', '2023-01-15'),
(2, N'Nhà sách Phuong Nam', '0912345678', N'Platinum', '2024-11-16'),
(3, N'Nguyễn Minh Tú', '0923456789', N'Bronze', '2025-03-16'),
(5, N'Đỗ Xuân Trí', '0945678901', N'Diamond', '2023-04-16'),
(6, N'Le Tri', '0843469437', N'Bronze', '2024-05-16'),
(7, N'Văn phòng luật sư công lý', '0967890123', N'Bronze', '2025-03-16'),
(8, N'Công ty tnhh sáng tạo', '0978901234', N'Silver', '2025-03-16'),
(10, N'Công ty dịch vụ toàn cầu', '0990123456', N'Bronze', '2024-05-16'),
(12, N'Trường trung học cơ sở Chu Văn An', '0912345679', N'Bronze', '2025-03-16'),
(13, N'Công Ty TNHH thương mại Nhật Minh', '0923456780', N'Bronze', '2025-03-16'),
(14, N'Van phòng Công chứng số 5', '0934567891', N'Bronze', '2025-03-16'),
(15, N'Trường đại học kinh tế', '0945678902', N'Gold', '2024-05-16'),
(16, N'Công ty CP Xuất khẩu', '0956789013', N'Silver', '2025-03-16'),
(17, N'Nhà sách Cá Chép', '0967890124', N'Bronze', '2025-03-16'),
(21, N'Nhà sách mực tím', '0123456789', N'Bronze', '2025-04-22'),
(22, N'Lê Hữu Trí', '0888261513', N'Bronze', '2025-04-22'),
(23, N'Anh Bảy', '0983452389', N'Bronze', '2025-05-02'),
(24, N'Nguyễn Len', '0593457385', N'Bronze', '2025-06-03'),
(25, N'Anh Khánh', '0834627458', N'Bronze', '2025-06-03');
INSERT INTO dbo.Employees (id_emp, fullname, address, phone, salary, email, status) VALUES
(1, N'Nguyễn Văn An', N'123 Lê lợi , hà nội', '0901234568', 15000000, 'nguyenvanan@example.com', 1),
(2, N'Trần Thi Bình', N'45 Nguyễn Huệ, Hồ Chí Minh', '0912345678', 12000000, 'tranthibình@example.com', 1),
(3, N'Phạm Văn Cường', N'78 Trần Hưng Đạo , Đà Nẵng', '0923456789', 10000000, 'phamvancuong@example.com', 1),
(5, N'Hoàng Van Em', N'89 Lê Duẩn, Hồ Chí Minh', '0945678901', 8000000, 'emailnhanvien5@gmail.com', 1),
(6, N'Ngô thị phương', N'268 Lý thường kiệt, hồ chí minh', '0956789012', 7500000, 'ngôthiphuong@example.com', 1),
(7, N'Truong Van Giáp', N'34 Nguyễn Du, Hà Nội', '0967890123', 7500000, 'truongvangiáp@example.com', 0),
(8, N'Lý Thị Hương', N'Ðà Nẵng', '0978901234', 8500000, 'lýthihuong@example.com', 1),
(9, N'Đỗ Văn Ích', N'56 Trần Phú, Hải Phòng', '0989012345', 12000000, 'dovaních@example.com', 1),
(10, N'Nguyễn Thị Kim', N'78 Lê Thánh Tông, Hà Nội', '0990123456', 9000000, 'nguyenthikim@example.com', 1),
(11, N'Trần Văn Lâm', N'45 Nguyễn Thị Minh Khai, Hồ Chí Minh', '0901234568', 8000000, 'tranvanlâm@example.com', 1),
(12, N'Phạm thị Minh', N'23 Lê Lợi, Hà Nội', '0912345679', 8000000, 'phamthiminh@example.com', 1),
(13, N'Lê Van Nam', N'Ðà Năng', '0923456780', 7500000, 'levannam@example.com', 1),
(14, N'Hoàng Thu Oanh', N'89 Bà Triệu, Hà Nội', '0934567891', 9500000, 'hoàngthuoanh@example.com', 1),
(15, N'Ngô Van Phúc', N'15 Giải Phóng, Hà Nội', '0945678902', 8500000, 'ngôvanphúc@example.com', 1),
(16, N'Trương Thi Quỳnh', N'56 Lý Tự Trọng, Hồ Chí Minh', '0956789013', 9000000, 'truongthiqunh@example.com', 1),
(17, N'Lý Văn Văn', N'78 Nguyễn Huệ, Hồ Chí Minh', '0967890124', 9000000, 'lývanvan@example.com', 1),
(18, N'Đỗ Thị Sen', N'100 Nguyễn Thị Minh Khai, Hồ Chí Minh', '0978901235', 8000000,  'dothsen@example.com', 0),
(19, N'Nguyễn Văn Tâm', N'34 Lê Duẫn, Hà Nội', '0989012346', 8000000, 'nguyenvantâm@example.com', 1),
(20, N'Trần Thị Uyên', N'45 Bà Triệu, Hải Phòng', '0990123457', 7500000, 'tranthyên@example.com', 1),
(30, N'Lê Hữu Trí', N'78 Lê Thánh Tông, Hà Nội', '0843469437', 200000, 'lehuutriexample@gmail.com', 1),
(98, N'Lê Hữu Trí', N'78 Trần Hưng Đạo , Đà Nẵng', '0843469437', 20000, 'lehuutri1609@gmail.com', 1),
(99, N'Nhân viên 99', N'45 Nguyễn Huệ, Hồ Chí Minh', '0102345679', 120000, 'nhânviên99@example.com', 1),
(100, N'nhan viên 100', N'89 Lê Duẩn, Hồ Chí Minh', '0987623456', 100000, 'nhanvien100@gmail.com', 1),
(101, N'lehuutri', N'tphcm', '0888232525', 2000, 'emailnhanvien101@gmail.com', 1);

INSERT INTO dbo.Import (id_import, id_emp, import_date) VALUES
(1, 6, '2023-01-10 08:30:00.000'),
(2, 7, '2023-01-12 09:45:00.000'),
(3, 13, '2023-01-14 10:15:00.000'),
(4, 20, '2023-01-17 14:30:00.000'),
(5, 6, '2023-01-19 15:20:00.000'),
(6, 98, '2025-04-24 15:13:12.347'),
(7, 7, '2025-04-24 18:56:14.843'),
(8, 30, '2025-04-24 19:20:16.053'),
(9, 7, '2025-04-24 19:58:27.703'),
(10, 2, '2025-05-05 16:31:03.830'),
(11, 1, '2025-05-27 17:45:04.800'),
(12, 3, '2025-05-27 22:12:08.460'),
(20, 8, '2025-05-27 22:56:00.217'),
(21, 5, '2025-05-27 22:58:43.827'),
(34, 1, '2025-06-03 22:12:45.520'),
(35, 1, '2025-06-12 01:00:57.390');

INSERT INTO dbo.Import_detail (id_import, id_prod, quantity, price) VALUES
(1, 1, 100, 3500),
(1, 2, 150, 2000),
(1, 3, 80, 11000),
(2, 5, 50, 32000),
(2, 6, 50, 70000),
(3, 7, 70, 8000),
(3, 8, 60, 12000),
(4, 10, 80, 5000),
(4, 12, 100, 7000),
(5, 13, 55, 18000),
(5, 15, 45, 25000),
(6, 679, 20, 1000),
(7, 34, 200, 2000),
(7, 45, 300, 4000),
(8, 77, 20, 2000),
(9, 12345, 200, 20000),
(10, 124, 100, 2000),
(11, 60, 100, 4000),
(12, 12346, 20, 20000),
(20, 12354, 100, 23000),
(21, 12355, 10, 200),
(34, 12356, 10, 20000),
(35, 12357, 10, 12000);

INSERT INTO dbo.Products (id_prod, name, unit, price, description, id_category, import_price, image_url, sale_price) VALUES
(1, N'Bút Bi Thiên Long Xanh', N'Cây bút', 5000, N'Bút bi màu xanh, viết mượt, phù hợp học sinh và văn phòng', 1, 3500, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747100390/0ebbd504-48f7-4a37-99dd-6ad97fbb7767.png', 4500),
(2, N'Bút Chì 2B Cao Cấp', N'Cây', 200, N'Bút chì 2B, nét đậm, dễ gọt, lý tưởng cho vẽ và viết', 1, 100, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747101371/3d769fda-af2d-42f1-ad18-d6d0767f7b3b.png', 180),
(3, N'Vở Campus 200 Trang Kẻ Ngang', N'Quy?n', 15000, N'Vở kẻ ngang cao cấp, 200 trang, giấy dày, không lem mực', 2, 11000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1744425720/hop_4_y1uew4.jpg', NULL),
(5, N'Hộp Bút Màu 24 Màu Cao Cấp', N'Hộp', 45000, N'Hộp bút màu 24 màu, chất lượng cao, màu sắc tươi sáng', 1, 32000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1744425720/hop_4_y1uew4.jpg', 40500),
(6, N'Giấy In A4 500 Tờ', N'Ram', 85000, N'Giấy in A4, 500 tờ, trắng mịn, phù hợp in ấn văn phòng', 4, 70000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747113447/aa99fad3-75e7-4dec-a3d3-a453db5e1891.png', NULL),
(7, N'Bút Dạ Quang Đa Màu', N'Cây', 12000, N'Bút dạ quang nhiều màu, nổi bật, dùng để đánh dấu tài liệu', 1, 8000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1743342765/butdanhdau1dau_e5phts.webp', 10800),
(8, N'Kéo Văn Phòng Cắt Giấy', N'cai', 200000, N'Kéo văn phòng sắc bén, chuyên dùng cắt giấy, bền bỉ', 3, 12000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747125578/2db780ab-14b4-4827-968d-c942d92851b7.png', NULL),
(10, N'Keo Dán Giấy Hộp Nhỏ', N'Chai', 2000, N'Keo dán giấy dạng chai, dính chắc, dễ sử dụng', 5, 200, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747119394/2a54becf-c762-401f-94c9-06ad064fb437.png', 1500),
(12, N'Vở Kẻ Ngang 100 Trang', N'Quyển', 10000, N'Vở kẻ ngang 100 trang, dành cho học sinh, giấy chất lượng', 2, 7000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747060001/4508c2b0-e26c-4f2e-8531-fe4ec1dce6bd.png', NULL),
(13, N'Vở ô li', N'B?', 20000, N'Compa kim loại, bền, chính xác, phù hợp học sinh học hình học', 3, 18000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747059642/6f92ce5d-b92b-47f7-89de-2addd4474a4a.png', NULL),
(15, N'Bìa Còng 5cm Lưu Trữ', N'Cái', 35000, N'Bìa còng 5cm, lưu trữ tài liệu an toàn, chất liệu cứng cáp', 7, 25000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747125002/8ea14567-92e5-4abd-9280-fd6037b95ec5.png', 29750),
(16, N'Bút Lông Viết Bảng', N'Cây', 12000, N'Bút lông viết bảng, mực đậm, dễ xóa, nhiều màu sắc', 1, 8000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1743342762/butdanhdau_j3cuih.webp', 10800),
(17, N'Tập Học Sinh 96 Trang Kẻ Ngang', N'Quy?n', 8000, N'Tập học sinh 96 trang, kẻ ngang, giấy mịn, phù hợp ghi chép', 2, 5500, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747058584/48908f40-667b-4734-a404-d8fa5c6feed7.png', NULL),
(18, N'Hộp Bút Chì Màu 12 Màu', N'H?p', 30000, N'Hộp bút chì màu 12 màu, cao cấp, màu sắc sống động', 1, 22000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747101549/8c9c5b83-dbab-4716-aa7d-58666f0b4774.png', 27000),
(19, N'Giấy Kraft A4 Làm Thủ Công', N'X?p', 30000, N'Giấy kraft A4, dùng làm thủ công, dày dặn, màu nâu tự nhiên', 4, 22000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747113425/f9637df0-130b-4fa6-9126-9f405829f5bc.png', NULL),
(20, N'Bút Mực Gel Màu Đen', N'Cây', 7000, N'Bút gel mực đen, viết mượt, nét thanh, phù hợp ghi chú', 1, 4500, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747100903/dfa64f0d-c8eb-4086-9633-891d1b9edac5.png', 6300),
(21, N'Bút Highlight Cao Cấp', N'cây', 200000, N'Bút highlight cao cấp, màu nổi bật, dùng đánh dấu văn bản', 2, 1000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1743342770/butmuc_ovm7kx.webp', NULL),
(22, N'Thuớc Kẻ Nhựa 30cm', N'cái', 10000, N'Thuớc kẻ nhựa 30cm, bền, có vạch chia chính xác', 3, 100, 'https://res.cloudinary.com/dafqftdol/image/upload/v1744425723/hop_1_an3jrv.jpg', NULL),
(23, N'Tẩy Gôm Học Sinh', N'cái', 10000, N'Tẩy gôm học sinh, sạch, không để lại vết bẩn', 10, 100, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747151508/c2ebe854-e32f-4a62-96fe-6db0120cea31.png', NULL),
(24, N'Bút Xóa Dạng Băng', N'cây', 20000, N'Bút xóa dạng băng, dễ sử dụng, xóa sạch mực', 1, 100, 'https://res.cloudinary.com/dafqftdol/image/upload/v1743342774/butxoa2_-_Copy_kjdngo.webp', 18000),
(25, N'Bút Xóa Dạng Băng Cao Cấp', N'cây', 20000, N'Bút xóa dạng băng cao cấp, tiện lợi, bền bỉ', 1, 100, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747104605/c2b7967a-5154-44c3-bc32-d95c2c69bae3.png', 18000),
(26, N'Máy Tính Học Sinh', N'cái', 2000, N'Máy tính học sinh, nhỏ gọn, phù hợp học sinh tiểu học', 2, 20, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747147953/f6a2281a-0e8e-42fe-8903-fd57a59fdbc7.png', NULL),
(27, N'Lá Xanh Trang Trí', N'cái', 20000, N'Lá xanh trang trí, dùng làm đồ thủ công hoặc trang trí', 5, 2000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1744425895/la_4_ybxc1q.webp', 15000),
(34, N'Máy tính đa năng', N'cái', 4000, N'Hồ dán đa năng, dính tốt trên nhiều chất liệu', 4, 2000, 'https://res.cloudinary.com/dpbfb6hai/image/upload/v1749655071/mcxb26cnasyrxyynjsaw.png', NULL),
(43, N'Máy tính fx 570Vn Plus', N'cái', 5000, N'Băng keo trong 5cm, dính chắc, dùng đóng gói', 2, 2000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1746863761/maytinh-fx5703_duyf4j.webp', NULL),
(45, N'Sổ tay thanh lịch', N'đôi', 10000, N'Găng tay vải đôi, bảo vệ tay, phù hợp làm việc nhẹ', 6, 4000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747062424/d4fb6ebf-da7e-4501-9e57-1c5c6dcf41a0.png', 0),
(57, N'Bút bi Deli', N'cái', 4000, N'Bút bi mực Gel B1 Muji Thân mờ Ngòi 0.5mm Màu Xanh Đen Đỏ', 1, 20000, 'https://res.cloudinary.com/dpbfb6hai/image/upload/v1749734470/rfyl5wvmyktw3ymmxgup.png', 3600),
(60, N'Sổ Deli 200 trang', N'cái', 10000, N'Sổ Deli a5 giá tốt', 2, 4000, 'https://res.cloudinary.com/dpbfb6hai/image/upload/v1749734573/t1ff8kxclhmwzyqlje5o.png', NULL),
(67, N'4 viên AA LR6', N'cái', 3000, N'Kẹp giấy nhỏ, giữ giấy chắc chắn, tiện lợi', 7, 2000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747148178/f6885984-e87f-45ba-bb4c-77c39dbbb299.png', 2550),
(76, N'Pin deli', N'cái', 8000, N'Kim bấm số 10, nhỏ gọn, dùng cho văn phòng', 1, 2000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747148213/400a6d07-f84b-46a1-85cf-88af78ed56bf.png', 7200),
(77, N'Bút Bi Đỏ', N'cái', 5000, N'Bút bi đỏ, viết mượt, phù hợp ghi chú và sửa bài', 2, 2000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747099908/63a759bd-5b17-42b0-909b-773e1710a1ac.png', NULL),
(85, N'Giấy Note 3x3cm', N'cái', 7000, N'Giấy note 3x3cm, nhiều màu, tiện lợi ghi chú nhanh', 7, 3000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747113130/d88a15bc-d811-4691-8561-19de0c2297ed.png', 5950),
(90, N'Lưỡi dao rọc giấy', N'cái', 6000, N'Dụng cụ gọt bút chì, nhỏ gọn, sắc bén', 1, 2000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747125880/148f04a0-11de-4a0f-b9ef-2d48028491f7.png', 5400),
(96, N'Ổ điện đa năng', N'cái', 10000, N'Băng keo hai mặt, dính chắc, dùng trong thủ công', 3, 900, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747125707/4e79f702-99ab-4318-927c-7ef77818af9f.png', NULL),
(124, N'Ngòi chì', N'cái', 2000, N'Phong bì A4, đựng tài liệu, chất liệu giấy bền', 2, 2000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747123385/7792833e-39c5-40eb-b5d2-bd9b798e9ffc.png', NULL),
(145, N'Đinh Ghim Văn Phòng', N'cái', 2000, N'Đinh ghim văn phòng, nhỏ, dùng với bảng ghim', 2, 200, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747123421/c8009803-adc2-4b48-b5f4-251657aec170.png', NULL),
(234, N'Hộp Đựng Bút Nhựa', N'cái', 15000, N'Hộp đựng bút nhựa, gọn nhẹ, tiện lợi cho học sinh', 2, 2000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747121233/6ad3f6e5-a052-47d5-99b9-b716236f616a.png', NULL),
(270, N'Túi đựng đồ dùng học tập', N'cái', 4000, N'Thuớc dẻo 20cm, mềm dẻo, dễ mang theo', 2, 9000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747121551/c091a79b-c746-45e1-a6b5-11b6ff5f328f.png', NULL),
(560, N'Ba lô đa năng', N'cái', 20000, N'Mực đóng dấu màu xanh, đậm, bền màu, dùng cho văn phòng', 3, 45000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747117691/84d856c4-8e29-4912-8942-bb3054fd6b6d.png', NULL),
(678, N'Bộ Dụng Cụ Học Tập', N'cái', 25000, N'Bộ dụng cụ học tập, đầy đủ, tiện lợi cho học sinh', 4, 4000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747117767/39af63e5-d14c-49b0-a6d4-1842fb4e911a.png', NULL),
(679, N'Giấy In Ảnh A4', N'cái', 15000, N'Giấy in ảnh A4, chất lượng cao, in ảnh sắc nét', 1, 1000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747113425/f9637df0-130b-4fa6-9126-9f405829f5bc.png', 13500),
(12345, N'Bộ Dụng Cụ Vẽ Kỹ Thuật', N'cái', 30000, N'Bộ dụng cụ vẽ kỹ thuật, chuyên dụng, phù hợp học sinh kỹ thuật', 2, 20000, 'https://res.cloudinary.com/dafqftdol/image/upload/v1747115440/af3d31b8-e3a6-4582-a30b-27aa0544a394.png', NULL),
(12346, N'Bút chì siêu bền', N'cái', 20000, N'Bút chì vĩnh cửu với công nghệ hiện đại, nét bút đẹp, dễ viết', 3, 20000, 'https://res.cloudinary.com/dpbfb6hai/image/upload/v1749733405/xmqbq5powpalwkk37db1.png', NULL),
(12354, N'Keo dán giấy Tmark', N'cái', 23000, N'Keo gián giấy Tmark - Giải pháp dán giấy hiệu quả và an toàn', 5, 23000, 'https://res.cloudinary.com/dpbfb6hai/image/upload/v1749733592/oeuhuq8wbjtyufewrry5.png', NULL),
(12355, N'Vở ô li loại dày', N'cái', 10000, N'Vở ô li 200 trang, chất giấy dày, thích hợp cho bé', 2, 200, 'https://res.cloudinary.com/dpbfb6hai/image/upload/v1749733657/jecxpme0scbqwqgij6mz.png', NULL),
(12356, N'Túi đựng đồ', N'cái', 25000, N'Túi đựng đồ nghề dành cho kỹ thuật', 7, 20000, 'https://res.cloudinary.com/dpbfb6hai/image/upload/v1749733719/mavumbmlizipftegeeid.png', NULL),
(12357, N'Máy tính 90fx', N'cái', 130000, N'Máy tính cầm tay 90fx - phù hợp cho học sinh, sinh viên. dễ sử dụng, tiện lợi', 8, 12000, 'https://res.cloudinary.com/dpbfb6hai/image/upload/v1749733773/odevmrb427iiopxeb8wy.png', NULL);

INSERT INTO dbo.Promotion (id_promotion, start_date, end_date, description) VALUES
(1, '2025-05-01', '2025-05-31', N'Khuyen mãi 1'),
(3, '2025-04-01', '2025-07-31', N'Khuyen mãi 3'),
(4, '2025-05-15', '2025-05-22', N'Khuyen mãi 4'),
(5, '2025-05-15', '2025-05-22', N'Khuyen mãi 5'),
(6, '2025-05-15', '2025-05-22', N'Khuyen mãi 6'),
(7, '2025-06-03', '2025-06-10', N'Khuyen mai 7');

INSERT INTO dbo.Promotion_detail (id_promotion, id_prod, discount_percent) VALUES
(1, 1, 10),
(1, 2, 15),
(3, 5, 25),
(3, 6, 30),
(4, 1, 10),
(5, 1, 10),
(6, 7, 15),
(7, 1, 10);

INSERT INTO dbo.Warehouse (id_warehouse, name, address, phone) VALUES
(1, N'Kho 1', N'11 Nguyen Ðình Chieu, Ða Kao, Quan 1, TP HCM', '0123456789');

INSERT INTO dbo.Warehouse_Product (id_warehouse, id_prod, quantity) VALUES
(1, 1, 533),
(1, 2, 602),
(1, 3, 400),
(1, 5, 198),
(1, 6, 147),
(1, 7, 347),
(1, 8, 250),
(1, 10, 60),
(1, 12, 60),
(1, 13, 197),
(1, 15, 298),
(1, 16, 30),
(1, 17, 30),
(1, 18, 194),
(1, 19, 59),
(1, 20, 10),
(1, 21, 50),
(1, 22, 60),
(1, 23, 20),
(1, 24, 50),
(1, 25, 70),
(1, 26, 178),
(1, 27, 600),
(1, 34, 400),
(1, 43, 49),
(1, 45, 600),
(1, 57, 20),
(1, 60, 200),
(1, 67, 19),
(1, 76, 200),
(1, 77, 35),
(1, 85, 20),
(1, 90, 30),
(1, 96, 200),
(1, 124, 300),
(1, 145, 20),
(1, 234, 199),
(1, 270, 20),
(1, 560, 17),
(1, 678, 19),
(1, 679, 39),
(1, 12345, 397),
(1, 12346, 20),
(1, 12354, 200),
(1, 12355, 10),
(1, 12356, 10),
(1,