from PyQt5.QtWidgets import QStackedWidget, QMainWindow, QApplication, QPushButton, QLabel, QVBoxLayout, QWidget, \
    QMessageBox
import sys
from PyQt5.QtCore import pyqtSignal, Qt

from new_dashboard import Ui_MainWindow
from run_log import LoginWindow




class AdminWindow(QMainWindow):
    def __init__(self):
        super(AdminWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.Full_menu.hide()

        self.ui.stackedWidget.setCurrentIndex(0)

        self.ui.home_btn_1.clicked.connect(self.on_home_btn_1)
        self.ui.dasboard_btn_1.clicked.connect(self.on_dashboard_btn_1)
        self.ui.product_btn_1.clicked.connect(self.on_product_btn_1)
        self.ui.orders_btn_1.clicked.connect(self.on_orders_btn_1)
        self.ui.employee_btn_1.clicked.connect(self.on_employee_btn_1)

        self.ui.home_btn_2.clicked.connect(self.on_home_btn_1)
        self.ui.dboaoboard_btn_2.clicked.connect(self.on_dashboard_btn_1)
        self.ui.product_btn_2.clicked.connect(self.on_product_btn_1)
        self.ui.orders_btn_2.clicked.connect(self.on_orders_btn_1)
        self.ui.employee_btn_2.clicked.connect(self.on_employee_btn_1)

        self.ui.Search.clicked.connect(self.on_search_btn_clicked)
        self.ui.Account.clicked.connect(self.on_user_btn_clicked)

        self.ui.home_btn_2.setChecked(True)

        self.ui.logo_label = QLabel("Stationery Store")
        self.ui.logo_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        self.ui.header_layout = self.ui.widget.layout()
        self.ui.header_layout.insertWidget(1, self.ui.logo_label)

        # Đặt nền trong suốt
        self.setAttribute(Qt.WA_TranslucentBackground)

    def on_search_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        search_text = self.ui.Search_input.text().strip()
        if search_text:
            self.ui.pushButton_6.setText(search_text)

    def on_user_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(6)

    def on_stackedWidget_curentChanged(self, index):
        btn_list = self.ui.icon_only.findChildren(QPushButton) \
                   + self.ui.Full_menu.findChildren(QPushButton)
        for btn in btn_list:
            if index in [5, 6]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)
                btn.setChecked(True)

    def on_home_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_home_btn_12(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_dashboard_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_dashboard_btn_2(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_product_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_product_btn_2(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_orders_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_orders_btn_2(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_employee_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def on_employee_btn_2(self):
        self.ui.stackedWidget.setCurrentIndex(4)


class MainApp(QStackedWidget):
    def __init__(self):
        super(MainApp, self).__init__()
        self.setGeometry(410, 140, 1100, 800)

        self.setObjectName("MainWindow")

        self.login_window = LoginWindow()
        self.dashboard_window = AdminWindow()

        self.login_window.setAttribute(Qt.WA_TranslucentBackground)

        self.addWidget(self.login_window)  # Index 0
        self.addWidget(self.dashboard_window)  # Index 1

        self.login_window.login_successful.connect(self.show_dashboard)
        self.setCurrentIndex(0)

    def show_dashboard(self):
        self.setCurrentIndex(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("style.qss", "r", encoding="utf-8") as style_file:
        style_str = style_file.read()

    app.setStyleSheet(style_str)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
