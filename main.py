from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
import sys
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
from numpy.ma.core import append

from new_dashboard import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.Full_menu.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.Home_2.setChecked(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())