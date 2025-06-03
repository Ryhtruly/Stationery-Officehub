import os

import pyodbc
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QAction, QMenu, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, \
    QSpinBox, QDialog, QTextEdit, QMessageBox, QLineEdit, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QDesktopServices
from src.modules.employee.ui.ui_py.employee import Ui_MainWindow
from src.modules.employee.view.product_view import ProductManagementView
from src.modules.employee.view.product_view import cart_data
from src.modules.employee.dialog.information_dialog import AppInfoDialog
from src.modules.employee.dialog.bill_detail_dialog import BillDetailDialog
from src.modules.employee.data.customer_data import load_data_to_customer_tb, get_customer_by_phone
from src.modules.employee.events.add_customer_handler import CustomerHandler
from src.database.DAO.common.AccountDetailDAO import AccountDetailDAO
from src.modules.admin.data.account_data import AccountDetailData
from src.database.connection import create_connection
from src.modules.login.view.login_window import LoginWindow
from src.database.DAO.common.BillDAO import BillDAO
from src.database.DAO.common.BillDetailDAO import BillDetailDAO
from src.database.DAO.common.CardDAO import CardDAO
from src.database.DAO.admin.CategoryDAO import CategoryDAO
from src.modules.employee.data.product_data import ProductData
from src.modules.employee.data.bill_data import load_bill_data
from src.modules.employee.data.promotion_data import load_promotion_data

class ClickableLabel(QLabel):
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(ClickableLabel, self).__init__(parent)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def mousePressEvent(self, event):
        self.clicked.emit()
        super(ClickableLabel, self).mousePressEvent(event)

class CustomerPhoneDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nhập Số Điện Thoại Khách Hàng")
        self.setModal(True)

        layout = QVBoxLayout()
        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Nhập số điện thoại")
        layout.addWidget(self.phone_input)

        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("Xác nhận")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Hủy")
        self.cancel_button.clicked.connect(self.reject)
        self.skip_button = QPushButton("Bỏ qua")
        self.skip_button.clicked.connect(self.skip)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.skip_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.skipped = False

    def get_phone(self):
        return self.phone_input.text().strip()

    def skip(self):
        self.skipped = True
        self.accept()

class CheckoutDialog(QDialog):
    def __init__(self, parent, customer_info, total, discounted_total, cart_items):
        super().__init__(parent)
        self.setWindowTitle("Hóa Đơn Thanh Toán")
        self.setModal(True)
        self.setMinimumWidth(500)

        layout = QVBoxLayout()

        header_label = QLabel("HÓA ĐƠN THANH TOÁN")
        header_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)

        customer_frame = QFrame()
        customer_frame.setFrameShape(QFrame.StyledPanel)
        customer_layout = QVBoxLayout(customer_frame)
        customer_layout.addWidget(QLabel(f"Khách hàng: {customer_info.get('fullname', 'Khách hàng')}"))
        customer_layout.addWidget(QLabel(f"Số điện thoại: {customer_info.get('phone', 'Không có')}"))
        customer_layout.addWidget(QLabel(f"Hạng: {customer_info.get('rank', 'Không có')}"))
        layout.addWidget(customer_frame)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Sản phẩm", "Số lượng", "Đơn giá", "Thành tiền"])
        self.table.setRowCount(len(cart_items))
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.setStyleSheet("QTableWidget { font-size: 12px; }")
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

        for row, item in enumerate(cart_items):
            self.table.setItem(row, 0, QTableWidgetItem(item["ten"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(item["so_luong"])))
            self.table.setItem(row, 2, QTableWidgetItem(f"{item['gia']:,} VNĐ"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{item['gia'] * item['so_luong']:,} VNĐ"))

        layout.addWidget(self.table)

        summary_frame = QFrame()
        summary_layout = QVBoxLayout(summary_frame)
        summary_layout.addWidget(QLabel(f"Tổng tiền ban đầu: {total:,} VNĐ"))
        discount = total - discounted_total
        summary_layout.addWidget(QLabel(f"Giảm giá: {discount:,} VNĐ"))
        summary_layout.addWidget(QLabel(f"Tổng tiền thanh toán: {discounted_total:,} VNĐ"))
        layout.addWidget(summary_frame)

        button_layout = QHBoxLayout()
        confirm_button = QPushButton("Thanh Toán")
        confirm_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px;")
        confirm_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Hủy")
        cancel_button.setStyleSheet("background-color: #f44336; color: white; padding: 5px;")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

class EmployeeWindow(QtWidgets.QMainWindow):
    def __init__(self, account_id=None):
        super(EmployeeWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.current_account_id = account_id
        self.db_connection = create_connection()
        self.account_detail_dao = AccountDetailDAO(self.db_connection)
        self.account_detail_data = AccountDetailData(self.account_detail_dao)
        self.account_detail_data.current_account_id = account_id
        self.bill_dao = BillDAO(self.db_connection)
        self.bill_detail_dao = BillDetailDAO(self.db_connection)
        self.card_dao = CardDAO(self.db_connection)
        self.product_data = ProductData()
        self.categories_dict = self.load_categories()

        if self.current_account_id is None:
            QMessageBox.critical(self, "Lỗi", "Không có thông tin tài khoản. Vui lòng đăng nhập lại!")
            self.close()
            self.login_window = LoginWindow()
            self.login_window.show()
            return

        print(f"Initializing EmployeeWindow with account_id: {self.current_account_id}")

        self.ui.icon_only.hide()
        self.setup_tables()
        self.load_data()
        self.customer_handler = CustomerHandler(self)
        self.connect_customer_events()
        self.product_view = ProductManagementView()
        product_layout = QtWidgets.QVBoxLayout(self.ui.sheet_sanPham)
        product_layout.setContentsMargins(0, 0, 0, 0)
        product_layout.addWidget(self.product_view)
        self.load_products()
        self.setup_cart_widget()
        cart_data.set_cart_updated_callback(self.update_cart_widget)
        self.setup_info_button()
        self.connect_buttons()
        self.setup_filter_menu()
        self.setup_home_image_widgets()
        self.connect_edit_buttons()
        self.ui.stackedWidget.setCurrentWidget(self.ui.home_widget)
        self.ui.home_nbtn_1.setChecked(True)
        self.ui.home_btn_2.setChecked(True)
        self.load_user_data()
        self.set_employee_name_to_label()

        self.center()

    def center(self):
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        size = self.geometry()
        y_position = (screen.height() - size.height()) // 2 - 50
        self.move(
            (screen.width() - size.width()) // 2,
            y_position
        )

    def load_categories(self):
        try:
            categories = CategoryDAO.get_all_categories()
            categories_dict = {str(category.id_category): category.name for category in categories}
            print(f"Loaded categories: {categories_dict}")
            return categories_dict
        except Exception as e:
            print(f"Error loading categories: {str(e)}")
            return {}

    def set_employee_name_to_label(self):
        """
        Lấy tên nhân viên từ hoten_line và hiển thị lên lb_ten_nv
        """
        if not hasattr(self.ui, 'hoten_line'):
            print("Cannot set employee name: hoten_line not found in UI")
            return

        if not hasattr(self.ui, 'lb_ten_nv'):
            print("Cannot set employee name: lb_ten_nv not found in UI")
            return

        employee_name = self.ui.hoten_line.text().strip()
        if employee_name:
            self.ui.lb_ten_nv.setText(employee_name)
            print(f"Employee name set to lb_ten_nv: {employee_name}")
        else:
            self.ui.lb_ten_nv.setText("Không xác định")
            print("Employee name not found in hoten_line, set to 'Không xác định'")

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

    def load_products(self):
        self.product_view.clear_products()
        products = self.product_data.get_all_products()
        for product in products:
            self.product_view.add_product_item(
                product_id=product["id"],
                name=product["ten"],
                price=product["display_price"],
                description=product["mo_ta"],
                image_path=product["hinh_anh"]
            )
        print(f"Displayed {len(products)} products")

    def search_products(self):
        self.change_page(self.ui.product_widget)

        keyword = self.ui.lineEdit.text()
        if keyword:
            self.product_view.clear_products()
            products = self.product_data.search_products(keyword)
            for product in products:
                self.product_view.add_product_item(
                    product_id=product["id"],
                    name=product["ten"],
                    price=product["display_price"],
                    description=product["mo_ta"],
                    image_path=product["hinh_anh"]
                )
            print(f"Displayed {len(products)} products matching keyword '{keyword}'")
        else:
            QtWidgets.QMessageBox.information(self, "Thông báo", "Vui lòng nhập từ khóa tìm kiếm")
            self.load_products()

    def sort_products_by_name(self, ascending=True):
        self.product_view.clear_products()
        products = sorted(
            self.product_data.get_all_products(),
            key=lambda x: x["ten"].lower(),
            reverse=not ascending
        )
        for product in products:
            self.product_view.add_product_item(
                product_id=product["id"],
                name=product["ten"],
                price=product["display_price"],
                description=product["mo_ta"],
                image_path=product["hinh_anh"]
            )
        print(f"Displayed {len(products)} products sorted by name {'ascending' if ascending else 'descending'}")

    def sort_products_by_price(self, ascending=True):
        self.product_view.clear_products()
        products = sorted(
            self.product_data.get_all_products(),
            key=lambda x: x["display_price"],
            reverse=not ascending
        )
        for product in products:
            self.product_view.add_product_item(
                product_id=product["id"],
                name=product["ten"],
                price=product["display_price"],
                description=product["mo_ta"],
                image_path=product["hinh_anh"]
            )
        print(f"Displayed {len(products)} products sorted by price {'ascending' if ascending else 'descending'}")

    def filter_products_by_category(self, category_id):
        self.product_view.clear_products()
        products = self.product_data.filter_by_category(category_id)
        for product in products:
            self.product_view.add_product_item(
                product_id=product["id"],
                name=product["ten"],
                price=product["display_price"],
                description=product["mo_ta"],
                image_path=product["hinh_anh"]
            )
        print(f"Displayed {len(products)} products for category ID {category_id}")

    def setup_info_button(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        infomation_icon = os.path.join(base_dir, "employee", "ui_design", "icon", "info-2-xxl.png")
        self.info_button = QPushButton(self.ui.home_widget)
        self.info_button.setIcon(QIcon(infomation_icon))
        self.info_button.setText(" Thông tin thêm")
        self.info_button.setGeometry(650, 20, 150, 30)
        self.info_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 150, 255, 0.3);
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 10px;
                border: 1.5px solid rgba(255, 255, 255, 0.4);
                border-style: outset;
                border-width: 1px;
            }
            QPushButton:hover {
                background-color: rgba(30, 170, 255, 0.5);
                border: 1.5px solid rgba(255, 255, 255, 0.6);
            }
            QPushButton:pressed {
                background-color: rgba(0, 120, 200, 0.4);
                border: 1.5px solid rgba(255, 255, 255, 0.3);
                padding-top: 9px;
                padding-left: 17px;
            }
        """)
        self.info_button.clicked.connect(self.show_app_info)
        self.info_button.raise_()
        self.info_button.show()

    def load_user_data(self):
        if self.current_account_id:
            if hasattr(self.ui, 'hoten_line') and hasattr(self.ui, 'phonenum_line'):
                success = self.account_detail_data.load_user_data(
                    self.current_account_id,
                    self.ui.hoten_line,
                    self.ui.phonenum_line,
                    self.ui.email_line,
                    self.ui.addr_line,
                    self.ui.chucvu_line,
                    self.ui.username_line,
                    self.ui.password_line
                )
                if not success:
                    print("Failed to load user data")
            else:
                print("UI does not have fields to display user data")
        else:
            print("Cannot load data: current_account_id is None")

    def setup_tables(self):
        def set_column_ratios(table, ratios):
            table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
            total_width = table.viewport().width()
            for col, ratio in enumerate(ratios):
                width = int(total_width * ratio)
                table.setColumnWidth(col, width)

        self.ui.table_khachhang.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.ui.table_khachhang.horizontalHeader().setStretchLastSection(True)
        set_column_ratios(self.ui.table_khachhang, [0.05, 0.31, 0.17, 0.17, 0.18, 0.12])
        self.ui.table_khachhang.verticalHeader().setVisible(False)
        self.ui.table_khachhang.viewport().installEventFilter(self)

        self.ui.table_khuyenmai_2.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.ui.table_khuyenmai_2.horizontalHeader().setStretchLastSection(True)
        set_column_ratios(self.ui.table_khuyenmai_2, [0.05, 0.31, 0.17, 0.17, 0.18, 0.12])
        self.ui.table_khuyenmai_2.verticalHeader().setVisible(False)
        self.ui.table_khuyenmai_2.viewport().installEventFilter(self)

        self.ui.table_bill.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.ui.table_bill.horizontalHeader().setStretchLastSection(True)
        set_column_ratios(self.ui.table_bill, [0.05, 0.31, 0.17, 0.17, 0.18, 0.12])
        self.ui.table_bill.verticalHeader().setVisible(False)
        self.ui.table_bill.viewport().installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.Resize:
            tables = [self.ui.table_khachhang, self.ui.table_bill, self.ui.table_khuyenmai_2]
            for table in tables:
                if source == table.viewport():
                    QtCore.QTimer.singleShot(0, self.setup_tables)
                    break
        return super().eventFilter(source, event)

    def load_data(self):
        load_data_to_customer_tb(self.ui.table_khachhang)
        self.load_bills()
        self.load_promotions()

    def load_bills(self):
        """
        Tải danh sách hóa đơn của nhân viên đang đăng nhập
        """
        try:
            # Lấy id_emp từ account_id
            id_emp = self.bill_dao.get_employee_id_from_account_id(self.current_account_id)
            if id_emp is None:
                print(f"Không thể lấy id_emp từ account_id: {self.current_account_id}")
                QMessageBox.critical(self, "Lỗi", "Không thể xác định nhân viên. Vui lòng đăng nhập lại!")
                return

            print(f"Loading bills for employee with id_emp: {id_emp}")

            print("Đang cập nhật bảng hóa đơn...")
            self.ui.table_bill.setRowCount(0)
            load_bill_data(self.ui.table_bill, id_emp, self)
            print("Đã cập nhật bảng hóa đơn")
        except Exception as e:
            print(f"Lỗi khi cập nhật bảng hóa đơn: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải danh sách hóa đơn: {str(e)}")

    def load_promotions(self):
        """
        Tải danh sách khuyến mãi đang hiện hành
        """
        try:
            print("Đang cập nhật bảng khuyến mãi...")
            self.ui.table_khuyenmai_2.setRowCount(0)
            load_promotion_data(self.ui.table_khuyenmai_2, self)
            print("Đã cập nhật bảng khuyến mãi")
        except Exception as e:
            print(f"Lỗi khi cập nhật bảng khuyến mãi: {str(e)}")

    def connect_buttons(self):
        self.ui.home_nbtn_1.clicked.connect(lambda: self.change_page(self.ui.home_widget))
        self.ui.home_btn_2.clicked.connect(lambda: self.change_page(self.ui.home_widget))
        self.ui.product_btn_1.clicked.connect(lambda: self.change_page(self.ui.product_widget))
        self.ui.product_btn_2.clicked.connect(lambda: self.change_page(self.ui.product_widget))
        self.ui.customer_btn_1.clicked.connect(lambda: self.change_page(self.ui.customer_widget))
        self.ui.cusomer_btn_2.clicked.connect(lambda: self.change_page(self.ui.customer_widget))
        self.ui.lien_he_btn_1.clicked.connect(self.send_email)
        self.ui.lien_he_btn_2.clicked.connect(self.send_email)
        self.ui.huong_dan_btn_1.clicked.connect(lambda: self.change_page(self.ui.page_huong_dan))
        self.ui.huong_dan_btn_2.clicked.connect(lambda: self.change_page(self.ui.page_huong_dan))
        self.ui.orpromotion_btn_1.clicked.connect(lambda: self.change_page(self.ui.search_widget))
        self.ui.promotion_btn_2.clicked.connect(lambda: self.change_page(self.ui.search_widget))
        self.ui.search_btn.clicked.connect(self.search_products)
        self.ui.user_btn.clicked.connect(self.show_account_info)
        self.ui.pushButton_5.clicked.connect(self.close)
        if hasattr(self.ui, 'loc_btn'):
            self.ui.loc_btn.clicked.connect(self.show_filter_menu)
        if hasattr(self.ui, 'logout_btn'):
            self.ui.logout_btn.clicked.connect(self.show_logout_confirmation)

    def show_account_info(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.account)
        self.load_user_data()

    def show_logout_confirmation(self):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Question)
        msg_box.setWindowTitle("Xác nhận đăng xuất")
        msg_box.setText("Bạn có chắc chắn muốn đăng xuất không?")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        msg_box.setDefaultButton(QtWidgets.QMessageBox.No)
        yes_button = msg_box.button(QtWidgets.QMessageBox.Yes)
        yes_button.setText("Có")
        no_button = msg_box.button(QtWidgets.QMessageBox.No)
        no_button.setText("Không")
        result = msg_box.exec_()
        if result == QtWidgets.QMessageBox.Yes:
            self.logout()

    def logout(self):
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()

    def setup_home_image_widgets(self):
        widgets = [self.ui.widget_2, self.ui.widget_4, self.ui.widget_5, self.ui.widget_6]
        labels = [self.ui.label_4, self.ui.label_5, self.ui.label_6, self.ui.label_16]
        for widget in widgets:
            widget.mousePressEvent = lambda event: self.change_page(self.ui.product_widget)
            widget.setCursor(QCursor(Qt.PointingHandCursor))
        for label in labels:
            label.mousePressEvent = lambda event: self.change_page(self.ui.product_widget)

    def show_filter_menu(self):
        self.filter_menu.exec_(self.ui.loc_btn.mapToGlobal(self.ui.loc_btn.rect().bottomLeft()))

    def setup_filter_menu(self):
        self.filter_menu = QMenu(self)

        # Sorting by Name
        name_menu = QMenu("Sắp xếp theo tên", self.filter_menu)
        self.sort_name_asc = QAction("A-Z", self)
        self.sort_name_desc = QAction("Z-A", self)
        name_menu.addAction(self.sort_name_asc)
        name_menu.addAction(self.sort_name_desc)
        self.filter_menu.addMenu(name_menu)

        # Sorting by Price
        price_menu = QMenu("Sắp xếp theo giá", self.filter_menu)
        self.sort_price_asc = QAction("Giá tăng dần", self)
        self.sort_price_desc = QAction("Giá giảm dần", self)
        price_menu.addAction(self.sort_price_asc)
        price_menu.addAction(self.sort_price_desc)
        self.filter_menu.addMenu(price_menu)

        # All Categories Submenu
        all_categories_menu = QMenu("Tất cả danh mục", self.filter_menu)
        show_all_action = QAction("Hiển thị tất cả", self)
        show_all_action.triggered.connect(lambda: self.filter_products_by_category(None))
        all_categories_menu.addAction(show_all_action)
        all_categories_menu.addSeparator()
        for category_id, category_name in self.categories_dict.items():
            action = QAction(category_name, self)
            action.triggered.connect(lambda checked, cid=category_id: self.filter_products_by_category(cid))
            all_categories_menu.addAction(action)
        self.filter_menu.addMenu(all_categories_menu)

        self.sort_name_asc.triggered.connect(lambda: self.sort_products_by_name(True))
        self.sort_name_desc.triggered.connect(lambda: self.sort_products_by_name(False))
        self.sort_price_asc.triggered.connect(lambda: self.sort_products_by_price(True))
        self.sort_price_desc.triggered.connect(lambda: self.sort_products_by_price(False))

    def connect_customer_events(self):
        if hasattr(self.ui, "add_promotion_btn"):
            self.ui.add_promotion_btn.clicked.connect(self.open_add_customer)

    def open_add_customer(self):
        self.customer_handler.show_add_customer_dialog()
        load_data_to_customer_tb(self.ui.table_khachhang)

    def change_page(self, widget):
        self.ui.stackedWidget.setCurrentWidget(widget)
        if widget == self.ui.home_widget:
            self.ui.home_nbtn_1.setChecked(True)
            self.ui.home_btn_2.setChecked(True)
        elif widget == self.ui.product_widget:
            self.ui.product_btn_1.setChecked(True)
            self.ui.product_btn_2.setChecked(True)
        elif widget == self.ui.customer_widget:
            self.ui.customer_btn_1.setChecked(True)
            self.ui.cusomer_btn_2.setChecked(True)

    def setup_cart_widget(self):
        cart_layout = QVBoxLayout(self.ui.thanh_toan_widget)
        cart_layout.setContentsMargins(5, 5, 5, 5)
        cart_title = QLabel("GIỎ HÀNG")
        cart_title.setStyleSheet("text-align: center; font-size: 18px; color: #E0E0E0; font-family: 'Times New Roman', serif;")
        cart_layout.addWidget(cart_title)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
            }
            QScrollBar:vertical {
                border: none;
                background-color: rgba(255, 255, 255, 0.1);
                width: 8px;
                margin: 0px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: rgba(255, 255, 255, 0.4);
                min-height: 30px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: rgba(255, 255, 255, 0.6);
            }
            QScrollBar::handle:vertical:pressed {
                background-color: rgba(255, 255, 255, 0.8);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar:horizontal {
                border: none;
                background-color: rgba(255, 255, 255, 0.1);
                height: 8px;
                margin: 0px;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal {
                background-color: rgba(255, 255, 255, 0.4);
                min-width: 30px;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: rgba(255, 255, 255, 0.6);
            }
            QScrollBar::handle:horizontal:pressed {
                background-color: rgba(255, 255, 255, 0.8);
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
                background: none;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
        """)
        self.cart_items_widget = QWidget()
        self.cart_items_layout = QVBoxLayout(self.cart_items_widget)
        self.cart_items_layout.setAlignment(QtCore.Qt.AlignTop)
        scroll_area.setWidget(self.cart_items_widget)
        cart_layout.addWidget(scroll_area)
        total_layout = QHBoxLayout()
        total_label = QLabel("Tổng tiền:")
        total_label.setStyleSheet("font-weight: bold; color: #E0E0E0;")
        self.total_price_label = QLabel("0 VNĐ")
        self.total_price_label.setStyleSheet("font-weight: bold; color: #FF6F61;")
        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_price_label, alignment=QtCore.Qt.AlignRight)
        cart_layout.addLayout(total_layout)

        self.checkout_button = QPushButton("THANH TOÁN")
        self.checkout_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(212, 163, 115, 0.2);
                color: #E0E0E0;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                font-family: 'Georgia', serif;
                font-size: 12px;
                font-weight: bold;
                padding: 5px 10px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            QPushButton:hover {
                background-color: rgba(212, 163, 115, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.5);
            }
            QPushButton:pressed {
                background-color: rgba(212, 163, 115, 0.6);
                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
            }
            QPushButton:checked {
                background-color: rgba(212, 163, 115, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.7);
                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
            }
        """)
        self.checkout_button.clicked.connect(self.checkout)
        cart_layout.addWidget(self.checkout_button)
        self.update_cart_widget()

    def update_cart_widget(self):
        from functools import partial
        while self.cart_items_layout.count():
            item = self.cart_items_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.cart_items_layout.setContentsMargins(0, 5, 10, 5)
        for item in cart_data.items:
            item_widget = QWidget()
            item_widget.setStyleSheet("""
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                margin: 2px;
            """)
            main_layout = QVBoxLayout(item_widget)
            main_layout.setContentsMargins(4, 4, 4, 4)
            main_layout.setSpacing(2)
            top_widget = QWidget()
            top_layout = QHBoxLayout(top_widget)
            top_layout.setContentsMargins(0, 0, 0, 0)
            top_layout.setSpacing(4)
            name_label = QLabel(item["ten"])
            name_label.setStyleSheet("font-size: 11px; color: #E0E0E0; font-weight: bold; background: transparent;")
            delete_button = QPushButton("×")
            delete_button.setFixedSize(18, 18)
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 82, 82, 0.2);
                    color: white;
                    font-size: 10px;
                    border-radius: 9px;
                    border: 1px solid rgba(255, 82, 82, 0.5);
                }
                QPushButton:hover {
                    background-color: rgba(255, 82, 82, 0.4);
                    border: 1px solid rgba(255, 82, 82, 0.7);
                }
            """)
            delete_func = partial(cart_data.remove_item, item["id"])
            delete_button.clicked.connect(delete_func)
            top_layout.addWidget(name_label)
            top_layout.addStretch()
            top_layout.addWidget(delete_button)
            bottom_widget = QWidget()
            bottom_layout = QHBoxLayout(bottom_widget)
            bottom_layout.setContentsMargins(0, 0, 0, 0)
            bottom_layout.setSpacing(0)
            price_label = QLabel(f"{item['gia']:,} VNĐ")
            price_label.setStyleSheet("color: #FF6F61; padding-right: 2px; font-size: 9px; background: transparent;")
            quantity_widget = QWidget()
            quantity_layout = QHBoxLayout(quantity_widget)
            quantity_layout.setContentsMargins(0, 0, 0, 0)
            quantity_layout.setSpacing(0)
            quantity_spinbox = QSpinBox()
            quantity_spinbox.setMinimum(1)
            quantity_spinbox.setMaximum(100)
            quantity_spinbox.setValue(item["so_luong"])
            quantity_spinbox.setFixedWidth(50)
            quantity_spinbox.setStyleSheet("""
                QSpinBox {
                    font-size: 9px;
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    border-radius: 3px;
                    background-color: rgba(255, 255, 255, 0.1);
                    color: #E0E0E0;
                }
                QSpinBox::up-button, QSpinBox::down-button {
                    background-color: rgba(255, 255, 255, 0.2);
                    border: none;
                }
                QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                    background-color: rgba(255, 255, 255, 0.4);
                }
            """)
            update_quantity_func = partial(cart_data.update_quantity, item["id"])
            quantity_spinbox.valueChanged.connect(update_quantity_func)
            quantity_layout.addWidget(quantity_spinbox)
            bottom_layout.addWidget(price_label)
            bottom_layout.addStretch()
            bottom_layout.addWidget(quantity_widget)
            main_layout.addWidget(top_widget)
            main_layout.addWidget(bottom_widget)
            self.cart_items_layout.addWidget(item_widget)
        self.total_price_label.setText(f"{cart_data.total_price:,} VNĐ")
        self.total_price_label.setStyleSheet("font-size: 10px; font-weight: bold; color: #FF6F61;")

    def validate_product(self, product_id):
        """
        Kiểm tra xem id_prod có tồn tại trong bảng Products không
        """
        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT id_prod
                FROM dbo.Products
                WHERE id_prod = ?
            """
            cursor.execute(query, (product_id,))
            row = cursor.fetchone()
            return row is not None
        except pyodbc.Error as e:
            print(f"Lỗi khi kiểm tra sản phẩm: {str(e)}")
            return False
        finally:
            cursor.close()

    def checkout(self):
        dialog = CustomerPhoneDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Lấy id_emp từ id_account
            id_emp = self.bill_dao.get_employee_id_from_account_id(self.current_account_id)
            if id_emp is None:
                QMessageBox.critical(self, "Lỗi", "Không thể tìm thấy nhân viên tương ứng với tài khoản này!")
                return

            print(f"Checkout with account_id: {self.current_account_id}, mapped to id_emp: {id_emp}")

            # Kiểm tra giỏ hàng
            if not cart_data.items:
                QMessageBox.warning(self, "Lỗi", "Giỏ hàng trống! Vui lòng thêm sản phẩm trước khi thanh toán.")
                return

            print(f"Cart items before checkout: {cart_data.items}")

            # Kiểm tra sản phẩm hợp lệ
            for item in cart_data.items:
                if not self.validate_product(item['id']):
                    QMessageBox.critical(self, "Lỗi", f"Sản phẩm {item['ten']} không tồn tại trong kho!")
                    return
                if item['gia'] <= 0:
                    QMessageBox.critical(self, "Lỗi", f"Sản phẩm {item['ten']} có giá không hợp lệ: {item['gia']} VNĐ!")
                    return
                if not isinstance(item['so_luong'], int) or item['so_luong'] <= 0:
                    QMessageBox.critical(self, "Lỗi", f"Sản phẩm {item['ten']} có số lượng không hợp lệ: {item['so_luong']}")
                    return

            # Bắt đầu giao dịch
            try:
                if dialog.skipped:
                    customer_info = {"fullname": "Khách hàng", "phone": "Không có", "rank": "Không có", "id_cust": None}
                    total = cart_data.total_price
                    discounted_total = total
                    checkout_dialog = CheckoutDialog(self, customer_info, total, discounted_total, cart_data.items)
                    if checkout_dialog.exec_() == QDialog.Accepted:
                        bill_id = self.bill_dao.insert_bill(id_emp, None, discounted_total)
                        if bill_id is None:
                            self.db_connection.rollback()
                            QMessageBox.critical(self, "Lỗi", "Không thể tạo hóa đơn!")
                            return

                        print(f"Created bill with id_bill: {bill_id}")

                        # Chèn chi tiết hóa đơn
                        all_success = True
                        for item in cart_data.items:
                            if not all(key in item for key in ['id', 'so_luong', 'gia', 'ten']):
                                print(f"Dữ liệu không hợp lệ cho sản phẩm: {item}")
                                all_success = False
                                continue
                            try:
                                success = self.bill_detail_dao.insert_bill_detail(
                                    bill_id,
                                    item['id'],
                                    item['so_luong'],
                                    item['gia'],
                                    0  # Không có giảm giá
                                )
                                if not success:
                                    print(f"Không thể chèn chi tiết hóa đơn cho sản phẩm {item['id']} vào hóa đơn {bill_id}")
                                    all_success = False
                            except pyodbc.Error as e:
                                error_msg = str(e)
                                print(f"Lỗi khi chèn chi tiết hóa đơn cho sản phẩm {item['id']}: {error_msg}")
                                if "Số lượng sản phẩm bán vượt quá tổng tồn kho hiện có" in error_msg:
                                    QMessageBox.critical(self, "Lỗi", f"Sản phẩm {item['ten']} không đủ tồn kho (yêu cầu: {item['so_luong']}).")
                                else:
                                    QMessageBox.critical(self, "Lỗi", f"Lỗi khi chèn chi tiết hóa đơn cho sản phẩm {item['ten']}: {error_msg}")
                                all_success = False

                        if all_success:
                            self.db_connection.commit()
                            QMessageBox.information(self, "Thanh toán thành công", f"Đã thanh toán {discounted_total:,} VNĐ thành công!")
                            bill_dialog = BillDetailDialog(bill_id, self)
                            bill_dialog.exec_()
                            cart_data.clear_cart()
                            self.load_bills()  # Cập nhật bảng hóa đơn
                        else:
                            self.db_connection.rollback()
                            QMessageBox.critical(self, "Lỗi", "Không thể hoàn tất thanh toán. Giao dịch đã bị hủy.")
                else:
                    phone = dialog.get_phone()
                    if phone:
                        customer = get_customer_by_phone(phone, self.db_connection)
                        if customer:
                            rank = customer.get('rank', 'Bronze')
                            discount = self.get_discount_by_rank(rank)
                            total = cart_data.total_price
                            discounted_total = total * (1 - discount)
                            checkout_dialog = CheckoutDialog(self, customer, total, discounted_total, cart_data.items)
                            if checkout_dialog.exec_() == QDialog.Accepted:
                                bill_id = self.bill_dao.insert_bill(id_emp, customer['id_cust'], discounted_total)
                                if bill_id is None:
                                    self.db_connection.rollback()
                                    QMessageBox.critical(self, "Lỗi", "Không thể tạo hóa đơn!")
                                    return

                                print(f"Created bill with id_bill: {bill_id}")

                                # Chèn chi tiết hóa đơn
                                all_success = True
                                for item in cart_data.items:
                                    if not all(key in item for key in ['id', 'so_luong', 'gia', 'ten']):
                                        print(f"Dữ liệu không hợp lệ cho sản phẩm: {item}")
                                        all_success = False
                                        continue
                                    try:
                                        success = self.bill_detail_dao.insert_bill_detail(
                                            bill_id,
                                            item['id'],
                                            item['so_luong'],
                                            item['gia'],
                                            discount
                                        )
                                        if not success:
                                            print(f"Không thể chèn chi tiết hóa đơn cho sản phẩm {item['id']} vào hóa đơn {bill_id}")
                                            all_success = False
                                    except pyodbc.Error as e:
                                        error_msg = str(e)
                                        print(f"Lỗi khi chèn chi tiết hóa đơn cho sản phẩm {item['id']}: {error_msg}")
                                        if "Số lượng sản phẩm bán vượt quá tổng tồn kho hiện có" in error_msg:
                                            QMessageBox.critical(self, "Lỗi", f"Sản phẩm {item['ten']} không đủ tồn kho (yêu cầu: {item['so_luong']}).")
                                        else:
                                            QMessageBox.critical(self, "Lỗi", f"Lỗi khi chèn chi tiết hóa đơn cho sản phẩm {item['ten']}: {error_msg}")
                                        all_success = False

                                if all_success:
                                    self.db_connection.commit()
                                    QMessageBox.information(self, "Thanh toán thành công", f"Đã thanh toán {discounted_total:,} VNĐ thành công!")
                                    bill_dialog = BillDetailDialog(bill_id, self)
                                    bill_dialog.exec_()
                                    cart_data.clear_cart()
                                    self.load_bills()  # Cập nhật bảng hóa đơn
                                else:
                                    self.db_connection.rollback()
                                    QMessageBox.critical(self, "Lỗi", "Không thể hoàn tất thanh toán. Giao dịch đã bị hủy.")
                        else:
                            QMessageBox.information(self, "Thông báo", "Không tìm thấy khách hàng. Tiếp tục thanh toán mà không áp dụng giảm giá.")
                            if QMessageBox.Yes == QMessageBox.question(self, "Xác nhận", f"Xác nhận thanh toán {cart_data.total_price:,} VNĐ?", QMessageBox.Yes | QMessageBox.No):
                                bill_id = self.bill_dao.insert_bill(id_emp, None, cart_data.total_price)
                                if bill_id is None:
                                    self.db_connection.rollback()
                                    QMessageBox.critical(self, "Lỗi", "Không thể tạo hóa đơn!")
                                    return

                                print(f"Created bill with id_bill: {bill_id}")

                                # Chèn chi tiết hóa đơn
                                all_success = True
                                for item in cart_data.items:
                                    if not all(key in item for key in ['id', 'so_luong', 'gia', 'ten']):
                                        print(f"Dữ liệu không hợp lệ cho sản phẩm: {item}")
                                        all_success = False
                                        continue
                                    try:
                                        success = self.bill_detail_dao.insert_bill_detail(
                                            bill_id,
                                            item['id'],
                                            item['so_luong'],
                                            item['gia'],
                                            0  # Không có giảm giá
                                        )
                                        if not success:
                                            print(f"Không thể chèn chi tiết hóa đơn cho sản phẩm {item['id']} vào hóa đơn {bill_id}")
                                            all_success = False
                                    except pyodbc.Error as e:
                                        error_msg = str(e)
                                        print(f"Lỗi khi chèn chi tiết hóa đơn cho sản phẩm {item['id']}: {error_msg}")
                                        if "Số lượng sản phẩm bán vượt quá tổng tồn kho hiện có" in error_msg:
                                            QMessageBox.critical(self, "Lỗi", f"Sản phẩm {item['ten']} không đủ tồn kho (yêu cầu: {item['so_luong']}).")
                                        else:
                                            QMessageBox.critical(self, "Lỗi", f"Lỗi khi chèn chi tiết hóa đơn cho sản phẩm {item['ten']}: {error_msg}")
                                        all_success = False

                                if all_success:
                                    self.db_connection.commit()
                                    QMessageBox.information(self, "Thanh toán thành công", f"Đã thanh toán {cart_data.total_price:,} VNĐ thành công!")
                                    bill_dialog = BillDetailDialog(bill_id, self)
                                    bill_dialog.exec_()
                                    cart_data.clear_cart()
                                    self.load_bills()  # Cập nhật bảng hóa đơn
                                else:
                                    self.db_connection.rollback()
                                    QMessageBox.critical(self, "Lỗi", "Không thể hoàn tất thanh toán. Giao dịch đã bị hủy.")
                    else:
                        QMessageBox.information(self, "Thông báo", "Số điện thoại trống. Tiếp tục mà không áp dụng giảm giá.")
                        if QMessageBox.Yes == QMessageBox.question(self, "Xác nhận", f"Xác nhận thanh toán {cart_data.total_price:,} VNĐ?", QMessageBox.Yes | QMessageBox.No):
                            bill_id = self.bill_dao.insert_bill(id_emp, None, cart_data.total_price)
                            if bill_id is None:
                                self.db_connection.rollback()
                                QMessageBox.critical(self, "Lỗi", "Không thể tạo hóa đơn!")
                                return

                            print(f"Created bill with id_bill: {bill_id}")

                            # Chèn chi tiết hóa đơn
                            all_success = True
                            for item in cart_data.items:
                                if not all(key in item for key in ['id', 'so_luong', 'gia', 'ten']):
                                    print(f"Dữ liệu không hợp lệ cho sản phẩm: {item}")
                                    all_success = False
                                    continue
                                try:
                                    success = self.bill_detail_dao.insert_bill_detail(
                                        bill_id,
                                        item['id'],
                                        item['so_luong'],
                                        item['gia'],
                                        0  # Không có giảm giá
                                    )
                                    if not success:
                                        print(f"Không thể chèn chi tiết hóa đơn cho sản phẩm {item['id']} vào hóa đơn {bill_id}")
                                        all_success = False
                                except pyodbc.Error as e:
                                    error_msg = str(e)
                                    print(f"Lỗi khi chèn chi tiết hóa đơn cho sản phẩm {item['id']}: {error_msg}")
                                    if "Số lượng sản phẩm bán vượt quá tổng tồn kho hiện có" in error_msg:
                                        QMessageBox.critical(self, "Lỗi", f"Sản phẩm {item['ten']} không đủ tồn kho (yêu cầu: {item['so_luong']}).")
                                    else:
                                        QMessageBox.critical(self, "Lỗi", f"Lỗi khi chèn chi tiết hóa đơn cho sản phẩm {item['ten']}: {error_msg}")
                                    all_success = False

                            if all_success:
                                self.db_connection.commit()
                                QMessageBox.information(self, "Thanh toán thành công", f"Đã thanh toán {cart_data.total_price:,} VNĐ thành công!")
                                bill_dialog = BillDetailDialog(bill_id, self)
                                bill_dialog.exec_()
                                cart_data.clear_cart()
                                self.load_bills()  # Cập nhật bảng hóa đơn
                            else:
                                self.db_connection.rollback()
                                QMessageBox.critical(self, "Lỗi", "Không thể hoàn tất thanh toán. Giao dịch đã bị hủy.")
            except pyodbc.Error as e:
                self.db_connection.rollback()
                error_msg = str(e)
                print(f"Lỗi trong quá trình thanh toán: {error_msg}")
                if "Số lượng sản phẩm bán vượt quá tổng tồn kho hiện có" in error_msg:
                    # Lỗi từ trigger, tìm sản phẩm gây lỗi (dựa trên log hoặc xử lý thêm nếu cần)
                    QMessageBox.critical(self, "Lỗi", "Không đủ tồn kho cho một hoặc nhiều sản phẩm trong giỏ hàng.")
                else:
                    QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi trong quá trình thanh toán: {error_msg}")
            except Exception as e:
                self.db_connection.rollback()
                print(f"Lỗi trong quá trình thanh toán: {str(e)}")
                QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi trong quá trình thanh toán: {str(e)}")
        else:
            QMessageBox.information(self, "Hủy", "Quá trình thanh toán đã bị hủy.")

    def get_discount_by_rank(self, rank):
        return self.card_dao.get_discount_by_rank(rank)

    def show_app_info(self):
        dialog = AppInfoDialog(self)
        dialog.exec_()

    def toggle_editable(self, line_edit, edit_button):
        if not line_edit or not edit_button:
            QMessageBox.critical(self, "Lỗi", "Không thể chỉnh sửa: Giao diện không hợp lệ!")
            return
        is_readonly = line_edit.isReadOnly()
        line_edit.setReadOnly(not is_readonly)
        edit_button.setChecked(not is_readonly)
        if not is_readonly:
            line_edit.setFocus()

    def save_changes(self):
        if not self.current_account_id:
            QMessageBox.warning(self, "Cảnh báo", "Không có thông tin tài khoản để lưu!")
            return
        hoten = self.ui.hoten_line.text().strip()
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
                hoten_line=self.ui.hoten_line,
                phonenum_line=self.ui.phonenum_line,
                email_line=self.ui.email_line,
                addr_line=self.ui.addr_line,
                username_line=self.ui.username_line,
                password_line=self.ui.password_line
            )
            if success:
                QMessageBox.information(self, "Thành công", "Cập nhật thông tin tài khoản thành công!")
            else:
                QMessageBox.warning(self, "Cảnh báo", "Không thể cập nhật thông tin tài khoản!")
                print("Update failed, check account_detail_data.update_user_data logs")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi khi cập nhật: {str(e)}")
            print(f"Error in save_changes: {str(e)}")

    def show_password(self):
        if not hasattr(self.ui, 'xem_pass_btn') or not hasattr(self.ui, 'password_line'):
            QMessageBox.critical(self, "Lỗi", "Không thể hiển thị mật khẩu: Giao diện không hợp lệ!")
            return
        if self.ui.xem_pass_btn.isChecked():
            self.ui.password_line.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.ui.password_line.setEchoMode(QtWidgets.QLineEdit.Password)

    def connect_edit_buttons(self):
        if not all(hasattr(self.ui, attr) for attr in [
            'edit_hoten', 'hoten_line', 'edit_phonenum', 'phonenum_line',
            'edit_email', 'email_line', 'edit_addr', 'addr_line',
            'xem_pass_btn', 'save_btn']):
            QMessageBox.critical(self, "Lỗi", "Không thể kết nối các nút chỉnh sửa: Giao diện không đầy đủ!")
            return
        self.ui.edit_hoten.clicked.connect(lambda: self.toggle_editable(self.ui.hoten_line, self.ui.edit_hoten))
        self.ui.edit_phonenum.clicked.connect(lambda: self.toggle_editable(self.ui.phonenum_line, self.ui.edit_phonenum))
        self.ui.edit_email.clicked.connect(lambda: self.toggle_editable(self.ui.email_line, self.ui.edit_email))
        self.ui.edit_addr.clicked.connect(lambda: self.toggle_editable(self.ui.addr_line, self.ui.edit_addr))
        self.ui.xem_pass_btn.clicked.connect(self.show_password)
        self.ui.save_btn.clicked.connect(self.save_all_changes)

    def save_all_changes(self):
        self.save_changes()
        self.ui.hoten_line.setReadOnly(True)
        self.ui.phonenum_line.setReadOnly(True)
        self.ui.email_line.setReadOnly(True)
        self.ui.addr_line.setReadOnly(True)
        self.ui.edit_hoten.setChecked(False)
        self.ui.edit_phonenum.setChecked(False)
        self.ui.edit_email.setChecked(False)
        self.ui.edit_addr.setChecked(False)