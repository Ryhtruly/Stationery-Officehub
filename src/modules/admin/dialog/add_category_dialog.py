from PyQt5 import QtWidgets, QtCore
import re

from src.modules.admin.ui.ui_py.add_category import Ui_Form
from src.database.DAO.admin.CategoryDAO import CategoryDAO
from src.database.connection import create_connection
import ctypes

class AddCategoryDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, category_id=None):
        super(AddCategoryDialog, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.category_id = category_id
        self.enable_blur()

        self.setWindowTitle("Thêm danh mục" if category_id is None else "Cập nhật danh mục")
        self.setModal(True)

        if hasattr(self.ui, "them_sua_label"):
            self.ui.them_sua_label.setText("THÊM DANH MỤC MỚI" if category_id is None else "CẬP NHẬT DANH MỤC")

        if hasattr(self.ui, "them_btn"):
            self.ui.them_btn.setText("Thêm" if category_id is None else "Cập nhật")

        self.ui.them_btn.clicked.connect(self.save_category)
        self.ui.huy_btn.clicked.connect(self.reject)

        if category_id:
            self.load_category_data()
        else:
            self.generate_new_id()

        print("Các thuộc tính có sẵn trong UI:")
        for attr in dir(self.ui):
            if not attr.startswith('__'):
                print(f"- {attr}")

    def enable_blur(self):
        hwnd = int(self.winId())
        accent_policy = ctypes.c_int * 4
        accent = accent_policy(5, 0, 0, 0)

        class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
            _fields_ = [
                ("Attribute", ctypes.c_int),
                ("Data", ctypes.c_void_p),
                ("SizeOfData", ctypes.c_size_t)
            ]

        data = WINDOWCOMPOSITIONATTRIBDATA()
        data.Attribute = 19
        data.Data = ctypes.cast(ctypes.pointer(accent), ctypes.c_void_p)
        data.SizeOfData = ctypes.sizeof(accent)

        set_window_composition_attribute = ctypes.windll.user32.SetWindowCompositionAttribute
        set_window_composition_attribute(hwnd, ctypes.byref(data))

    def generate_new_id(self):
        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT MAX(id_category) FROM Categories")
            max_id = cursor.fetchone()[0]
            if max_id is None:
                new_id = 1
            else:
                new_id = max_id + 1
            self.ui.line_id.setText(str(new_id))

            cursor.close()
            connection.close()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Không thể tạo ID mới: {str(e)}")

    def load_category_data(self):
        if self.category_id is None:
            return

        try:
            print(f"Đang nạp thông tin danh mục có ID: {self.category_id}")
            category = CategoryDAO.get_category_by_id(self.category_id)

            print(f"Kết quả truy vấn: {category}")

            if category:
                if hasattr(self.ui, "line_id"):
                    self.ui.line_id.setText(str(category.id_category))
                    self.ui.line_id.setReadOnly(True)
                    print(f"Đã đặt ID danh mục: {category.id_category}")

                if hasattr(self.ui, "line_nameDanhMuc"):
                    self.ui.line_nameDanhMuc.setText(category.name)
                    print(f"Đã đặt tên danh mục: {category.name}")

                print("Đã nạp thông tin danh mục vào form")
            else:
                print(f"Không tìm thấy danh mục có ID: {self.category_id}")
                QtWidgets.QMessageBox.warning(
                    self,
                    "Lỗi",
                    f"Không tìm thấy danh mục có ID: {self.category_id}"
                )

        except Exception as e:
            print(f"Lỗi khi nạp thông tin danh mục: {e}")
            import traceback
            traceback.print_exc()

    def validate_category(self, id_category, name):
        """Validate dữ liệu danh mục trước khi lưu"""
        # Kiểm tra ID không âm
        try:
            id_category = int(id_category)
            if id_category < 0:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "ID danh mục không được âm.")
                return False
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "ID danh mục phải là số nguyên.")
            return False

        # Kiểm tra tên không chứa ký tự đặc biệt
        if not re.match(r'^[a-zA-Z0-9\s-]+$', name):
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Tên danh mục chỉ được chứa chữ, số, dấu cách và dấu gạch ngang.")
            return False

        # Kiểm tra tên trùng (không phân biệt hoa/thường)
        try:
            connection = create_connection()
            cursor = connection.cursor()
            if self.category_id:
                cursor.execute("SELECT COUNT(*) FROM Categories WHERE LOWER(name) = LOWER(?) AND id_category != ?",
                             (name, self.category_id))
            else:
                cursor.execute("SELECT COUNT(*) FROM Categories WHERE LOWER(name) = LOWER(?)", (name,))
            count = cursor.fetchone()[0]
            cursor.close()
            connection.close()
            if count > 0:
                QtWidgets.QMessageBox.warning(self, "Lỗi", f"Tên danh mục '{name}' đã tồn tại.")
                return False
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Lỗi kiểm tra trùng tên danh mục: {str(e)}")
            return False

        return True

    def get_category_data(self):
        category_data = {}
        if hasattr(self.ui, "line_id"):
            category_data["id"] = self.ui.line_id.text().strip()
        if hasattr(self.ui, "line_nameDanhMuc"):
            category_data["name"] = self.ui.line_nameDanhMuc.text().strip()
        return category_data

    def save_category(self):
        try:
            category_data = self.get_category_data()

            if not category_data["id"]:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "ID danh mục không được để trống.")
                return
            if not category_data["name"]:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Tên danh mục không được để trống.")
                return

            # Validate dữ liệu
            if not self.validate_category(category_data["id"], category_data["name"]):
                return

            success = False
            if self.category_id is None:
                # Thêm mới danh mục
                success = CategoryDAO.add_category(category_data["name"])
                message = "Thêm danh mục thành công!"
            else:
                # Cập nhật danh mục
                success = CategoryDAO.update_category(self.category_id, category_data["name"])
                message = "Cập nhật danh mục thành công!"

            if success:
                QtWidgets.QMessageBox.information(self, "Thành công", message)
                self.accept()
            else:
                QtWidgets.QMessageBox.critical(self, "Lỗi", "Không thể lưu danh mục. Vui lòng thử lại!")

        except Exception as e:
            print(f"Lỗi khi lưu danh mục: {e}")
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi: {str(e)}")