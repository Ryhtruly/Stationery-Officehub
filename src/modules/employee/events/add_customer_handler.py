from PyQt5 import QtWidgets
from src.modules.employee.dialog.add_customer_dialog import AddCustomerDialog
from src.modules.employee.data.customer_data import load_data_to_customer_tb


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

            # Nếu dialog trả về kết quả là Accepted (người dùng đã thêm/cập nhật thành công)
            if result == QtWidgets.QDialog.Accepted:
                # Reload lại bảng khách hàng
                if hasattr(self.parent, 'ui') and hasattr(self.parent.ui, 'table_khachhang'):
                    load_data_to_customer_tb(self.parent.ui.table_khachhang)
                    print("Đã reload bảng khách hàng sau khi thêm/cập nhật")
                else:
                    print("Không thể reload bảng khách hàng: không tìm thấy table_khachhang")

        except Exception as e:
            QtWidgets.QMessageBox.critical(self.parent, "Lỗi", f"Không thể mở dialog thêm khách hàng: {str(e)}")

    def show_edit_customer_dialog(self, customer_id):
        """
        Hiển thị dialog chỉnh sửa thông tin khách hàng
        """
        try:
            dialog = AddCustomerDialog(self.parent, customer_id)
            result = dialog.exec_()

            # Nếu dialog trả về kết quả là Accepted (người dùng đã thêm/cập nhật thành công)
            if result == QtWidgets.QDialog.Accepted:
                # Reload lại bảng khách hàng
                if hasattr(self.parent, 'ui') and hasattr(self.parent.ui, 'table_khachhang'):
                    load_data_to_customer_tb(self.parent.ui.table_khachhang)
                    print("Đã reload bảng khách hàng sau khi thêm/cập nhật")
                else:
                    print("Không thể reload bảng khách hàng: không tìm thấy table_khachhang")

        except Exception as e:
            QtWidgets.QMessageBox.critical(self.parent, "Lỗi", f"Không thể mở dialog chỉnh sửa khách hàng: {str(e)}")
