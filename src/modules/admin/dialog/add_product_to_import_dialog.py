from PyQt5 import QtWidgets, QtGui, QtCore

from src.database.DAO.admin.ProductAdminDAO import ProductDAO
from src.modules.admin.ui.ui_py.add_product_to_import import Ui_Form
from PyQt5.QtWidgets import QMessageBox
from src.database.DAO.admin.CategoryDAO import CategoryDAO
from src.database.DAO.admin.WarehouseDAO import WarehouseDAO
from src.database.connection import create_connection

class AddProductToImportDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AddProductToImportDialog, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.setWindowTitle("Thêm sản phẩm vào phiếu nhập")
        self.setModal(True)

        self.setup_validation()

        self.connect_events()

        self.load_categories()

        self.finished.connect(self.on_dialog_finished)

        self.ui.them_btn.clicked.connect(self.add_product_to_import)
        self.ui.huy_btn.clicked.connect(self.close)

        self.generate_new_id()

    def generate_new_id(self):
        """
        Tự động tạo ID mới cho sản phẩm bằng cách lấy ID lớn nhất hiện tại và tăng thêm 1
        """
        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT MAX(id_prod) FROM Products")
            max_id = cursor.fetchone()[0]
            if max_id is None:
                new_id = 1
            else:
                new_id = max_id + 1
            self.ui.line_id.setText(str(new_id))
            cursor.close()
            connection.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Không thể tạo ID mới cho sản phẩm: {str(e)}")

    def add_product_to_import(self):
        """
        Xử lý sự kiện thêm sản phẩm vào phiếu nhập
        """
        try:
            # Lấy thông tin từ form
            id_prod_text = self.ui.line_id.text().strip()
            name = self.ui.line_name.text().strip()
            unit = self.ui.line_unit.text().strip()
            quantity_text = self.ui.line_soLuong.text().strip()
            price_import_text = self.ui.line_gia_nhap.text().strip()

            if not id_prod_text:
                QMessageBox.warning(self, "Lỗi", "ID sản phẩm không được để trống.")
                return
            try:
                id_prod = int(id_prod_text)
            except ValueError:
                QMessageBox.warning(self, "Lỗi", "ID sản phẩm phải là số nguyên.")
                return
            if not name:
                QMessageBox.warning(self, "Lỗi", "Tên sản phẩm không được để trống.")
                return
            if not unit:
                QMessageBox.warning(self, "Lỗi", "Đơn vị không được để trống.")
                return
            try:
                quantity = int(quantity_text)
                if quantity < 0:
                    QMessageBox.warning(self, "Lỗi", "Số lượng không được âm.")
                    return
            except ValueError:
                QMessageBox.warning(self, "Lỗi", "Số lượng phải là số nguyên hợp lệ.")
                return
            try:
                price_import = float(price_import_text)
                if price_import < 0:
                    QMessageBox.warning(self, "Lỗi", "Giá nhập không được âm.")
                return
            except ValueError:
                QMessageBox.warning(self, "Lỗi", "Giá nhập phải là số hợp lệ.")
                return

            category_index = self.ui.combo_box_danhmuc.currentIndex()
            id_category = self.ui.combo_box_danhmuc.itemData(category_index)
            if id_category is None or category_index <= 0:
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn danh mục.")
                return

            id_warehouse = 1
            if id_warehouse is None:
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn kho.")
                return

            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM Products WHERE id_prod = ?", (id_prod,))
            count = cursor.fetchone()[0]
            cursor.close()
            connection.close()
            if count > 0:
                QMessageBox.warning(self, "Lỗi", f"ID sản phẩm {id_prod} đã tồn tại.")
                return

            product_data = self.get_product_data()

            product = ProductDAO.get_product_by_id(str(id_prod))
            if product:
                self.product_data = product_data
                self.accept()
            else:
                self.product_data = product_data
                self.accept()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def on_dialog_finished(self, result):
        try:
            self.ui.line_soLuong.textChanged.disconnect()
            self.ui.line_gia_nhap.textChanged.disconnect()
            if hasattr(self.ui, "combo_box_danhmuc"):
                try:
                    self.ui.combo_box_danhmuc.currentIndexChanged.disconnect()
                except:
                    pass

        except:
            pass

    def setup_validation(self):
        validator = QtGui.QDoubleValidator()
        self.ui.line_soLuong.setValidator(validator)
        self.ui.line_gia_nhap.setValidator(validator)
        self.ui.line_soLuong.setPlaceholderText("Số lượng...")
        self.ui.them_sua_label.setText("THÊM SẢN PHẨM VÀO PHIẾU NHẬP")
        self.ui.them_btn.setText("THÊM")

    def connect_events(self):
        self.ui.them_btn.clicked.connect(self.accept)
        self.ui.huy_btn.clicked.connect(self.reject)
        self.ui.line_soLuong.textChanged.connect(self.update_total_price)
        self.ui.line_gia_nhap.textChanged.connect(self.update_total_price)

    def update_total_price(self):
        try:
            quantity_text = self.ui.line_soLuong.text().strip()
            price_text = self.ui.line_gia_nhap.text().strip()
            quantity = float(quantity_text) if quantity_text else 0
            price = float(price_text) if price_text else 0
            total_price = quantity * price
            self.total_price = total_price
        except ValueError:
            self.total_price = 0
        except Exception as e:
            print(f"Lỗi khi tính tổng giá trị: {str(e)}")
            self.total_price = 0

    def load_categories(self):
        print("Bắt đầu nạp danh mục...")
        try:
            if hasattr(self.ui, "combo_box_danhmuc"):
                print("Tìm thấy combo box danh mục: combo_box_danhmuc")
                categories = CategoryDAO.get_all_categories()
                print(f"Đã lấy được {len(categories)} danh mục từ database")
                self.ui.combo_box_danhmuc.clear()
                self.ui.combo_box_danhmuc.addItem("Thêm danh mục", -1)
                for category in categories:
                    print(f"Thêm danh mục: {category.name} (ID: {category.id_category})")
                    self.ui.combo_box_danhmuc.addItem(category.name, category.id_category)
                self.ui.combo_box_danhmuc.currentIndexChanged.connect(self.on_category_changed)
            else:
                print("Không tìm thấy combo box danh mục trong UI")
        except Exception as e:
            print(f"Lỗi khi nạp danh mục: {str(e)}")


    def on_category_changed(self, index):
        selected_value = self.ui.combo_box_danhmuc.itemData(index)
        if selected_value == -1:
            print("Người dùng chọn 'Thêm danh mục'")
            if index > 0 and self.ui.combo_box_danhmuc.count() > 1:
                self.ui.combo_box_danhmuc.setCurrentIndex(1)



    def get_product_data(self):
        try:
            product_id = self.ui.line_id.text().strip()
            product_name = self.ui.line_name.text().strip()
            category_index = self.ui.combo_box_danhmuc.currentIndex()
            category_id = self.ui.combo_box_danhmuc.itemData(category_index)
            category_name = self.ui.combo_box_danhmuc.currentText()
            warehouse_id = 1
            warehouse_name = "Kho 1"
            quantity = self.ui.line_soLuong.text().strip()
            unit = self.ui.line_unit.text().strip()
            import_price = self.ui.line_gia_nhap.text().strip()
            total_amount = getattr(self, 'total_price', 0)
            product_data = {
                'id_prod': product_id,
                'name': product_name,
                'category_id': category_id,
                'category_name': category_name,
                'warehouse_id': warehouse_id,
                'warehouse_name': warehouse_name,
                'quantity': quantity,
                'unit': unit,
                'import_price': import_price,
                'total_amount': total_amount
            }
            return product_data
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu sản phẩm: {str(e)}")
            return None

    def clear_form(self):
        self.ui.line_id.clear()
        self.ui.line_name.clear()
        self.ui.line_soLuong.clear()
        self.ui.line_gia_nhap.clear()
        self.ui.line_unit.clear()
        if hasattr(self.ui, "combo_box_danhmuc"):
            self.ui.combo_box_danhmuc.setCurrentIndex(0)