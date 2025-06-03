from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QPushButton
from src.modules.login.ui.ui_py.login import Ui_Main_log
from src.modules.login.view.signup_window import SignupWindow
from src.modules.login.data.login_data import LoginData
from src.modules.admin.views.admin_window import AdminWindow
import os

class LoginWindow(QMainWindow):
    def __init__(self, authenticate_callback=None):
        super(LoginWindow, self).__init__()
        self.ui = Ui_Main_log()
        self.ui.setupUi(self)
        self.authenticate_callback = authenticate_callback
        self.signup_window = None
        self.admin_window = None

        self.setup_password_toggle_button()
        self.ui.login_btn.clicked.connect(self.handle_login)
        self.ui.register_btn.mousePressEvent = self.handle_register

    def setup_password_toggle_button(self):
        try:
            self.password_toggle_btn = QPushButton(self.ui.centralwidget)
            self.password_toggle_btn.setObjectName("password_toggle_btn")
            self.password_toggle_btn.setFixedSize(30, 30)
            self.password_toggle_btn.setVisible(True)

            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            eye_icon_path = os.path.join(base_dir, "login","ui", "ui_design", "icon", "visible-xxl (1).png")
            eye_slash_icon_path = os.path.join(base_dir, "login","ui", "ui_design", "icon", "visible-xxl.png")

            if os.path.exists(eye_icon_path):
                self.eye_icon = QIcon(eye_icon_path)
            else:
                print(f"Không tìm thấy icon tại: {eye_icon_path}")
                self.eye_icon = QIcon()

            if os.path.exists(eye_slash_icon_path):
                self.eye_slash_icon = QIcon(eye_slash_icon_path)
            else:
                print(f"Không tìm thấy icon tại: {eye_slash_icon_path}")
                self.eye_slash_icon = QIcon()

            self.password_toggle_btn.setIcon(self.eye_icon)
            self.password_toggle_btn.setIconSize(QSize(20, 20))
            self.password_toggle_btn.setStyleSheet("background-color: transparent")

            self.password_toggle_btn.setGeometry(QtCore.QRect(
                self.ui.password_line.x() + self.ui.password_line.width() + 660,
                self.ui.password_line.y() + 395,
                30, 30
            ))

            self.password_toggle_btn.clicked.connect(self.toggle_password_visibility)
            self.password_is_visible = False
        except Exception as e:
            print(f"Lỗi khi thiết lập nút toggle password: {e}")

    def handle_login(self):
        username = self.ui.username_line.text()
        password = self.ui.password_line.text()

        success, message, user_info = LoginData.validate_login(username, password)
        if success and user_info:
            QMessageBox.information(self, "Thành công", message)
            account_id = user_info['account_id']
            print(f"Login successful, account_id: {account_id}")  # Log kiểm tra
            self.admin_window = AdminWindow(account_id=account_id)
            self.admin_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Thất bại", message)

    def handle_register(self, event):
        try:
            self.signup_window = SignupWindow(self)
            self.signup_window.show()
            self.hide()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi mở cửa sổ đăng ký: {str(e)}")

    def toggle_password_visibility(self):
        try:
            if self.password_is_visible:
                self.ui.password_line.setEchoMode(2)
                self.password_toggle_btn.setIcon(self.eye_icon)
                self.password_is_visible = False
            else:
                self.ui.password_line.setEchoMode(0)
                self.password_toggle_btn.setIcon(self.eye_slash_icon)
                self.password_is_visible = True
        except Exception as e:
            print(f"Lỗi khi chuyển đổi hiển thị mật khẩu: {e}")