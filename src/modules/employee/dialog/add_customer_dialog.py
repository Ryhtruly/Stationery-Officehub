from PyQt5 import QtWidgets

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

    def add_customer(self):
        try:
            id_cust = self.ui.line_id.text().strip()
            fullname = self.ui.line_name.text().strip()
            phone = self.ui.line_phoneNum.text().strip()

            if not fullname:
                QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập tên khách hàng!")
                return

            if not phone:
                QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập số điện thoại!")
                return

            id_cust = int(id_cust) if id_cust and id_cust.isdigit() else None

            CustomerDAO.add_customer(fullname, phone, id_cust)

            QMessageBox.information(self, "Thông báo", "Thêm khách hàng thành công!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể thêm khách hàng mới: {str(e)}")

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

    def save_customer(self):
        """
        Lưu thông tin khách hàng (thêm mới hoặc cập nhật)
        """
        try:
            id_cust_text = self.ui.line_id.text().strip()
            fullname = self.ui.line_name.text().strip()
            phone = self.ui.line_phoneNum.text().strip()

            if not id_cust_text and not self.customer_id:
                QMessageBox.warning(self, "Cảnh báo", "ID khách hàng không được để trống!")
                return
            if not self.customer_id:
                try:
                    id_cust = int(id_cust_text)
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
            if not self.customer_id:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM Customers WHERE id_cust = ?", (id_cust,))
                count = cursor.fetchone()[0]
                cursor.close()
                connection.close()
                if count > 0:
                    QMessageBox.warning(self, "Cảnh báo", f"ID khách hàng {id_cust} đã tồn tại!")
                    return

            if self.customer_id:
                current_customer = CustomerDAO.get_customer_by_id(self.customer_id)
                if not current_customer:
                    QMessageBox.critical(self, "Lỗi", "Không tìm thấy thông tin khách hàng!")
                    return

                if phone != current_customer.phone and CustomerDAO.check_phone_exists(phone):
                    QMessageBox.warning(self, "Cảnh báo",
                                        "Số điện thoại này đã được đăng ký! Vui lòng sử dụng số khác.")
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

                if CustomerDAO.check_phone_exists(phone):
                    QMessageBox.warning(self, "Cảnh báo",
                                        "Số điện thoại này đã được đăng ký! Vui lòng sử dụng số khác.")
                    return

                try:
                    CustomerDAO.add_customer(fullname, phone, id_cust)
                    QMessageBox.information(self, "Thông báo", "Thêm khách hàng mới thành công!")
                    self.accept()
                except Exception as e:
                    QMessageBox.critical(self, "Lỗi", f"Không thể thêm khách hàng mới: {str(e)}")

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi khi lưu thông tin khách hàng: {str(e)}")