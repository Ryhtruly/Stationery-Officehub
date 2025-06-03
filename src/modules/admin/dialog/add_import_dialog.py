from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QPushButton, QWidget, QHBoxLayout

from src.database.DAO.admin.ProductAdminDAO import ProductDAO
from src.modules.admin.ui.ui_py.add_import import Ui_Form
from src.modules.admin.events.add_product_to_import_handler import AddProductToImportHandler
from src.database.DAO.admin.ImportDAO import NhapHangDAO
from src.database.DAO.admin.EmployeeDAO import EmployeeDAO
from src.modules.admin.dialog.add_product_to_import_dialog import AddProductToImportDialog
from src.database.connection import create_connection

class AddImportDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AddImportDialog, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.setWindowTitle("Thêm phiếu nhập hàng")
        self.setModal(True)

        self.product_handler = AddProductToImportHandler(self, self.ui.table_san_pham_pn)

        self.setup_validation()
        self.finished.connect(self.on_dialog_finished)

        self.connect_events()
        self.setup_product_table()

        self.load_employee_data()

        self.product_list = []  # Danh sách sản phẩm đã chọn
        self.new_products = []  # Danh sách sản phẩm mới cần thêm vào Products

        self.generate_new_id()

        self.update_total_amount()

    def generate_new_id(self):
        """
        Tự động tạo ID mới cho phiếu nhập bằng cách lấy ID lớn nhất hiện tại và tăng thêm 1
        """
        try:
            connection = create_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT MAX(id_imp) FROM Import")
            max_id = cursor.fetchone()[0]

            if max_id is None:
                new_id = 1
            else:
                new_id = max_id + 1

            self.ui.line_id.setText(str(new_id))

            cursor.close()
            connection.close()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Không thể tạo ID mới cho phiếu nhập: {str(e)}")

    def load_employee_data(self):
        """
        Load danh sách nhân viên vào combo box
        """
        employee_list = EmployeeDAO.get_all_nhan_vien()

        self.employee_dict = {}

        self.ui.combo_box_ten_nhan_vien.clear()

        for employee in employee_list:
            self.ui.combo_box_ten_nhan_vien.addItem(employee.fullname)
            self.employee_dict[employee.fullname] = employee.id_emp

    def setup_product_table(self):
        def set_column_ratios(table, ratios):
            """Thiết lập tỷ lệ kích thước cho các cột của bảng dựa trên tổng chiều rộng."""
            table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
            total_width = table.viewport().width()
            for col, ratio in enumerate(ratios):
                width = int(total_width * ratio)
                table.setColumnWidth(col, width)
        self.ui.table_san_pham_pn.setColumnCount(8)
        headers = ["ID", "Tên sản phẩm", "Danh mục", "Kho", "Số lượng", "Đơn vị", "Giá nhập", "Chỉnh sửa"]
        self.ui.table_san_pham_pn.setHorizontalHeaderLabels(headers)

        self.ui.table_san_pham_pn.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.ui.table_san_pham_pn.horizontalHeader().setStretchLastSection(True)
        set_column_ratios(self.ui.table_san_pham_pn, [0.08, 0.20, 0.12, 0.12, 0.10, 0.08, 0.15, 0.15])
        self.ui.table_san_pham_pn.setAlternatingRowColors(True)
        self.ui.table_san_pham_pn.viewport().installEventFilter(self)
        self.ui.table_san_pham_pn.verticalHeader().setVisible(False)

    def setup_tables(self):
        """Cập nhật lại kích thước các cột của bảng khi thay đổi kích thước."""

        def set_column_ratios(table, ratios):
            total_width = table.viewport().width()
            for col, ratio in enumerate(ratios):
                width = int(total_width * ratio)
                table.setColumnWidth(col, width)
        set_column_ratios(self.ui.table_san_pham_pn, [0.08, 0.20, 0.12, 0.12, 0.10, 0.08, 0.15, 0.15])

    def eventFilter(self, source, event):
        """Xử lý sự kiện thay đổi kích thước để cập nhật lại tỷ lệ cột."""
        if event.type() == QtCore.QEvent.Resize:
            tables = [
                self.ui.table_san_pham_pn
            ]

            for table in tables:
                if source == table.viewport():
                    QtCore.QTimer.singleShot(0, self.setup_tables)
                    break

        return super().eventFilter(source, event)

    def update_total_amount(self):
        """
        Tính và cập nhật tổng tiền của tất cả các sản phẩm trong danh sách vào ô line_tong_tien
        """
        try:
            total_amount = 0
            for product in self.product_list:
                total_amount += product['total_amount']

            self.ui.line_tong_tien.setText(f"{total_amount:,.2f} VNĐ")

        except Exception as e:
            print(f"Lỗi khi tính tổng tiền: {str(e)}")
            self.ui.line_tong_tien.setText("0.00 VNĐ")

    def get_import_data(self):
        """
        Lấy dữ liệu từ form nhập hàng

        Returns:
            dict: Dữ liệu phiếu nhập
        """
        id_phieu_nhap = self.ui.line_id.text().strip()

        selected_employee_name = self.ui.combo_box_ten_nhan_vien.currentText()
        id_nhan_vien = self.employee_dict.get(selected_employee_name)

        san_pham_list = []
        table = self.ui.table_san_pham_pn

        for row in range(table.rowCount()):
            if table.item(row, 0) is not None:
                id_san_pham = table.item(row, 0).text()  # Cột ID
                ten_san_pham = table.item(row, 1).text()  # Cột Tên sản phẩm
                danh_muc = table.item(row, 2).text()  # Cột Danh mục
                kho = table.item(row, 3).text()  # Cột Kho
                so_luong = int(table.item(row, 4).text())  # Cột Số lượng
                don_vi = table.item(row, 5).text()  # Cột Đơn vị
                gia_nhap = float(table.item(row, 6).text())  # Cột Giá nhập

                san_pham = {
                    'id': id_san_pham,
                    'ten': ten_san_pham,
                    'danh_muc': danh_muc,
                    'kho': kho,
                    'so_luong': so_luong,
                    'don_vi': don_vi,
                    'gia_nhap': gia_nhap
                }
                san_pham_list.append(san_pham)

        import_data = {
            'id_phieu_nhap': id_phieu_nhap,
            'id_nhan_vien': id_nhan_vien,
            'san_pham_list': san_pham_list
        }

        return import_data

    def on_dialog_finished(self, result):
        """Xử lý khi dialog đóng"""
        try:
            self.ui.them_san_pham_pn_btn.clicked.disconnect()
            self.ui.them_btn.clicked.disconnect()
            self.ui.huy_btn.clicked.disconnect()
        except:
            pass

    def setup_validation(self):
        """Thiết lập validation cho các trường nhập liệu"""
        if hasattr(self.ui, 'line_id'):
            self.ui.line_id.setPlaceholderText("Nhập mã phiếu nhập")

        if hasattr(self.ui, 'line_date'):
            self.ui.line_date.setPlaceholderText("Ngày nhập (dd/mm/yyyy)")

        if hasattr(self.ui, 'combo_box_supplier'):
            self.ui.combo_box_supplier.clear()
            self.ui.combo_box_supplier.addItem("Chọn nhà cung cấp")

        # Thêm validator cho ID nhân viên
        if hasattr(self.ui, 'line_id_emp'):
            self.ui.line_id_emp.setPlaceholderText("Nhập ID nhân viên")
            validator = QtGui.QIntValidator()
            self.ui.line_id_emp.setValidator(validator)

    def connect_events(self):
        """Kết nối các sự kiện"""
        self.ui.them_san_pham_pn_btn.clicked.connect(self.add_product_to_import)  # Đảm bảo tên nút là chính xác

        self.ui.them_btn.clicked.connect(self.accept)
        self.ui.huy_btn.clicked.connect(self.reject)


    def add_product_to_import(self):
        """Thêm sản phẩm vào phiếu nhập"""
        dialog = AddProductToImportDialog(self)
        if dialog.exec_():
            product_data = dialog.get_product_data()
            if product_data:
                try:
                    id_prod = int(product_data['id_prod'])
                    if id_prod <= 0:
                        raise ValueError("ID sản phẩm phải lớn hơn 0.")
                except (ValueError, TypeError):
                    QMessageBox.warning(
                        self,
                        "Lỗi",
                        f"ID sản phẩm '{product_data['id_prod']}' không hợp lệ. Vui lòng nhập một số nguyên dương.",
                        QMessageBox.Ok
                    )
                    return

                formatted_product = {
                    'id': str(id_prod),
                    'ten': product_data['name'],
                    'danh_muc': product_data['category_name'],
                    'kho': product_data['warehouse_name'],
                    'so_luong': int(product_data['quantity']),
                    'don_vi': product_data['unit'],
                    'gia_nhap': float(product_data['import_price']),
                    'total_amount': product_data['total_amount']
                }

                self.product_list.append(formatted_product)

                if not ProductDAO.get_product_by_id(str(id_prod)):
                    new_product = {
                        'id': id_prod,
                        'name': product_data['name'],
                        'unit': product_data['unit'],
                        'price': 0,
                        'price_import': float(product_data['import_price']),
                        'description': None,
                        'id_category': product_data['category_id'],
                        'image_url': None
                    }
                    self.new_products.append(new_product)

                row = self.ui.table_san_pham_pn.rowCount()
                self.ui.table_san_pham_pn.insertRow(row)

                self.ui.table_san_pham_pn.setItem(row, 0, QTableWidgetItem(str(id_prod)))
                self.ui.table_san_pham_pn.setItem(row, 1, QTableWidgetItem(product_data['name']))
                self.ui.table_san_pham_pn.setItem(row, 2, QTableWidgetItem(product_data['category_name']))
                self.ui.table_san_pham_pn.setItem(row, 3, QTableWidgetItem(product_data['warehouse_name']))
                self.ui.table_san_pham_pn.setItem(row, 4, QTableWidgetItem(product_data['quantity']))
                self.ui.table_san_pham_pn.setItem(row, 5, QTableWidgetItem(product_data['unit']))
                self.ui.table_san_pham_pn.setItem(row, 6, QTableWidgetItem(product_data['import_price']))

                widget = QWidget()
                layout = QHBoxLayout()
                layout.setContentsMargins(5, 2, 5, 2)

                edit_btn = QPushButton("Chỉnh sửa")
                edit_btn.setStyleSheet("background-color: #2196F3; color: white; border-radius: 5px; padding: 2px;")
                edit_btn.clicked.connect(lambda checked, r=row: self.edit_product(r))

                delete_btn = QPushButton("Xóa")
                delete_btn.setStyleSheet("background-color: #F44336; color: white; border-radius: 5px; padding: 2px;")
                delete_btn.clicked.connect(lambda checked, r=row: self.delete_product(r))

                layout.addWidget(edit_btn)
                layout.addWidget(delete_btn)
                widget.setLayout(layout)
                self.ui.table_san_pham_pn.setCellWidget(row, 7, widget)

                self.update_total_amount()

    def edit_product(self, row):
        """
        Chỉnh sửa sản phẩm trong bảng
        """
        product_data = self.product_list[row]
        dialog = AddProductToImportDialog(self)
        dialog.ui.line_id.setText(product_data['id'])
        dialog.ui.line_name.setText(product_data['ten'])
        dialog.ui.line_unit.setText(product_data['don_vi'])
        dialog.ui.line_soLuong.setText(str(product_data['so_luong']))
        dialog.ui.line_gia_nhap.setText(str(product_data['gia_nhap']))
        for i in range(dialog.ui.combo_box_danhmuc.count()):
            if dialog.ui.combo_box_danhmuc.itemText(i) == product_data['danh_muc']:
                dialog.ui.combo_box_danhmuc.setCurrentIndex(i)
                break
        for i in range(dialog.ui.combo_box_kho.count()):
            if dialog.ui.combo_box_kho.itemText(i) == product_data['kho']:
                dialog.ui.combo_box_kho.setCurrentIndex(i)
                break

        if dialog.exec_():
            new_data = dialog.get_product_data()
            if new_data:
                # Cập nhật danh sách tạm
                formatted_product = {
                    'id': new_data['id_prod'],
                    'ten': new_data['name'],
                    'danh_muc': new_data['category_name'],
                    'kho': new_data['warehouse_name'],
                    'so_luong': int(new_data['quantity']),
                    'don_vi': new_data['unit'],
                    'gia_nhap': float(new_data['import_price']),
                    'total_amount': new_data['total_amount']  # Lấy tổng tiền từ product_data
                }
                self.product_list[row] = formatted_product

                # Cập nhật new_products nếu sản phẩm là mới
                if any(p['id'] == new_data['id_prod'] for p in self.new_products):
                    for i, p in enumerate(self.new_products):
                        if p['id'] == int(new_data['id_prod']):
                            self.new_products[i] = {
                                'id': int(new_data['id_prod']),
                                'name': new_data['name'],
                                'unit': new_data['unit'],
                                'price': 0,
                                'price_import': float(new_data['import_price']),
                                'description': None,
                                'id_category': new_data['category_id'],
                                'image_url': None
                            }
                            break

                # Cập nhật bảng hiển thị
                self.ui.table_san_pham_pn.setItem(row, 0, QTableWidgetItem(new_data['id_prod']))
                self.ui.table_san_pham_pn.setItem(row, 1, QTableWidgetItem(new_data['name']))
                self.ui.table_san_pham_pn.setItem(row, 2, QTableWidgetItem(new_data['category_name']))
                self.ui.table_san_pham_pn.setItem(row, 3, QTableWidgetItem(new_data['warehouse_name']))
                self.ui.table_san_pham_pn.setItem(row, 4, QTableWidgetItem(new_data['quantity']))
                self.ui.table_san_pham_pn.setItem(row, 5, QTableWidgetItem(new_data['unit']))
                self.ui.table_san_pham_pn.setItem(row, 6, QTableWidgetItem(new_data['import_price']))

                # Cập nhật tổng tiền
                self.update_total_amount()

    def delete_product(self, row):
        """
        Xóa sản phẩm khỏi bảng
        """
        reply = QMessageBox.question(
            self,
            'Xác nhận xóa',
            f'Bạn có chắc chắn muốn xóa sản phẩm {self.product_list[row]["ten"]} khỏi phiếu nhập?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            product_id = self.product_list[row]['id']
            del self.product_list[row]
            self.new_products = [p for p in self.new_products if p['id'] != int(product_id)]
            self.ui.table_san_pham_pn.removeRow(row)

            # Cập nhật tổng tiền
            self.update_total_amount()

    def accept(self):
        """
        Thêm phiếu nhập hàng
        """
        import_data = self.get_import_data()

        # Kiểm tra dữ liệu
        if not import_data['id_phieu_nhap']:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID phiếu nhập")
            return

        if not import_data['id_nhan_vien']:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn nhân viên")
            return

        if not import_data['san_pham_list']:
            QMessageBox.warning(self, "Lỗi", "Vui lòng thêm ít nhất một sản phẩm")
            return

        success, message, id_imp = NhapHangDAO.add_phieu_nhap(import_data, self.new_products)

        if success:
            QMessageBox.information(self, "Thành công", message)
            super().accept()
        else:
            QMessageBox.warning(self, "Lỗi", message)

    def add_import(self):
        """
        Thêm phiếu nhập hàng
        """
        import_data = self.get_import_data()

        if not import_data['id_phieu_nhap']:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID phiếu nhập")
            return

        if not import_data['id_nhan_vien']:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn nhân viên")
            return

        if not import_data['san_pham_list']:
            QMessageBox.warning(self, "Lỗi", "Vui lòng thêm ít nhất một sản phẩm")
            return

        success, message, _ = NhapHangDAO.add_phieu_nhap(import_data)

        if success:
            QMessageBox.information(self, "Thành công", message)
            self.accept()  # Đóng dialog với kết quả Accepted
        else:
            QMessageBox.warning(self, "Lỗi", message)