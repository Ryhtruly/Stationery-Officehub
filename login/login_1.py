from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame
from PyQt5.QtGui import QPixmap
import sys
import os


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 1100, 800)  # Cập nhật vị trí và kích thước cửa sổ
        self.initUI()

    def initUI(self):
        self.background = QtWidgets.QLabel(self)
        self.background.setGeometry(0, 0, 1100, 800)  # Cập nhật vị trí và kích thước background
        bg_path = os.path.join('assets', 'background_login.png')
        pixmap = QPixmap(bg_path)
        self.background.setPixmap(pixmap.scaled(1100, 800))
        self.background.lower()
        self.login_frame = QFrame(self)
        self.login_frame.setGeometry(300, 200, 500, 400)  # Điều chỉnh lại frame login
        self.login_frame.setStyleSheet("""
                    QFrame {
                        background-color: rgba(255, 255, 255, 0.7);  
                        border-radius: 20px;
                        border: 2px solid rgba(255, 255, 255, 0.3);
                    }
                """)
        self.lbl_welcome = QtWidgets.QLabel(self)
        self.lbl_welcome.setText("YO!")
        self.lbl_welcome.move(450, 220)
        self.lbl_welcome.resize(200, 40)
        self.lbl_welcome.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                qproperty-alignment: AlignCenter;
                font-family: 'Arial';
                background-color: rgba(255, 255, 255, 0.7);
                -webkit-background-clip: text;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        self.lbl_username = QtWidgets.QLabel(self)
        self.lbl_username.setText("Username : ")
        self.lbl_username.move(370, 300)
        self.lbl_username.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #333333;
                font-weight: bold;
            }
        """)

        self.txt_username = QtWidgets.QLineEdit(self)
        self.txt_username.move(460, 300)
        self.txt_username.resize(300, 40)
        self.txt_username.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                background-color: rgba(255, 255, 255, 0.8);
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        self.lbl_password = QtWidgets.QLabel(self)
        self.lbl_password.setText("Password : ")
        self.lbl_password.move(370, 380)
        self.lbl_password.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #333333;
                font-weight: bold;
            }
        """)

        self.txt_password = QtWidgets.QLineEdit(self)
        self.txt_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_password.move(460, 380)
        self.txt_password.resize(300, 40)
        self.txt_password.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                background-color: rgba(255, 255, 255, 0.8);
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        self.btn_login = QtWidgets.QPushButton(self)
        self.btn_login.setText("Login")
        self.btn_login.move(460, 460)
        self.btn_login.resize(300, 50)
        self.btn_login.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        self.btn_login.clicked.connect(self.login)

    def login(self):
        username = self.txt_username.text()
        password = self.txt_password.text()

        if username == "admin" and password == "123456":
            QtWidgets.QMessageBox.information(self, "Thông báo", "Đăng nhập thành công!")
        else:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())