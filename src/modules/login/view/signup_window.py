from PyQt5.QtWidgets import QMainWindow, QMessageBox
from src.modules.login.ui.ui_py.sign_up import Ui_Main_log
from src.modules.login.data.login_data import LoginData


class SignupWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SignupWindow, self).__init__(parent)
        self.ui = Ui_Main_log()
        self.ui.setupUi(self)
        self.parent = parent  # Lưu tham chiếu đến cửa sổ cha (LoginWindow)

        self.ui.signup_btn.clicked.connect(self.handle_signup)
        self.ui.back_btn.clicked.connect(self.handle_back)

    def handle_signup(self):
        """Xử lý sự kiện khi nhấn nút Đăng ký"""
        try:
            sdt_email = self.ui.sdt_email_line.text().strip()
            username = self.ui.username_line.text().strip()
            password = self.ui.password_line.text().strip()
            confirm_password = self.ui.cpass_line.text().strip()

            valid, message = LoginData.validate_signup_data(sdt_email, username, password, confirm_password)
            if not valid:
                QMessageBox.warning(self, "Lỗi đăng ký", message)
                return

            success, message = LoginData.register_user(sdt_email, username, password)

            if success:
                QMessageBox.information(self, "Thành công", message)
                self.handle_back()
            else:
                QMessageBox.critical(self, "Lỗi đăng ký", message)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi đăng ký: {str(e)}")

    def handle_back(self):
        """Quay lại màn hình đăng nhập"""
        try:
            if self.parent:
                self.parent.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi quay lại: {str(e)}")
