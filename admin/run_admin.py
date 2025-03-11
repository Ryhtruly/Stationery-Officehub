from PyQt5.QtWidgets import QStackedWidget, QMainWindow, QApplication, QPushButton, QLabel, QVBoxLayout, QWidget, \
    QMessageBox
import sys
from PyQt5.QtCore import pyqtSignal, Qt

from admin_page import Ui_MainWindow
from run_log import LoginWindow


class AdminWindow(QMainWindow):
    def __init__(self):
        super(AdminWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.Full_menu.hide()

        self.ui.stackedWidget.setCurrentIndex(0)

        self.ui.product_btn_1.clicked.connect(self.on_product_btn_1)
        self.ui.warehouse_btn_1.clicked.connect(self.on_warehouse_btn_1)
        self.ui.emp_btn_1.clicked.connect(self.on_emp_btn_1)
        self.ui.statistics_btn_1.clicked.connect(self.on_statistics_btn_1)
        self.ui.promotion_btn_1.clicked.connect(self.on_promotion_btn_1)

        self.ui.product_btn_2.clicked.connect(self.on_product_btn_2)
        self.ui.warehouse_btn_2.clicked.connect(self.on_warehouse_btn_2)
        self.ui.emp_btn_2.clicked.connect(self.on_emp_btn_2)
        self.ui.statistic_btn_2.clicked.connect(self.on_statistic_btn_2)
        self.ui.promotion_btn_2.clicked.connect(self.on_promotion_btn_2)

        self.ui.Search.clicked.connect(self.on_search_btn_clicked)
        self.ui.Account.clicked.connect(self.on_user_btn_clicked)

        self.ui.product_btn_2.setChecked(True)

        self.ui.logo_label = QLabel("Stationery Store")
        self.ui.logo_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        self.ui.header_layout = self.ui.widget.layout()
        self.ui.header_layout.insertWidget(1, self.ui.logo_label)



    def on_search_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        search_text = self.ui.Search_input.text().strip()
        if search_text:
            self.ui.pushButton_6.setText(search_text)

    def on_user_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(5)

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

    def on_product_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_product_btn_2(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_warehouse_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_warehouse_btn_2(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_emp_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_emp_btn_2(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_statistics_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_statistic_btn_2(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_promotion_btn_1(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def on_promotion_btn_2(self):
        self.ui.stackedWidget.setCurrentIndex(4)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("style.qss", "r", encoding="utf-8") as style_file:
        style_str = style_file.read()

    app.setStyleSheet(style_str)
    main_app = AdminWindow()
    main_app.show()
    sys.exit(app.exec_())