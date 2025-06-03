from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog
from src.modules.admin.dialog.inventory_adjust_dialog import InventoryAdjustDialog

class InventoryAdjustHandler:
    def __init__(self, parent=None):
        self.parent = parent

    def show_inventory_adjust_dialog(self):
        """Hiển thị dialog chỉnh sửa số lượng tồn kho."""
        dialog = InventoryAdjustDialog(self.parent)
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        result = dialog.exec_()
        return result == QDialog.Accepted