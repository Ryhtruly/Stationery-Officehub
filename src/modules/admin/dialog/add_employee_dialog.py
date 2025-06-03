import datetime
import re

from PyQt5 import QtWidgets, QtGui
from src.modules.admin.ui.ui_py.add_employee import Ui_Form
from src.database.DAO.admin.EmployeeDAO import EmployeeDAO
from src.database.models.account import Account
from src.database.models.employee import NhanVien
from src.database.DAO.common.AccountDAO import AccountDAO
from src.database.connection import create_connection

class AddEmployeeDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, employee_id=None):
        super(AddEmployeeDialog, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.employee_id = employee_id

        self.setWindowTitle("Thêm/Sửa Nhân Viên")
        self.ui.them_sua_label.setText("THÊM THÔNG TIN NHÂN VIÊN MỚI" if employee_id is None else "SỦA THÔNG TIN NHÂN VIÊN")
        self.ui.them_btn.setText("THÊM" if employee_id is None else "Cập nhật")
        self.ui.them_btn.clicked.connect(self.add_employee)
        self.ui.huy_btn.clicked.connect(self.reject)
        if employee_id:
            self.load_employee_data(employee_id)
        else:
            self.generate_new_id()

        self.ui.line_id.textChanged.connect(self.check_id_exists)

    def generate_new_id(self):
        try:
            connection = create_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT MAX(id_emp) FROM Employees")
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

    def check_id_exists(self):
        """
        Kiểm tra xem ID nhân viên đã tồn tại chưa
        """
        id_text = self.ui.line_id.text().strip()
        if not id_text:
            return

        try:
            id_emp = int(id_text)

            if self.employee_id and id_emp == self.employee_id:
                return

            connection = create_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM Employees WHERE id_emp = ?", (id_emp,))
            count = cursor.fetchone()[0]

            cursor.close()
            connection.close()

            if count > 0:
                self.ui.line_id.setStyleSheet("border: 1px solid red;")
                QtWidgets.QToolTip.showText(
                    self.ui.line_id.mapToGlobal(QtWidgets.QPoint(0, 0)),
                    f"ID nhân viên {id_emp} đã tồn tại",
                    self.ui.line_id
                )
            else:
                self.ui.line_id.setStyleSheet("")

        except ValueError:
            self.ui.line_id.setStyleSheet("border: 1px solid red;")
            QtWidgets.QToolTip.showText(
                self.ui.line_id.mapToGlobal(QtWidgets.QPoint(0, 0)),
                "ID nhân viên phải là số nguyên",
                self.ui.line_id
            )

    def load_employee_data(self, employee_id):
        """
        Tải thông tin nhân viên lên form
        """
        try:
            # Lấy thông tin nhân viên từ database
            nhan_vien = EmployeeDAO.get_nhan_vien_by_id(employee_id)
            if not nhan_vien:
                QtWidgets.QMessageBox.warning(self, "Lỗi", f"Không tìm thấy nhân viên có ID {employee_id}")
                self.reject()
                return

            # Hiển thị thông tin nhân viên lên form
            self.ui.line_id.setText(str(nhan_vien.id_emp))
            self.ui.line_fullName.setText(nhan_vien.fullname)
            self.ui.line_address.setText(nhan_vien.address if nhan_vien.address else "")
            self.ui.line_phoneNum.setText(nhan_vien.phone if nhan_vien.phone else "")
            self.ui.line_salary.setText(str(nhan_vien.salary) if nhan_vien.salary else "")
            self.ui.line_email.setText(nhan_vien.email if nhan_vien.email else "")

            # Lấy thông tin tài khoản
            account = AccountDAO.get_account_by_employee_id(employee_id)
            if account:
                self.ui.line_name.setText(account.username)
                self.ui.line_pass.setText(account.password)

            # Disable ô ID khi đang sửa
            self.ui.line_id.setEnabled(False)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Không thể tải thông tin nhân viên: {str(e)}")
            self.reject()

    def add_employee(self):
        """
        Xử lý sự kiện khi người dùng nhấn nút Thêm/Cập nhật
        """
        try:
            # Lấy dữ liệu từ form
            id_emp_text = self.ui.line_id.text().strip()
            fullname = self.ui.line_fullName.text().strip()
            address = self.ui.line_address.text().strip()
            phone = self.ui.line_phoneNum.text().strip()
            salary_text = self.ui.line_salary.text().strip()
            email = self.ui.line_email.text().strip()
            username = self.ui.line_name.text().strip()
            password = self.ui.line_pass.text().strip()

            # Validate input
            if not id_emp_text:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "ID nhân viên không được để trống.")
                return
            if not fullname:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Họ tên không được để trống.")
                return
            if not phone:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Số điện thoại không được để trống.")
                return
            if not phone.isdigit() or len(phone) != 10:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Số điện thoại phải là 10 chữ số.")
                return
            if not email:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Email không được để trống.")
                return
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Email không hợp lệ.")
                return
            if not username:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Tên đăng nhập không được để trống.")
                return
            if not password:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Mật khẩu không được để trống.")
                return
            if len(password) < 6:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Mật khẩu phải có ít nhất 6 ký tự.")
                return

            try:
                id_emp = int(id_emp_text)
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "ID nhân viên phải là số nguyên.")
                return

            salary = None
            if salary_text:
                try:
                    salary = float(salary_text)
                    if salary < 0:
                        QtWidgets.QMessageBox.warning(self, "Lỗi", "Lương không được âm.")
                        return
                except ValueError:
                    QtWidgets.QMessageBox.warning(self, "Lỗi", "Lương phải là một số hợp lệ.")
                    return

            if not self.employee_id:  # Chỉ kiểm tra khi thêm mới
                connection = create_connection()
                cursor = connection.cursor()

                cursor.execute("SELECT COUNT(*) FROM Employees WHERE id_emp = ?", (id_emp,))
                count = cursor.fetchone()[0]
                cursor.close()
                connection.close()

                if count > 0:
                    QtWidgets.QMessageBox.warning(self, "Lỗi", f"ID nhân viên {id_emp} đã tồn tại.")
                    return

            connection = create_connection()
            cursor = connection.cursor()

            if self.employee_id:
                cursor.execute("SELECT username FROM Accounts WHERE id_emp = ?", (self.employee_id,))
                current_username = cursor.fetchone()
                if current_username and current_username[0] != username:
                    cursor.execute("SELECT COUNT(*) FROM Accounts WHERE username = ? AND id_emp <> ?", (username, self.employee_id))
                    count = cursor.fetchone()[0]
                    if count > 0:
                        cursor.close()
                        connection.close()
                        QtWidgets.QMessageBox.warning(self, "Lỗi", f"Tên đăng nhập {username} đã tồn tại.")
                        return
            else:
                cursor.execute("SELECT COUNT(*) FROM Accounts WHERE username = ?", (username,))
                count = cursor.fetchone()[0]
                if count > 0:
                    cursor.close()
                    connection.close()
                    QtWidgets.QMessageBox.warning(self, "Lỗi", f"Tên đăng nhập {username} đã tồn tại.")
                    return

            cursor.close()
            connection.close()

            try:
                connection = create_connection()
                cursor = connection.cursor()
                connection.autocommit = False

                if self.employee_id:
                    query_employee = """
                        UPDATE Employees 
                        SET fullname = ?, address = ?, phone = ?, salary = ?, email = ?
                        WHERE id_emp = ?
                    """
                    cursor.execute(query_employee, (fullname, address, phone, salary, email, self.employee_id))

                    # Cập nhật tài khoản nếu cần
                    query_account = """
                        UPDATE Accounts 
                        SET username = ?, password = ?
                        WHERE id_emp = ?
                    """
                    cursor.execute(query_account, (username, password, self.employee_id))

                else:
                    query_employee = """
                        INSERT INTO Employees (id_emp, fullname, address, phone, salary, email)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """
                    cursor.execute(query_employee, (id_emp, fullname, address, phone, salary, email))

                    query_account = """
                        INSERT INTO Accounts (username, password, id_emp, role, is_active, created_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """
                    cursor.execute(query_account, (
                        username,
                        password,
                        id_emp,
                        'employee',
                        1,
                        datetime.datetime.now()
                    ))

                connection.commit()

                QtWidgets.QMessageBox.information(self, "Thành công",
                                                  "Cập nhật nhân viên thành công!" if self.employee_id else "Thêm nhân viên thành công!")
                self.accept()

            except Exception as e:
                connection.rollback()
                QtWidgets.QMessageBox.critical(self, "Lỗi",
                                               f"Không thể {('cập nhật' if self.employee_id else 'thêm')} nhân viên: {str(e)}")

            finally:
                cursor.close()
                connection.close()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi: {str(e)}")