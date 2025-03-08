from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal
from login import Ui_Main_log
import sys

class LoginWindow(QMainWindow):
    # Tín hiệu để thông báo khi đăng nhập thành công
    login_successful = pyqtSignal()

    def __init__(self):
        super(LoginWindow, self).__init__()
        self.ui = Ui_Main_log()
        self.ui.setupUi(self)

        self.center_window()

        self.ui.pushButton.clicked.connect(self.check_login)



    def center_window(self):
        """Căn giữa cửa sổ"""
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def check_login(self):
        # Lấy thông tin từ các trường nhập liệu
        username = self.ui.lineEdit.text()  # Tên trường nhập username là "lineEdit"
        password = self.ui.lineEdit_2.text()  # Tên trường nhập password là "lineEdit_2"

        # Kiểm tra tài khoản và mật khẩu
        if username == "admin" and password == "1234":
            QMessageBox.information(self, "Login", "Đăng nhập thành công!")
            self.login_successful.emit()  # Phát tín hiệu đăng nhập thành công
        else:
            QMessageBox.warning(self, "Login", "Sai tài khoản hoặc mật khẩu!")


if __name__ == "__main__":
    # Khởi tạo ứng dụng PyQt5
    app = QApplication(sys.argv)

    # Tạo cửa sổ đăng nhập
    login_window = LoginWindow()
    login_window.show()

    # Chạy vòng lặp sự kiện
    sys.exit(app.exec_())
