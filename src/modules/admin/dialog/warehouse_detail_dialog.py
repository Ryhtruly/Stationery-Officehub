from PyQt5 import QtWidgets
from src.modules.admin.ui.ui_py.warehouse_detail import Ui_Form

class WareHouseDetailDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(WareHouseDetailDialog,self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.setWindowTitle("Thông tin kho")
        self.setModal(True)

def run_warehouseDetail_dialog(parent = None):
    dialog = WareHouseDetailDialog(parent)
    result = dialog.exec_()

    if result == QtWidgets.QDialog.Accepted:
        return True, dialog.get_category_data()
    else:
        return False, (None, None)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    success, (category_id, category_name) = run_warehouseDetail_dialog()


