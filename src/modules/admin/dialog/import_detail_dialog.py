# app/admin/dialog/import_detail_dialog.py

from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QMessageBox, QHeaderView
from PyQt5.QtCore import Qt, QTimer, QEvent
from src.modules.admin.ui.ui_py.import_detail import Ui_Form
from src.database.DAO.admin.ImportDetailDAO import NhapHangDAO

class ImportDetailDialog(QDialog):
    def __init__(self, id_imp, parent=None):
        super(ImportDetailDialog, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.id_imp = id_imp

        self.setWindowTitle("Chi tiết phiếu nhập")
        self.setModal(True)

        self.setup_table()

        if hasattr(self.ui, 'dong_btn'):
            self.ui.dong_btn.clicked.connect(self.close)

        self.load_import_detail()

    def setup_table(self):
        """Cấu hình bảng để tự động điều chỉnh kích thước theo màn hình."""
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        total_width = self.ui.tableWidget.viewport().width()
        ratios = [0.15, 0.30, 0.15, 0.20, 0.20]
        for col, ratio in enumerate(ratios):
            width = int(total_width * ratio)
            self.ui.tableWidget.setColumnWidth(col, width)
        self.ui.tableWidget.setAlternatingRowColors(True)
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.tableWidget.viewport().installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Resize and source == self.ui.tableWidget.viewport():
            QTimer.singleShot(0, self.setup_table)
        return super().eventFilter(source, event)

    def load_import_detail(self):
        """Tải thông tin chi tiết phiếu nhập"""
        try:
            nhap_hang = NhapHangDAO.get_nhap_hang_by_id(self.id_imp)
            if nhap_hang:
                self.ui.lineEdit.setText(str(nhap_hang.id_imp))
                self.ui.lineEdit_2.setText(str(nhap_hang.id_emp))
                self.ui.lineEdit_3.setText(nhap_hang.employee_name)
                self.ui.lineEdit_6.setText(f"{nhap_hang.total_price:,.0f} VNĐ")
                self.ui.lineEdit_7.setText(nhap_hang.date.strftime('%d/%m/%Y %H:%M:%S'))
                self.load_import_products(nhap_hang.chi_tiet_list)
            else:
                QMessageBox.warning(
                    self,
                    "Cảnh báo",
                    f"Không tìm thấy phiếu nhập có ID: {self.id_imp}",
                    QMessageBox.Ok
                )
        except Exception as e:
            pass

    def load_import_products(self, chi_tiet_list):
        """Hiển thị danh sách sản phẩm trong phiếu nhập"""
        self.ui.tableWidget.setRowCount(0)
        for row, chi_tiet in enumerate(chi_tiet_list):
            self.ui.tableWidget.insertRow(row)
            id_item = QTableWidgetItem(str(chi_tiet.id_prod) if chi_tiet.id_prod is not None else "")
            name_item = QTableWidgetItem(chi_tiet.product_name if chi_tiet.product_name is not None else "")
            qty_item = QTableWidgetItem(str(chi_tiet.quantity) if chi_tiet.quantity is not None else "")
            price_item = QTableWidgetItem(f"{chi_tiet.price:,.0f} VNĐ" if chi_tiet.price is not None else "")
            subtotal_item = QTableWidgetItem(f"{chi_tiet.sub_total:,.0f} VNĐ" if chi_tiet.sub_total is not None else "")
            id_item.setTextAlignment(Qt.AlignCenter)
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            qty_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            subtotal_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.ui.tableWidget.setItem(row, 0, id_item)
            self.ui.tableWidget.setItem(row, 1, name_item)
            self.ui.tableWidget.setItem(row, 2, qty_item)
            self.ui.tableWidget.setItem(row, 3, price_item)
            self.ui.tableWidget.setItem(row, 4, subtotal_item)