import traceback
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from src.modules.admin.events.add_import_handlers import ImportHandler
from src.modules.admin.views.statistic import StatisticWindow
from src.modules.admin.ui.ui_py.admin import Ui_MainWindow
from src.modules.admin.data.employee_data import load_employee_data
from src.modules.admin.data.import_data import load_data_to_table_nhap
from src.modules.admin.data.product_data import load_data_to_sanPham_tb
from src.modules.admin.data.category_data import load_data_to_danhMuc_tb
from src.modules.admin.data.warehouse_data import load_data_to_warehouse_table
from src.modules.admin.data.promotion_data import load_promotion_data
from src.modules.admin.data.bill_data import load_bill_data, load_employees_to_combobox
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from src.modules.admin.events.add_category_handlers import CategoryHandler
from src.modules.admin.events.add_employee_handlers import EmployeeHandler
from src.modules.admin.events.add_product_handlers import ProductHandler
from src.modules.admin.events.warehouse_detail_handlers import WarehouseHandler
from src.modules.admin.events.import_detail_handlers import setup_import_events
from src.modules.admin.dialog.add_employee_dialog import AddEmployeeDialog
from src.modules.admin.dialog.add_product_dialog import AddProductDialog
from src.database.DAO.common.AccountDetailDAO import AccountDetailDAO
from src.modules.admin.data.account_data import AccountDetailData
from src.database.connection import create_connection
from src.modules.admin.events.add_promotion_handlers import PromotionHandler
from src.modules.admin.data.product_data import load_products_to_combobox
from src.modules.admin.events.inventory_adjust_handler import InventoryAdjustHandler
import os

class AdminWindow(QMainWindow):
    def __init__(self, account_id=None):
        super(AdminWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        print(f"AdminWindow initialized with account_id: {account_id}")
        self.current_account_id = account_id
        self.db_connection = create_connection()
        self.account_detail_dao = AccountDetailDAO(self.db_connection)
        self.account_detail_data = AccountDetailData(self.account_detail_dao)

        self.setup_tables()
        self.ui.icon_only.hide()

        self.load_data()
        self.setup_connections()

        self.import_handler = ImportHandler(self)
        self.import_handler.set_table_phieu_nhap(self.ui.table_nhap)

        self.ui.save_btn.clicked.connect(self.save_account_info)
        self.account_detail_data.current_account_id = account_id

        self.setup_logo()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.statistic_window = StatisticWindow()
        self.ui.stackedWidget.addWidget(self.statistic_window)
        self.category_handler = CategoryHandler(self)
        self.promotion_handler = PromotionHandler(self)
        self.employee_handler = EmployeeHandler(self)
        self.product_handler = ProductHandler(self)
        self.warehouse_handler = WarehouseHandler()
        self.inventory_adjust_handler = InventoryAdjustHandler(self)
        self.setup_events()

        self.load_user_data()

        self.ui.hoten_lline.setReadOnly(True)
        self.ui.phonenum_line.setReadOnly(True)
        self.ui.email_line.setReadOnly(True)
        self.ui.addr_line.setReadOnly(True)
        self.ui.chucvu_line.setReadOnly(True)
        self.ui.username_line.setReadOnly(True)
        self.ui.password_line.setReadOnly(True)

        load_employees_to_combobox(self.ui.cbb_tennhanvien)
        self.ui.cbb_tennhanvien.currentIndexChanged.connect(self.load_bills)

    def send_email(self):
        """
        Mở trình duyệt để soạn email gửi đến email của bạn
        """
        email = "n22dccn089@student.ptithcm.edu.vn"
        subject = "Liên hệ từ OFFICEHUB"
        body = "Xin chào,\n\nTôi muốn liên hệ với bạn về...\n"
        mailto_url = QUrl(f"mailto:{email}?subject={subject}&body={body}")
        QDesktopServices.openUrl(mailto_url)
        print(f"Opened mailto URL: {mailto_url.toString()}")

    def load_user_data(self):
        print(f"Loading user data with account_id: {self.current_account_id}")
        if self.current_account_id:
            success = self.account_detail_data.load_user_data(
                self.current_account_id,
                self.ui.hoten_lline,
                self.ui.phonenum_line,
                self.ui.email_line,
                self.ui.addr_line,
                self.ui.chucvu_line,
                self.ui.username_line,
                self.ui.password_line
            )
            if success:
                print("User data loaded successfully")
            else:
                print("Failed to load user data")
        else:
            print("Không thể tải dữ liệu: current_account_id là None")

    def toggle_readonly(self, line_edit, button):
        """Toggle the read-only state of a QLineEdit and update button state."""
        is_readonly = line_edit.isReadOnly()
        line_edit.setReadOnly(not is_readonly)
        button.setChecked(not is_readonly)
        if not is_readonly:
            line_edit.setFocus()

    def toggle_password_visibility(self):
        """Toggle password visibility for password_line."""
        if self.ui.xempass_btn.isChecked():
            self.ui.password_line.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.ui.password_line.setEchoMode(QtWidgets.QLineEdit.Password)

    def open_add_category(self):
        success, category_id, category_name = self.category_handler.show_add_category_dialog()
        if success:
            self.update_category_list()  # Chỉ reload bảng danh mục

    def open_warehouse_detail(self):
        result = self.warehouse_handler.show_warehouse_detail_dialog()
        if result:
            self.update_warehouse_list()  # Chỉ reload bảng kho

    def open_inventory_adjust(self):
        """Mở dialog chỉnh sửa số lượng tồn kho."""
        success = self.inventory_adjust_handler.show_inventory_adjust_dialog()
        if success:
            self.update_warehouse_list()  # Cập nhật bảng kho sau khi chỉnh sửa tồn kho

    def open_add_employee(self):
        dialog = AddEmployeeDialog(self)
        dialog.setWindowModality(Qt.ApplicationModal)
        result = dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            try:
                self.update_employee_list()
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self, "Lỗi", f"Cập nhật danh sách nhân viên thất bại: {e}"
                )

    def open_add_product_dialog(self):
        try:
            dialog = AddProductDialog(self)
            result = dialog.exec_()
            if result == QtWidgets.QDialog.Accepted:
                self.update_product_list()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi khi mở dialog thêm sản phẩm: {str(e)}")

    def open_add_promotion(self):
        try:
            success, promotion_data = self.promotion_handler.show_add_promotion_dialog()
            if success:
                self.load_promotions()  # Đã có reload bảng khuyến mãi
                QMessageBox.information(self, "Thành công", "Thêm khuyến mãi mới thành công!")
        except Exception as e:
            print(f"Lỗi khi mở dialog thêm khuyến mãi: {str(e)}")
            traceback.print_exc()

    def open_add_bill(self):
        QMessageBox.information(self, "Thông báo", "Chức năng thêm hóa đơn đang được phát triển!")

    def open_add_import(self):
        success = self.import_handler.show_add_import_dialog()
        if success:
            self.update_import_list()

    def setup_events(self):
        setup_import_events(self)

    def load_initial_data(self):
        self.on_tab_changed(0)

    def refresh_all_data(self):
        try:
            print("Đang cập nhật tất cả dữ liệu...")
            self.update_product_list()
            self.update_category_list()
            self.update_warehouse_list()
            self.update_employee_list()
            self.update_import_list()
            self.load_promotions()
            self.load_bills()
            print("Đã cập nhật tất cả dữ liệu thành công")
        except Exception as e:
            import traceback
            print(f"Lỗi khi cập nhật dữ liệu: {str(e)}")
            print(traceback.format_exc())

    def update_product_list(self):
        try:
            print("Đang cập nhật bảng sản phẩm...")
            self.ui.table_sanpham.setRowCount(0)
            load_data_to_sanPham_tb(self.ui.table_sanpham)
            print("Đã cập nhật bảng sản phẩm")
        except Exception as e:
            print(f"Lỗi khi cập nhật bảng sản phẩm: {str(e)}")

    def update_category_list(self):
        try:
            print("Đang cập nhật bảng danh mục...")
            self.ui.table_danhmuc.setRowCount(0)
            load_data_to_danhMuc_tb(self.ui.table_danhmuc)
            print("Đã cập nhật bảng danh mục")
        except Exception as e:
            print(f"Lỗi khi cập nhật bảng danh mục: {str(e)}")

    def update_warehouse_list(self):
        try:
            print("Đang cập nhật bảng kho...")
            self.ui.tb_kho_1.setRowCount(0)
            self.ui.tb_kho_2.setRowCount(0)
            load_data_to_warehouse_table(self.ui.tb_kho_1)
            print("Đã cập nhật bảng kho")
        except Exception as e:
            print(f"Lỗi khi cập cập nhật bảng kho: {str(e)}")

    def update_employee_list(self):
        try:
            print("Đang cập nhật bảng nhân viên...")
            self.ui.table_nhanvien.setRowCount(0)
            load_employee_data(self.ui.table_nhanvien)
            print("Đã cập nhật bảng nhân viên")
        except Exception as e:
            print(f"Lỗi khi cập nhật bảng nhân viên: {str(e)}")

    def update_import_list(self):
        try:
            print("Đang cập nhật bảng phiếu nhập...")
            self.ui.table_nhap.setRowCount(0)
            load_data_to_table_nhap(self.ui.table_nhap)
            print("Đã cập nhật bảng phiếu nhập")
        except Exception as e:
            print(f"Lỗi khi cập nhật bảng phiếu nhập: {str(e)}")

    def load_promotions(self):
        try:
            print("Đang cập nhật bảng khuyến mãi...")
            self.ui.table_khuyenmai.setRowCount(0)
            load_promotion_data(self.ui.table_khuyenmai, self)
            print("Đã cập nhật bảng khuyến mãi")
        except Exception as e:
            print(f"Lỗi khi cập nhật bảng khuyến mãi: {str(e)}")

    def load_bills(self):
        try:
            print("Đang cập nhật bảng hóa đơn...")
            self.ui.table_bill.setRowCount(0)
            load_bill_data(self.ui.table_bill, self)
            print("Đã cập nhật bảng hóa đơn")
        except Exception as e:
            print(f"Lỗi khi cập nhật bảng hóa đơn: {str(e)}")

    def on_tab_changed(self, index):
        try:
            print(f"Đang chuyển sang tab {index}")
            if index == 0:
                self.update_product_list()
            elif index == 1:
                self.update_warehouse_list()
                self.update_import_list()
                self.update_category_list()
            elif index == 2:
                self.update_employee_list()
            elif index == 4:
                self.load_promotions()
            elif index == 5:
                self.load_bills()
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu cho tab {index}: {str(e)}")

    def setup_tables(self):
        def set_column_ratios(table, ratios):
            table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
            total_width = table.viewport().width()
            for col, ratio in enumerate(ratios):
                width = int(total_width * ratio)
                table.setColumnWidth(col, width)

        self.ui.table_sanpham.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.ui.table_sanpham.horizontalHeader().setStretchLastSection(True)
        set_column_ratios(self.ui.table_sanpham, [0.08, 0.25, 0.07, 0.10, 0.10, 0.25, 0.15])

        self.ui.table_danhmuc.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.ui.table_danhmuc.horizontalHeader().setStretchLastSection(True)
        set_column_ratios(self.ui.table_danhmuc, [0.20, 0.60, 0.20])

        self.ui.table_nhap.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.ui.table_nhap.horizontalHeader().setStretchLastSection(True)
        set_column_ratios(self.ui.table_nhap, [0.11, 0.17, 0.23, 0.17, 0.17, 0.15])

        self.ui.table_bill.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.ui.table_bill.horizontalHeader().setStretchLastSection(True)
        set_column_ratios(self.ui.table_bill, [0.10, 0.20, 0.20, 0.15, 0.20, 0.15])

        self.ui.tb_kho_1.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.ui.tb_kho_1.horizontalHeader().setStretchLastSection(True)
        set_column_ratios(self.ui.tb_kho_1, [0.7, 0.3])

        self.ui.table_nhanvien.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.ui.table_nhanvien.horizontalHeader().setStretchLastSection(True)
        set_column_ratios(self.ui.table_nhanvien, [0.02, 0.13, 0.13, 0.17, 0.12, 0.12, 0.15, 0.15])

        self.ui.table_khuyenmai.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.ui.table_khuyenmai.horizontalHeader().setStretchLastSection(True)
        set_column_ratios(self.ui.table_khuyenmai, [0.10, 0.25, 0.15, 0.15, 0.15, 0.20])

        tables = [
            self.ui.table_sanpham, self.ui.table_khuyenmai, self.ui.table_danhmuc,
            self.ui.tb_kho_1, self.ui.tb_kho_2, self.ui.table_nhanvien,
            self.ui.table_bill, self.ui.table_nhap
        ]
        for table in tables:
            table.verticalHeader().setVisible(False)

        self.ui.table_sanpham.viewport().installEventFilter(self)
        self.ui.table_khuyenmai.viewport().installEventFilter(self)
        self.ui.table_danhmuc.viewport().installEventFilter(self)
        self.ui.tb_kho_1.viewport().installEventFilter(self)
        self.ui.tb_kho_2.viewport().installEventFilter(self)
        self.ui.table_nhanvien.viewport().installEventFilter(self)
        self.ui.table_bill.viewport().installEventFilter(self)
        self.ui.table_nhap.viewport().installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.Resize:
            tables = [
                self.ui.table_sanpham, self.ui.table_khuyenmai, self.ui.table_danhmuc,
                self.ui.tb_kho_1, self.ui.tb_kho_2, self.ui.table_nhanvien,
                self.ui.table_bill, self.ui.table_nhap
            ]
            for table in tables:
                if source == table.viewport():
                    QtCore.QTimer.singleShot(0, self.setup_tables)
                    break
        return super().eventFilter(source, event)

    def load_data(self):
        load_data_to_sanPham_tb(self.ui.table_sanpham)
        load_data_to_danhMuc_tb(self.ui.table_danhmuc)
        load_data_to_warehouse_table(self.ui.tb_kho_1)
        load_employee_data(self.ui.table_nhanvien)
        load_data_to_table_nhap(self.ui.table_nhap)
        load_promotion_data(self.ui.table_khuyenmai, self)
        load_bill_data(self.ui.table_bill, self)

    def setup_connections(self):
        self.ui.product_btn_1.clicked.connect(self.on_product_btn_1)
        self.ui.warehouse_btn_1.clicked.connect(self.on_warehouse_btn_1)
        self.ui.emp_btn_1.clicked.connect(self.on_emp_btn_1)
        self.ui.statistics_btn_1.clicked.connect(self.on_statistics_btn_1)
        self.ui.ql_danh_muc.clicked.connect(self.on_ql_danhmuc)
        self.ui.ql_kho.clicked.connect(self.on_ql_kho)
        self.ui.ql_nhap_btn.clicked.connect(self.on_ql_nhap)
        self.ui.add_category_btn.clicked.connect(self.open_add_category)
        self.ui.add_employee_btn.clicked.connect(self.open_add_employee)
        self.ui.thongtinkho_btn.clicked.connect(self.open_warehouse_detail)
        self.ui.add_promotion_btn.clicked.connect(self.open_add_promotion)
        self.ui.product_btn_2.clicked.connect(self.on_product_btn_2)
        self.ui.warehouse_btn_2.clicked.connect(self.on_warehouse_btn_2)
        self.ui.emp_btn_2.clicked.connect(self.on_emp_btn_2)
        self.ui.statistic_btn_2.clicked.connect(self.on_statistic_btn_2)
        self.ui.orpromotion_btn_1.clicked.connect(self.on_promotion_btn_1)
        self.ui.promotion_btn_2.clicked.connect(self.on_promotion_btn_2)

        self.ui.bill_btn_1.clicked.connect(self.on_bill)
        self.ui.bill_btn_2.clicked.connect(self.on_bill)
        self.ui.Account.clicked.connect(self.show_account_info)
        self.ui.them_phieu_nhap_btn.clicked.connect(self.open_add_import)

        # Kết nối nút chỉnh sửa số lượng tồn kho
        if hasattr(self.ui, 'chinh_so_luong_btn'):
            self.ui.chinh_so_luong_btn.clicked.connect(self.open_inventory_adjust)

        # Kết nối nút tìm kiếm sản phẩm
        if hasattr(self.ui, 'search_product_btn'):
            self.ui.search_product_btn.clicked.connect(self.search_products)

        # Kết nối nút tìm kiếm nhân viên
        if hasattr(self.ui, 'search_nhanvien_btn'):
            self.ui.search_nhanvien_btn.clicked.connect(self.search_employees)

        # Kết nối nút liên hệ với phương thức send_email
        if hasattr(self.ui, 'lien_he_btn_1'):
            self.ui.lien_he_btn_1.clicked.connect(self.send_email)
        if hasattr(self.ui, 'lien_he_btn_2'):
            self.ui.lien_he_btn_2.clicked.connect(self.send_email)

        # Kết nối nút "Thêm hóa đơn" nếu có trong UI
        if hasattr(self.ui, 'add_bill_btn'):
            self.ui.add_bill_btn.clicked.connect(self.open_add_bill)

        self.ui.product_btn_2.setChecked(True)

        if hasattr(self.ui, 'logout_btn'):
            self.ui.logout_btn.clicked.connect(self.show_logout_confirmation)

        # Connect edit buttons to toggle read-only state
        self.ui.edit_hoten.clicked.connect(lambda: self.toggle_readonly(self.ui.hoten_lline, self.ui.edit_hoten))
        self.ui.edit_phonenum.clicked.connect(
            lambda: self.toggle_readonly(self.ui.phonenum_line, self.ui.edit_phonenum))
        self.ui.edit_email.clicked.connect(lambda: self.toggle_readonly(self.ui.email_line, self.ui.edit_email))
        self.ui.edit_addr.clicked.connect(lambda: self.toggle_readonly(self.ui.addr_line, self.ui.edit_addr))

        # Connect xempass_btn to toggle password visibility
        self.ui.xempass_btn.clicked.connect(self.toggle_password_visibility)

    def show_logout_confirmation(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Xác nhận đăng xuất")
        msg_box.setText("Bạn có chắc chắn muốn đăng xuất không?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)

        yes_button = msg_box.button(QMessageBox.Yes)
        yes_button.setText("Có")
        no_button = msg_box.button(QMessageBox.No)
        no_button.setText("Không")

        result = msg_box.exec_()

        if result == QMessageBox.Yes:
            self.logout()

    def logout(self):
        self.close()
        from src.modules.login.view.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()

    def setup_logo(self):
        self.ui.logo_label = QLabel("Stationery Store")
        self.ui.logo_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        self.ui.header_layout = self.ui.widget.layout()

    def on_bill(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        self.load_bills()

    def show_account_info(self):
        print(f"Showing account info for account_id: {self.current_account_id}")
        self.ui.stackedWidget.setCurrentIndex(7)
        self.load_user_data()

    def save_account_info(self):
        if not self.current_account_id:
            QMessageBox.warning(self, "Cảnh báo", "Không có thông tin tài khoản để lưu!")
            return

        # Validate fields before saving
        hoten = self.ui.hoten_lline.text().strip()
        phonenum = self.ui.phonenum_line.text().strip()
        email = self.ui.email_line.text().strip()
        addr = self.ui.addr_line.text().strip()
        username = self.ui.username_line.text().strip()
        password = self.ui.password_line.text().strip()

        if not all([hoten, phonenum, email, addr, username, password]):
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
            return

        try:
            success = self.account_detail_data.update_user_data(
                hoten_line=self.ui.hoten_lline,
                phonenum_line=self.ui.phonenum_line,
                email_line=self.ui.email_line,
                addr_line=self.ui.addr_line,
                username_line=self.ui.username_line,
                password_line=self.ui.password_line
            )
            if success:
                QMessageBox.information(self, "Thành công", "Cập nhật thông tin tài khoản thành công!")
                # Reset all fields to read-only and uncheck edit buttons
                self.ui.hoten_lline.setReadOnly(True)
                self.ui.phonenum_line.setReadOnly(True)
                self.ui.email_line.setReadOnly(True)
                self.ui.addr_line.setReadOnly(True)
                self.ui.edit_hoten.setChecked(False)
                self.ui.edit_phonenum.setChecked(False)
                self.ui.edit_email.setChecked(False)
                self.ui.edit_addr.setChecked(False)
            else:
                QMessageBox.warning(self, "Cảnh báo", "Không thể cập nhật thông tin tài khoản!")
                print("Update failed, check account_detail_data.update_user_data logs")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi khi cập nhật: {str(e)}")
            print(f"Error in save_account_info: {str(e)}")
            traceback.print_exc()

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
        self.update_import_list()

    def on_ql_kho(self):
        self.ui.kho_stacked.setCurrentIndex(0)
        self.ui.ql_danh_muc.setChecked(False)
        self.ui.ql_nhap_btn.setChecked(False)
        self.ui.ql_kho.setChecked(True)

    def on_product_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.update_product_list()

    def on_product_btn_2(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.update_product_list()

    def on_warehouse_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.update_warehouse_list()
        self.update_category_list()

    def on_warehouse_btn_2(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.update_warehouse_list()
        self.update_category_list()

    def on_emp_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.update_employee_list()

    def on_emp_btn_2(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.update_employee_list()

    def on_statistics_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.statistic_window))

    def on_statistic_btn_2(self):
        self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.statistic_window))

    def on_promotion_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        self.load_promotions()

    def on_promotion_btn_2(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        self.load_promotions()

    def search_products(self):
        """Xử lý tìm kiếm sản phẩm"""
        from src.modules.admin.data.product_data import search_products
        keyword = self.ui.line_search_product.text().strip()
        search_products(self.ui.table_sanpham, keyword)

    def search_employees(self):
        """Xử lý tìm kiếm nhân viên"""
        from src.modules.admin.data.employee_data import search_employees
        keyword = self.ui.line_search_nhanvien.text().strip()
        search_employees(self.ui.table_nhanvien, keyword)

