from PyQt5.QtWidgets import QStackedWidget, QMainWindow, QApplication, QPushButton, QLabel, QVBoxLayout, QWidget, \
    QMessageBox, QTableWidgetItem
import sys
from PyQt5.QtCore import pyqtSignal, Qt

from admin_page import Ui_MainWindow
from run_log import LoginWindow

from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout, QTableWidgetItem


class AdminWindow(QMainWindow):
    def __init__(self):
        super(AdminWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        self.ui.icon_only.hide()

        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.kho_stacked.setCurrentIndex(1)

        self.ui.table_sanpham.setColumnWidth(0,8)
        self.ui.table_sanpham.setColumnWidth(1,150)
        self.ui.table_sanpham.setColumnWidth(2, 70)
        self.ui.table_sanpham.setColumnWidth(3, 70)
        self.ui.table_sanpham.setColumnWidth(4, 70)
        self.ui.table_sanpham.setColumnWidth(5, 100)
        self.ui.table_sanpham.setColumnWidth(6, 150)
        self.ui.table_danhmuc.setColumnWidth(0,90)
        self.ui.table_danhmuc.setColumnWidth(1, 600)
        self.ui.table_search.setColumnWidth(0, 10)
        self.ui.table_search.setColumnWidth(1, 165)
        self.ui.table_search.setColumnWidth(2, 80)
        self.ui.table_search.setColumnWidth(3, 80)
        self.ui.table_search.setColumnWidth(4, 80)
        self.ui.table_search.setColumnWidth(5, 100)
        self.ui.table_search.setColumnWidth(6, 150)
        self.ui.table_danhmuc.setColumnWidth(0, 90)
        self.ui.table_danhmuc.setColumnWidth(1, 600)
        self.ui.table_danhmuc.setColumnWidth(2, 150)
        self.ui.tb_kho_1.setColumnWidth(0,240)
        self.ui.tb_kho_1.setColumnWidth(1, 280)
        self.ui.tb_kho_1.setColumnWidth(2, 210)

        self.ui.tb_kho_2.setColumnWidth(0, 240)
        self.ui.tb_kho_2.setColumnWidth(1, 280)
        self.ui.tb_kho_2.setColumnWidth(2, 210)

        self.ui.table_nhanvien.setColumnWidth(0,55)
        self.ui.table_nhanvien.setColumnWidth(1,160)
        self.ui.table_nhanvien.setColumnWidth(2,160)
        self.ui.table_nhanvien.setColumnWidth(3,110)
        self.ui.table_nhanvien.setColumnWidth(4,80)
        self.ui.table_nhap.setColumnWidth(0,100)
        self.ui.table_nhap.setColumnWidth(1,150)
        self.ui.table_nhap.setColumnWidth(2,200)
        self.ui.table_nhap.setColumnWidth(3,150)
        self.ui.table_nhap.setColumnWidth(4,150)
        self.ui.table_nhap.setColumnWidth(5,130)
        self.ui.table_khuyenmai.setColumnWidth(0,100)
        self.ui.table_khuyenmai.setColumnWidth(1, 250)
        self.ui.table_khuyenmai.setColumnWidth(4, 150)


        load_data_to_table(self.ui.table_sanpham)
        load_data_to_table_2(self.ui.table_danhmuc)
        load_data_kho_1(self.ui.tb_kho_1)
        load_data_kho_2(self.ui.tb_kho_2)
        load_employee_data(self.ui.table_nhanvien)
        load_data_to_search_table(self.ui.table_search)
        load_data_to_table_nhap(self.ui.table_nhap)
        load_data_to_table_khuyenmai(self.ui.table_khuyenmai)

        self.ui.table_sanpham.verticalHeader().setVisible(False)
        self.ui.table_khuyenmai.verticalHeader().setVisible(False)
        self.ui.table_danhmuc.verticalHeader().setVisible(False)
        self.ui.tb_kho_1.verticalHeader().setVisible(False)
        self.ui.tb_kho_2.verticalHeader().setVisible(False)
        self.ui.table_nhanvien.verticalHeader().setVisible(False)
        self.ui.table_search.verticalHeader().setVisible(False)
        self.ui.table_nhap.verticalHeader().setVisible(False)
        self.ui.ql_nhap_btn.clicked.connect(self.on_ql_nhap)

        self.ui.product_btn_1.clicked.connect(self.on_product_btn_1)
        self.ui.warehouse_btn_1.clicked.connect(self.on_warehouse_btn_1)
        self.ui.emp_btn_1.clicked.connect(self.on_emp_btn_1)
        self.ui.statistics_btn_1.clicked.connect(self.on_statistics_btn_1)
        self.ui.promotion_btn_1.clicked.connect(self.on_promotion_btn_1)
        self.ui.ql_danh_muc.clicked.connect(self.on_ql_danhmuc)
        self.ui.ql_kho.clicked.connect(self.on_ql_kho)
        self.ui.kho1_btn.clicked.connect(self.on_kho_1)
        self.ui.kho2_btn.clicked.connect(self.on_kho_2)

        self.ui.product_btn_2.clicked.connect(self.on_product_btn_2)
        self.ui.warehouse_btn_2.clicked.connect(self.on_warehouse_btn_2)
        self.ui.emp_btn_2.clicked.connect(self.on_emp_btn_2)
        self.ui.statistic_btn_2.clicked.connect(self.on_statistic_btn_2)
        self.ui.promotion_btn_2.clicked.connect(self.on_promotion_btn_2)

        self.ui.Search.clicked.connect(self.on_search_btn_clicked)
        self.ui.Account.clicked.connect(self.on_user_btn_clicked)

        self.ui.product_btn_2.setChecked(True)

        self.ui.logo_label = QLabel("Stationery Store")
        self.ui.logo_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        self.ui.header_layout = self.ui.widget.layout()
        self.ui.header_layout.insertWidget(1, self.ui.logo_label)



    def on_search_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        search_text = self.ui.Search_input.text().strip()
        if search_text:
            self.ui.label_15.setText(search_text)

    def on_user_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(5)

    def on_stackedWidget_curentChanged(self, index):
        btn_list = self.ui.icon_only.findChildren(QPushButton) \
                   + self.ui.Full_menu.findChildren(QPushButton)
        for btn in btn_list:
            if index in [5, 6]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)
                btn.setChecked(True)

    def on_ql_danhmuc(self):
        self.ui.kho_stacked.setCurrentIndex(1)
        self.ui.ql_kho.setChecked(False)
        self.ui.ql_nhap_btn.setChecked(False)
        self.ui.ql_danh_muc.setChecked(True)

    def on_ql_nhap(self):
        self.ui.kho_stacked.setCurrentIndex(2)
        self.ui.ql_kho.setChecked(False)
        self.ui.ql_danh_muc.setChecked(False)
        self.ui.ql_nhap_btn.setChecked(True)

    def on_ql_kho(self):
        self.ui.kho_stacked.setCurrentIndex(0)
        self.ui.ql_danh_muc.setChecked(False)
        self.ui.ql_nhap_btn.setChecked(False)
        self.ui.ql_kho.setChecked(True)

    def on_kho_1(self):
        self.ui.kho_widget.setCurrentIndex(0)

    def on_kho_2(self):
        self.ui.kho_widget.setCurrentIndex(1)

    def on_product_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_product_btn_2(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_warehouse_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_warehouse_btn_2(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_emp_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_emp_btn_2(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_statistics_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_statistic_btn_2(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_promotion_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def on_promotion_btn_2(self):
        self.ui.stackedWidget.setCurrentIndex(4)


def load_data_to_table_nhap(table):
    data = [
        ("P01", "Z02", "Nguyễn Văn a", "10-03-2025 12:00", "1,400,900"),
        ("C37", "090", "Lê Thị b", "11-03-2025 00:00", "200,000"),
        ("d d d", "10", "Đỗ Xuân c", "12-03-2025 06:00", "690,000"),
    ]

    table.setRowCount(len(data))  # Đặt số dòng

    for row, (id_, emp_id, emp_name, date, total_price) in enumerate(data):
        table.setItem(row, 0, QTableWidgetItem(id_))
        table.setItem(row, 1, QTableWidgetItem(emp_id))
        table.setItem(row, 2, QTableWidgetItem(emp_name))
        table.setItem(row, 3, QTableWidgetItem(date))
        table.setItem(row, 4, QTableWidgetItem(total_price))

        # Tạo widget chứa nút "Xem chi tiết"
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)

        btn_detail = QPushButton("Xem chi tiết")
        btn_detail.setStyleSheet("background-color: #2196F3; color: white; border-radius: 5px; padding: 2px;")

        layout.addWidget(btn_detail)
        widget.setLayout(layout)

        # Thêm widget vào cột "Chi tiết"
        table.setCellWidget(row, 5, widget)


# Hàm để thêm dữ liệu và nút vào bảng
def load_data_to_table(table):
    data = [
        ("SP001", "Bút bi xanh", 100, 5000, 3000, "Bút viết trơn"),
        ("SP002", "Tập 100 trang", 50, 12000, 8000, "Tập vở học sinh"),
        ("SP003", "Keo dán giấy", 30, 7000, 4000, "Keo dán tốt"),
        ("SP004", "Thước kẻ 30cm", 80, 10000, 7000, "Thước kẻ nhựa"),
    ]

    table.setRowCount(len(data))  # Đặt số dòng

    for row, (id_, name, quantity, price, cost, desc) in enumerate(data):
        table.setItem(row, 0, QTableWidgetItem(id_))
        table.setItem(row, 1, QTableWidgetItem(name))
        table.setItem(row, 2, QTableWidgetItem(str(quantity)))
        table.setItem(row, 3, QTableWidgetItem(str(price)))
        table.setItem(row, 4, QTableWidgetItem(str(cost)))
        table.setItem(row, 5, QTableWidgetItem(desc))

        # Tạo widget chứa nút bấm
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)

        # Nút Sửa
        btn_edit = QPushButton("Sửa")
        btn_edit.setStyleSheet("background-color: #2196F3; color: white; border-radius: 5px; padding: 2px;")
        btn_edit.clicked.connect(lambda _, r=row: edit_item(r))

        # Nút Xóa
        btn_delete = QPushButton("Xóa")
        btn_delete.setStyleSheet("background-color: #FF5722; color: white; border-radius: 5px; padding: 2px;")
        btn_delete.clicked.connect(lambda _, r=row: delete_item(table, r))

        # Thêm vào layout
        layout.addWidget(btn_edit)
        layout.addWidget(btn_delete)
        widget.setLayout(layout)

        # Thêm widget vào cột "Chỉnh sửa"
        table.setCellWidget(row, 6, widget)

def load_data_to_table_khuyenmai(table):
    # Cập nhật dữ liệu khuyến mãi (5 dòng, năm 2025, tên mới)
    data = [
        (17, "Giảm giá đặc biệt", "07-01-2025", "07-02-2025", "Đang diễn ra"),
        (23, "Flash Sale", "09-02-2025", "09-03-2025", "Sắp diễn ra"),
        (24, "Ưu đãi khách hàng VIP", "10-03-2025", "12-04-2025", "Đang diễn ra"),
        (25, "Mua 1 tặng 1", "11-04-2025", "11-05-2025", "Sắp diễn ra"),
        (27, "Khuyến mãi hè", "12-05-2025", "13-06-2025", "Sắp diễn ra"),
    ]

    table.setRowCount(len(data))  # Đặt số dòng
    table.setColumnCount(6)  # Số cột: ID, Tên KM, Từ ngày, Đến ngày, Trạng thái, Chỉnh sửa
    table.setHorizontalHeaderLabels(["ID", "Tên khuyến mãi", "Từ ngày", "Đến ngày", "Trạng thái", "Chỉnh sửa"])

    for row, (id_, name, start_date, end_date, status) in enumerate(data):
        table.setItem(row, 0, QTableWidgetItem(str(id_)))  # ID
        table.setItem(row, 1, QTableWidgetItem(name))  # Tên KM
        table.setItem(row, 2, QTableWidgetItem(start_date))  # Từ ngày
        table.setItem(row, 3, QTableWidgetItem(end_date))  # Đến ngày
        table.setItem(row, 4, QTableWidgetItem(status))  # Trạng thái

        # Tạo widget chứa hai nút
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)

        # Nút Sửa
        btn_edit = QPushButton("Sửa")
        btn_edit.setStyleSheet("background-color: #2196F3; color: white; border-radius: 5px; padding: 2px;")
        btn_edit.clicked.connect(lambda _, r=row: edit_item(r))

        # Nút Xóa
        btn_delete = QPushButton("Xóa")
        btn_delete.setStyleSheet("background-color: #FF5722; color: white; border-radius: 5px; padding: 2px;")
        btn_delete.clicked.connect(lambda _, r=row: delete_item(table, r))

        # Thêm vào layout
        layout.addWidget(btn_edit)
        layout.addWidget(btn_delete)
        widget.setLayout(layout)

        # Thêm widget vào cột "Chỉnh sửa"
        table.setCellWidget(row, 5, widget)

def load_data_to_search_table(table):
    data = [
        ("SP007", "Bút lông xanh", 100, 5000, 3000, "Bút viết trơn"),
        ("SP008", "Bút lông đỏ", 80, 10000, 7000, "Bút viết trơn"),
    ]

    table.setRowCount(len(data))  # Đặt số dòng

    for row, (id_, name, quantity, price, cost, desc) in enumerate(data):
        table.setItem(row, 0, QTableWidgetItem(id_))
        table.setItem(row, 1, QTableWidgetItem(name))
        table.setItem(row, 2, QTableWidgetItem(str(quantity)))
        table.setItem(row, 3, QTableWidgetItem(str(price)))
        table.setItem(row, 4, QTableWidgetItem(str(cost)))
        table.setItem(row, 5, QTableWidgetItem(desc))

        # Tạo widget chứa nút bấm
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)

        # Nút Sửa
        btn_edit = QPushButton("Sửa")
        btn_edit.setStyleSheet("background-color: #2196F3; color: white; border-radius: 5px; padding: 2px;")
        btn_edit.clicked.connect(lambda _, r=row: edit_item(r))

        # Nút Xóa
        btn_delete = QPushButton("Xóa")
        btn_delete.setStyleSheet("background-color: #FF5722; color: white; border-radius: 5px; padding: 2px;")
        btn_delete.clicked.connect(lambda _, r=row: delete_item(table, r))

        # Thêm vào layout
        layout.addWidget(btn_edit)
        layout.addWidget(btn_delete)
        widget.setLayout(layout)

        # Thêm widget vào cột "Chỉnh sửa"
        table.setCellWidget(row, 6, widget)

def load_employee_data(table):
    """
    Load dữ liệu vào bảng cho danh sách nhân viên gồm:
    ID, Họ và tên, Địa chỉ, Số điện thoại, Lương, Chỉnh sửa (Sửa/Xóa).
    """
    data = [
        ("NV001", "Nguyễn Văn A", "Hà Nội", "0912345678", 15000000),
        ("NV002", "Trần Thị B", "Hải Phòng", "0987654321", 12000000),
        ("NV003", "Lê Văn C", "Đà Nẵng", "0934567890", 10000000),
        ("NV004", "Phạm Thị D", "TP. Hồ Chí Minh", "0978123456", 17000000),
    ]

    table.setRowCount(len(data))  # Đặt số dòng

    for row, (id_, name, address, phone, salary) in enumerate(data):
        table.setItem(row, 0, QTableWidgetItem(id_))  # ID Nhân viên
        table.setItem(row, 1, QTableWidgetItem(name))  # Họ và tên
        table.setItem(row, 2, QTableWidgetItem(address))  # Địa chỉ
        table.setItem(row, 3, QTableWidgetItem(phone))  # Số điện thoại
        table.setItem(row, 4, QTableWidgetItem(str(salary)))  # Lương

        # Tạo widget chứa nút bấm
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)

        # Nút Sửa
        btn_edit = QPushButton("Sửa")
        btn_edit.setStyleSheet("background-color: #2196F3; color: white; border-radius: 5px; padding: 2px;")
        btn_edit.clicked.connect(lambda _, r=row: edit_item(r))

        # Nút Xóa
        btn_delete = QPushButton("Xóa")
        btn_delete.setStyleSheet("background-color: #FF5722; color: white; border-radius: 5px; padding: 2px;")
        btn_delete.clicked.connect(lambda _, r=row: delete_item(table, r))

        # Thêm vào layout
        layout.addWidget(btn_edit)
        layout.addWidget(btn_delete)
        widget.setLayout(layout)

        # Thêm widget vào cột "Chỉnh sửa"
        table.setCellWidget(row, 5, widget)
# Hàm xử lý khi nhấn nút Sửa
def edit_item(row):
    print(f"Sửa sản phẩm ở dòng {row}")

# Hàm xử lý khi nhấn nút Xóa
def delete_item(table, row):
    table.removeRow(row)
    print(f"Đã xóa sản phẩm ở dòng {row}")

def load_data_to_table_2(table):
    data = [
        ("SP001", "Bút bi xanh"),
        ("SP002", "Tập 100 trang"),
        ("SP003", "Keo dán giấy"),
        ("SP004", "Thước kẻ 30cm"),
    ]

    table.setColumnCount(3)  # Chỉ có 3 cột: ID, Tên sản phẩm, Chỉnh sửa
    table.setRowCount(len(data))

    for row, (id_, name) in enumerate(data):
        table.setItem(row, 0, QTableWidgetItem(id_))
        table.setItem(row, 1, QTableWidgetItem(name))

        # Tạo nút Sửa
        btn_edit = QPushButton("Sửa")
        btn_edit.setStyleSheet("background-color: #2196F3; color: white; border-radius: 5px; padding: 2px;")
        btn_edit.clicked.connect(lambda _, r=row: edit_item(r))  # Sử dụng lambda để truyền row vào hàm

        # Tạo nút Xóa
        btn_delete = QPushButton("Xóa")
        btn_delete.setStyleSheet("background-color: #FF5722; color: white; border-radius: 5px; padding: 2px;")
        btn_delete.clicked.connect(lambda _, r=row: delete_item(table, r))  # Truyền row vào hàm xóa

        # Đặt hai nút vào một widget
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        layout.addWidget(btn_edit)
        layout.addWidget(btn_delete)
        widget.setLayout(layout)

        # Đặt widget vào cột 3 (cột chứa nút)
        table.setCellWidget(row, 2, widget)


def load_data_kho_1(table):
    """
    Load dữ liệu vào bảng cho Kho 1 với 3 cột: Warehouse ID, Product ID, Số lượng tồn.
    """
    data = [
        ("SP001", 100),
        ("SP002", 50),
        ("SP003", 30),
        ("SP004", 80),
    ]

    table.setRowCount(len(data))  # Đặt số dòng

    for row, (product_id, quantity) in enumerate(data):
        table.setItem(row, 0, QTableWidgetItem("SRQ30"))  # ID Kho 1
        table.setItem(row, 1, QTableWidgetItem(product_id))  # Mã sản phẩm
        table.setItem(row, 2, QTableWidgetItem(str(quantity)))  # Số lượng tồn

def load_data_kho_2(table):
    """
    Load dữ liệu vào bảng cho Kho 2 với 3 cột: Warehouse ID, Product ID, Số lượng tồn.
    """
    data = [
        ("SP005", 120),
        ("SP006", 60),
        ("SP007", 40),
        ("SP008", 25),
    ]

    table.setRowCount(len(data))  # Đặt số dòng

    for row, (product_id, quantity) in enumerate(data):
        table.setItem(row, 0, QTableWidgetItem("OPM75"))  # ID Kho 2
        table.setItem(row, 1, QTableWidgetItem(product_id))  # Mã sản phẩm
        table.setItem(row, 2, QTableWidgetItem(str(quantity)))  # Số lượng tồn


if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("style.qss", "r", encoding="utf-8") as style_file:
        style_str = style_file.read()

    app.setStyleSheet(style_str)
    main_app = AdminWindow()
    main_app.show()
    sys.exit(app.exec_())