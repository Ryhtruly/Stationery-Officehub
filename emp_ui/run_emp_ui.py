from PyQt5.QtWidgets import QStackedWidget, QMainWindow, QApplication, QPushButton, QLabel, QVBoxLayout, QWidget, \
    QMessageBox
import sys
from PyQt5.QtCore import pyqtSignal, Qt

from emp_ui import Ui_MainWindow
from run_log import LoginWindow


class AdminWindow(QMainWindow):
    def __init__(self):
        super(AdminWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.full_menu.hide()

        self.ui.stackedWidget.setCurrentIndex(0)

        self.ui.home_nbtn_1.clicked.connect(self.on_home_btn_1)
        self.ui.product_btn_1.clicked.connect(self.on_product_btn_1)
        self.ui.customer_btn_1.clicked.connect(self.on_customer_btn_1)

        self.ui.home_btn_2.clicked.connect(self.on_home_btn_2)
        self.ui.product_btn_2.clicked.connect(self.on_product_btn_2)
        self.ui.cusomer_btn_2.clicked.connect(self.on_customer_btn_2)


        self.ui.search_btn.clicked.connect(self.on_search_btn_clicked)
        self.ui.user_btn.clicked.connect(self.on_user_btn_clicked)

        self.ui.home_btn_2.setChecked(True)

        self.ui.logo_label = QLabel("Stationery Store")
        self.ui.logo_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        self.ui.header_layout = self.ui.widget.layout()
        self.ui.header_layout.insertWidget(1, self.ui.logo_label)



    def on_search_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        search_text = self.ui.lineEdit.text().strip()
        if hasattr(self.ui, 'search_output'):
            self.ui.search_output.setText(f" {search_text}")


    def on_user_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(5)

    def on_stackedWidget_curentChanged(self, index):
        btn_list = self.ui.icon_only.findChildren(QPushButton) \
                   + self.ui.full_menu.findChildren(QPushButton)
        for btn in btn_list:
            if index in [4, 5]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)
                btn.setChecked(True)

    def on_home_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_home_btn_2(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_product_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_product_btn_2(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_customer_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_customer_btn_2(self):
        self.ui.stackedWidget.setCurrentIndex(2)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("style.qss", "r", encoding="utf-8") as style_file:
        style_str = style_file.read()

    app.setStyleSheet(style_str)
    main_app = AdminWindow()
    main_app.show()
    sys.exit(app.exec_())