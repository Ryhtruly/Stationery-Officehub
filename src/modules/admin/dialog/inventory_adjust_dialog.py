from PyQt5.QtWidgets import QDialog, QMessageBox
from src.modules.admin.ui.ui_py.inventory_adjust import Ui_Form
from src.database.DAO.admin.ProductAdminDAO import ProductDAO
from src.database.DAO.admin.WarehouseDAO import WarehouseDAO

class InventoryAdjustDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.them_btn.clicked.connect(self.save_inventory)
        self.ui.huy_btn.clicked.connect(self.reject)

        self.load_products()

    def load_products(self):
        """Tải danh sách sản phẩm vào combo box."""
        products = ProductDAO.get_all_products()
        self.ui.cbb_ten_san_pham.clear()
        self.product_mapping = {}  # Lưu ánh xạ tên sản phẩm với id_prod
        for product in products:
            self.product_mapping[product.name] = product.id_prod
            self.ui.cbb_ten_san_pham.addItem(product.name)

    def save_inventory(self):
        """Lưu số lượng tồn kho mới."""
        selected_product_name = self.ui.cbb_ten_san_pham.currentText()
        if not selected_product_name:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một sản phẩm!")
            return

        quantity_text = self.ui.line_so_luong.text().strip()
        if not quantity_text:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập số lượng!")
            return

        try:
            quantity = int(quantity_text)
            if quantity < 0:
                QMessageBox.warning(self, "Cảnh báo", "Số lượng không thể âm!")
                return
        except ValueError:
            QMessageBox.warning(self, "Cảnh báo", "Số lượng phải là một số nguyên!")
            return

        # Lấy id_prod từ tên sản phẩm
        id_prod = self.product_mapping.get(selected_product_name)
        if not id_prod:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy ID sản phẩm!")
            return

        # Cập nhật tồn kho (giả sử id_warehouse = 1, bạn có thể điều chỉnh)
        success, message = WarehouseDAO.add_product_to_warehouse(
            id_warehouse=1,  # Có thể thay đổi nếu có nhiều kho
            id_prod=id_prod,
            inventory=quantity
        )

        if success:
            QMessageBox.information(self, "Thành công", "Cập nhật số lượng tồn kho thành công!")
            self.accept()
        else:
            QMessageBox.critical(self, "Lỗi", message)