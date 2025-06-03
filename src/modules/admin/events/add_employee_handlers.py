from PyQt5 import QtWidgets

from src.database.DAO.admin.EmployeeDAO import EmployeeDAO
from src.modules.admin.dialog.add_employee_dialog import AddEmployeeDialog
from src.database.models.employee import NhanVien


class EmployeeHandler:
    def __init__(self, main_window):
        self.main_window = main_window

    def show_add_employee_dialog(self):
        """
        Hiển thị dialog thêm nhân viên và trả về kết quả
        """
        dialog = AddEmployeeDialog(self.main_window)
        result = dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            self.main_window.update_employee_list()
            return True, {}

        return False, {}

    def validate_employee_data(self, id_emp, fullname, username, password):
        """
        Kiểm tra tính hợp lệ của dữ liệu nhân viên
        """
        # Kiểm tra các trường bắt buộc
        if not id_emp or not fullname or not username or not password:
            return False, "Vui lòng nhập đầy đủ thông tin bắt buộc"

        try:
            id_emp = int(id_emp)
        except ValueError:
            return False, "ID nhân viên phải là số nguyên"

        if EmployeeDAO.check_id_exists(id_emp):
            return False, f"ID nhân viên {id_emp} đã tồn tại"

        return True, ""

    def open_add_employee_dialog(self):
        """
        Mở dialog thêm nhân viên
        """
        dialog = AddEmployeeDialog(self.main_window)
        result = dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            self.main_window.load_employee_data()

    def open_edit_employee_dialog(self, employee_id):
        """
        Mở dialog sửa nhân viên
        """
        dialog = AddEmployeeDialog(self.main_window, employee_id)
        result = dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            self.main_window.load_employee_data()

    def delete_employee(self, employee_id):
        """
        Xóa nhân viên
        """
        # Hiển thị hộp thoại xác nhận
        reply = QtWidgets.QMessageBox.question(
            self.main_window,
            'Xác nhận xóa',
            f'Bạn có chắc chắn muốn xóa nhân viên có ID {employee_id} không?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            try:
                # Thực hiện xóa nhân viên
                from src.database.connection import create_connection
                connection = create_connection()
                cursor = connection.cursor()

                # Bắt đầu transaction
                connection.autocommit = False

                # Xóa tài khoản trước (nếu có)
                cursor.execute("DELETE FROM Accounts WHERE id_emp = ?", (employee_id,))

                # Xóa nhân viên
                cursor.execute("DELETE FROM Employees WHERE id_emp = ?", (employee_id,))

                # Commit transaction
                connection.commit()

                cursor.close()
                connection.close()

                # Hiển thị thông báo thành công
                QtWidgets.QMessageBox.information(
                    self.main_window,
                    'Thành công',
                    f'Đã xóa nhân viên có ID {employee_id}'
                )

                # Cập nhật bảng nhân viên
                self.main_window.load_employee_data()

            except Exception as e:
                # Rollback nếu có lỗi
                if 'connection' in locals() and connection:
                    connection.rollback()
                    cursor.close()
                    connection.close()

                # Hiển thị thông báo lỗi
                QtWidgets.QMessageBox.critical(
                    self.main_window,
                    'Lỗi',
                    f'Không thể xóa nhân viên: {str(e)}'
                )

