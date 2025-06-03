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

-- Thêm Admin
INSERT INTO dbo.Admin (id_ad, fullname, address, phone, email)
VALUES (1, N'Nguyễn Văn Admin', N'123 Đường Láng, TP.HCM', '0909123456', 'admin@officehub.com');

-- Thêm nhân viên
INSERT INTO dbo.Employees (id_emp, fullname, address, phone, salary, email, status)
VALUES (1, N'Trần Thị Nhân Viên', N'456 Nguyễn Trãi, TP.HCM', '0912345678', 7000000, 'employee1@officehub.com', 1);

-- Thêm tài khoản Admin
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at)
VALUES (1, 'admin', 'admin123', NULL, 1, 'Admin', 1, GETDATE());

-- Thêm tài khoản nhân viên
INSERT INTO dbo.Accounts (id_account, username, password, id_emp, id_ad, role, is_active, created_at)
VALUES (2, 'employee1', 'emp123', 1, NULL, 'Employee', 1, GETDATE());