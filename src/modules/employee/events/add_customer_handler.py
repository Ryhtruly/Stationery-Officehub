from PyQt5 import QtWidgets
from src.modules.employee.dialog.add_customer_dialog import AddCustomerDialog


class CustomerHandler:
    def __init__(self, parent=None):
        self.parent = parent

    def show_add_customer_dialog(self):
        """
        Hiển thị dialog thêm khách hàng mới
        """
        try:
            dialog = AddCustomerDialog(self.parent)
            result = dialog.exec_()

            if result == QtWidgets.QDialog.Accepted:
                from src.modules.employee.data.customer_data import load_data_to_customer_tb
                if hasattr(self.parent, 'tb_customer'):
                    load_data_to_customer_tb(self.parent.tb_customer)
        except Exception as e:
            print(f"Lỗi khi hiển thị dialog: {str(e)}")

    def show_edit_customer_dialog(self, customer_id):
        """
        Hiển thị dialog sửa thông tin khách hàng
        """
        try:
            from src.modules.employee.dialog.add_customer_dialog import AddCustomerDialog
            dialog = AddCustomerDialog(self.parent, customer_id)

            if hasattr(dialog, 'line_id'):
                dialog.line_id.setText(str(customer_id))
                dialog.line_id.setReadOnly(True)

            result = dialog.exec_()

            if result and hasattr(self.parent, 'load_customers'):
                self.parent.load_customers()

            return result
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(None, "Lỗi", f"Đã xảy ra lỗi khi hiển thị dialog: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

