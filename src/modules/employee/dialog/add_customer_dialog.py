from PyQt5 import QtWidgets
import re

from src.database.connection import create_connection
from src.database.models.customer import KhachHang
from src.modules.employee.ui.ui_py.add_customer import Ui_Form
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime
from src.database.DAO.employee.CustomerDAO import CustomerDAO

class AddCustomerDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, customer_id=None):
        super(AddCustomerDialog, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.customer_id = customer_id
        self.main_window = parent

        self.setWindowTitle("Thêm khách hàng mới" if customer_id is None else "Cập nhật khách hàng")

        if hasattr(self.ui, "them_sua_label"):
            self.ui.them_sua_label.setText("THÊM KHÁCH HÀNG MỚI" if customer_id is None else "CẬP NHẬT KHÁCH HÀNG")

        if hasattr(self.ui, "huy_btn"):
            self.ui.huy_btn.clicked.connect(self.close)
        if hasattr(self.ui, "them_btn"):
            self.ui.them_btn.clicked.connect(self.save_customer)
            self.ui.them_btn.setText("Thêm" if customer_id is None else "Cập nhật")
        if customer_id is not None:
            if hasattr(self.ui, "line_id"):
                self.ui.line_id.setReadOnly(True)
                self.ui.line_id.setEnabled(False)
            self.load_customer_data()
        else:
            self.generate_new_id()

    def generate_new_id(self):
        """
        Tự động tạo ID mới cho khách hàng bằng cách lấy ID lớn nhất hiện tại và tăng thêm 1
        """
        try:
            connection = create_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT MAX(id_cust) FROM Customers")
            max_id = cursor.fetchone()[0]

            if max_id is None:
                new_id = 1
            else:
                new_id = max_id + 1

            self.ui.line_id.setText(str(new_id))

            cursor.close()
            connection.close()

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tạo ID mới cho khách hàng: {str(e)}")

    def load_customer_data(self):
        """
        Load thông tin khách hàng vào form khi ở chế độ sửa
        """
        try:
            customer = CustomerDAO.get_customer_by_id(self.customer_id)

            if customer:
                if hasattr(self.ui, "line_id"):
                    self.ui.line_id.setText(str(customer.id_cust))
                if hasattr(self.ui, "line_name"):
                    self.ui.line_name.setText(customer.fullname)
                if hasattr(self.ui, "line_phoneNum"):
                    self.ui.line_phoneNum.setText(customer.phone)
            else:
                QMessageBox.warning(self, "Cảnh báo", "Không tìm thấy thông tin khách hàng!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể load thông tin khách hàng: {str(e)}")

    def validate_customer(self, fullname, phone):
        """Validate dữ liệu khách hàng trước khi lưu"""
        # Kiểm tra tên không chứa số hoặc ký tự đặc biệt (chỉ cần không có số là được)
        if any(char.isdigit() for char in fullname):
            QMessageBox.warning(self, "Cảnh báo", "Tên khách hàng không được chứa số!")
            return False

        # Kiểm tra trùng tên khách hàng (không phân biệt hoa/thường)
        try:
            connection = create_connection()
            cursor = connection.cursor()
            if self.customer_id:
                cursor.execute("SELECT COUNT(*) FROM Customers WHERE LOWER(fullname) = LOWER(?) AND id_cust != ?", (fullname, self.customer_id))
            else:
                cursor.execute("SELECT COUNT(*) FROM Customers WHERE LOWER(fullname) = LOWER(?)", (fullname,))
            count = cursor.fetchone()[0]
            cursor.close()
            connection.close()
            if count > 0:
                QMessageBox.warning(self, "Cảnh báo", f"Tên khách hàng '{fullname}' đã tồn tại!")
                return False
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi kiểm tra trùng tên khách hàng: {str(e)}")
            return False

        # Kiểm tra trùng số điện thoại
        try:
            connection = create_connection()
            cursor = connection.cursor()
            if self.customer_id:
                cursor.execute("SELECT COUNT(*) FROM Customers WHERE phone = ? AND id_cust != ?", (phone, self.customer_id))
            else:
                cursor.execute("SELECT COUNT(*) FROM Customers WHERE phone = ?", (phone,))
            count = cursor.fetchone()[0]
            cursor.close()
            connection.close()
            if count > 0:
                QMessageBox.warning(self, "Cảnh báo", f"Số điện thoại '{phone}' đã được đăng ký! Vui lòng sử dụng số khác.")
                return False
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi kiểm tra trùng số điện thoại: {str(e)}")
            return False

        return True

    def save_customer(self):
        """
        Lưu thông tin khách hàng (thêm mới hoặc cập nhật)
        """
        try:
            id_cust_text = self.ui.line_id.text().strip()
            fullname = self.ui.line_name.text().strip()
            phone = self.ui.line_phoneNum.text().strip()

            # Validate cơ bản
            if not id_cust_text and not self.customer_id:
                QMessageBox.warning(self, "Cảnh báo", "ID khách hàng không được để trống!")
                return
            if not self.customer_id:
                try:
                    id_cust = int(id_cust_text)
                    if id_cust <= 0:
                        QMessageBox.warning(self, "Cảnh báo", "ID khách hàng phải lớn hơn 0!")
                        return
                except ValueError:
                    QMessageBox.warning(self, "Cảnh báo", "ID khách hàng phải là số nguyên!")
                    return
            if not fullname:
                QMessageBox.warning(self, "Cảnh báo", "Tên khách hàng không được để trống!")
                return
            if not phone:
                QMessageBox.warning(self, "Cảnh báo", "Số điện thoại không được để trống!")
                return
            if not phone.isdigit() or len(phone) != 10:
                QMessageBox.warning(self, "Cảnh báo", "Số điện thoại phải là 10 chữ số!")
                return

            # Validate bổ sung: kiểm tra trùng tên và số điện thoại
            if not self.validate_customer(fullname, phone):
                return

            if self.customer_id:
                current_customer = CustomerDAO.get_customer_by_id(self.customer_id)
                if not current_customer:
                    QMessageBox.critical(self, "Lỗi", "Không tìm thấy thông tin khách hàng!")
                    return

                customer = KhachHang(
                    id_cust=self.customer_id,
                    fullname=fullname,
                    phone=phone,
                    rank=current_customer.rank,
                    register_date=current_customer.register_date
                )

                success = CustomerDAO.update_customer(customer)
                if success:
                    QMessageBox.information(self, "Thông báo", "Cập nhật thông tin khách hàng thành công!")
                    self.accept()
                else:
                    QMessageBox.critical(self, "Lỗi", "Không thể cập nhật thông tin khách hàng!")
            else:
                try:
                    # Chỉ truyền fullname và phone, vì CustomerDAO.add_customer tự tạo id_cust
                    CustomerDAO.add_customer(fullname, phone)
                    QMessageBox.information(self, "Thông báo", "Thêm khách hàng mới thành công!")
                    self.accept()
                except Exception as e:
                    QMessageBox.critical(self, "Lỗi", f"Không thể thêm khách hàng mới: {str(e)}")

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi khi lưu thông tin khách hàng: {str(e)}")