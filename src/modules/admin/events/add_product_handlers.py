from PyQt5 import QtWidgets
from src.modules.admin.dialog.add_product_dialog import AddProductDialog


class ProductHandler:
    def __init__(self, parent=None):
        self.parent = parent

    def show_add_product_dialog(self):
        """Hiển thị dialog thêm sản phẩm"""
        dialog = AddProductDialog(self.parent)
        result = dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            product_data = dialog.get_product_data()

            success = self.add_product_to_database(product_data)

            if success:
                return True, product_data
            else:
                QtWidgets.QMessageBox.warning(
                    self.parent,
                    "Lỗi",
                    "Không thể thêm sản phẩm. Vui lòng thử lại."
                )
                return False, None
        return False, None

    def add_product_to_database(self, product_data):
        """Thêm sản phẩm vào database"""
        try:
            # TODO: Thêm code kết nối database và thêm sản phẩm

            print(f"Đã thêm sản phẩm: {product_data['name']}")
            return True
        except Exception as e:
            print(f"Lỗi khi thêm sản phẩm: {e}")
            return False
