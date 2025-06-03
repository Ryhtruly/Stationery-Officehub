from PyQt5 import QtWidgets
from src.modules.admin.dialog.add_category_dialog import AddCategoryDialog

class CategoryHandler:
    def __init__(self, parent=None):
        self.parent = parent

    def show_add_category_dialog(self):
        """Hiển thị dialog thêm danh mục"""
        dialog = AddCategoryDialog(self.parent)
        result = dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            category_id = dialog.ui.line_id.text()
            category_name = dialog.ui.line_nameDanhMuc.text()

            self.add_category_to_database(category_id, category_name)

            return True, category_id, category_name
        return False, None, None

    def add_category_to_database(self, category_id, category_name):
        """Thêm danh mục vào database"""
        # Code xử lý thêm vào database ở đây
        print(f"Đã thêm danh mục: {category_id} - {category_name}")
        # TODO: Thêm code kết nối database và thêm danh mục

