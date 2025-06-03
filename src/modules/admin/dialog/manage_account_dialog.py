from PyQt5 import QtWidgets, QtGui
from src.database.DAO.common.AccountDAO import AccountDAO
from src.database.models.account import Account


class ManageAccountDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, employee_id=None):
        super(ManageAccountDialog, self).__init__(parent)
        self.employee_id = employee_id
        self.account = None

        self.setup_ui()

        self.load_account_data()

    def setup_ui(self):
        """
        Thiết lập giao diện người dùng
        """
        self.setWindowTitle("Quản lý tài khoản")
        self.setMinimumWidth(400)

        # Layout chính
        main_layout = QtWidgets.QVBoxLayout(self)

        # Form layout
        form_layout = QtWidgets.QFormLayout()

        # Username
        self.username_txt = QtWidgets.QLineEdit()
        form_layout.addRow("Tên đăng nhập:", self.username_txt)

        # Password
        self.password_txt = QtWidgets.QLineEdit()
        self.password_txt.setEchoMode(QtWidgets.QLineEdit.Password)
        form_layout.addRow("Mật khẩu:", self.password_txt)

        # Role
        self.role_combo = QtWidgets.QComboBox()
        self.role_combo.addItems(["employee", "manager"])
        form_layout.addRow("Vai trò:", self.role_combo)

        # Active status
        self.active_check = QtWidgets.QCheckBox("Tài khoản hoạt động")
        self.active_check.setChecked(True)
        form_layout.addRow("", self.active_check)

        main_layout.addLayout(form_layout)

        # Buttons
        button_layout = QtWidgets.QHBoxLayout()

        self.save_btn = QtWidgets.QPushButton("Lưu")
        self.save_btn.clicked.connect(self.save_account)
        button_layout.addWidget(self.save_btn)

        self.delete_btn = QtWidgets.QPushButton("Xóa tài khoản")
        self.delete_btn.clicked.connect(self.delete_account)
        button_layout.addWidget(self.delete_btn)

        self.cancel_btn = QtWidgets.QPushButton("Hủy")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)

        main_layout.addLayout(button_layout)

    def load_account_data(self):
        """
        Tải thông tin tài khoản vào form
        """
        if not self.employee_id:
            self.delete_btn.setEnabled(False)
            return

        self.account = AccountDAO.get_account_by_employee_id(self.employee_id)

        if self.account:
            self.username_txt.setText(self.account.username)
            # Không hiển thị mật khẩu, để trống để người dùng nhập mới nếu muốn đổi
            self.role_combo.setCurrentText(self.account.role)
            self.active_check.setChecked(self.account.is_active)
        else:
            self.delete_btn.setEnabled(False)

    def save_account(self):
        """
        Lưu thông tin tài khoản
        """
        username = self.username_txt.text().strip()
        password = self.password_txt.text().strip()
        role = self.role_combo.currentText()
        is_active = self.active_check.isChecked()

        if not username:
            QtWidgets.QMessageBox.critical(
                self,
                "Lỗi",
                "Vui lòng nhập tên đăng nhập!"
            )
            return

        if not self.account and not password:
            QtWidgets.QMessageBox.critical(
                self,
                "Lỗi",
                "Vui lòng nhập mật khẩu cho tài khoản mới!"
            )
            return

        if self.account:
            # Cập nhật tài khoản hiện có
            self.account.username = username
            if password:  # Chỉ cập nhật mật khẩu nếu có nhập mới
                self.account.password = password  # Trong thực tế cần mã hóa mật khẩu
            self.account.role = role
            self.account.is_active = is_active

            success = AccountDAO.update_account(self.account)
            if success:
                QtWidgets.QMessageBox.information(
                    self,
                    "Thành công",
                    "Đã cập nhật thông tin tài khoản."
                )
                self.accept()
            else:
                QtWidgets.QMessageBox.critical(
                    self,
                    "Lỗi",
                    "Không thể cập nhật tài khoản!"
                )
        else:
            # Tạo tài khoản mới
            new_account = Account(
                username=username,
                password=password,  # Trong thực tế cần mã hóa mật khẩu
                id_emp=self.employee_id,
                role=role,
                is_active=is_active
            )

            success = AccountDAO.add_account(new_account)
            if success:
                QtWidgets.QMessageBox.information(
                    self,
                    "Thành công",
                    "Đã tạo tài khoản mới."
                )
                self.accept()
            else:
                QtWidgets.QMessageBox.critical(
                    self,
                    "Lỗi",
                    "Không thể tạo tài khoản mới!"
                )

    def delete_account(self):
        """
        Xóa tài khoản
        """
        if not self.account:
            return

        confirm = QtWidgets.QMessageBox.question(
            self,
            "Xác nhận xóa",
            "Bạn có chắc chắn muốn xóa tài khoản này không?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if confirm == QtWidgets.QMessageBox.Yes:
            success = AccountDAO.delete_account(self.account.id_account)
            if success:
                QtWidgets.QMessageBox.information(
                    self,
                    "Thành công",
                    "Đã xóa tài khoản."
                )
                self.accept()
            else:
                QtWidgets.QMessageBox.critical(
                    self,
                    "Lỗi",
                    "Không thể xóa tài khoản!"
                )
