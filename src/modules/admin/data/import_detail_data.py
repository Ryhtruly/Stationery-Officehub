
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from src.database.models.import_product import NhapHang
from src.database.models.import_detail import ChiTietNhapHang
from src.database.DAO.admin.ImportDetailDAO  import NhapHangDAO
from src.modules.admin.dialog.import_detail_dialog import ImportDetailDialog

def load_import_data(table, parent=None):
    """
    Tải dữ liệu phiếu nhập từ database lên bảng
    """
    # Lấy danh sách phiếu nhập
    nhap_hang_list = NhapHangDAO.get_all_nhap_hang()

    # Xóa tất cả dữ liệu hiện có trong bảng
    table.setRowCount(0)

    # Thêm dữ liệu vào bảng
    for row, nhap_hang in enumerate(nhap_hang_list):
        table.insertRow(row)

        table.setItem(row, 0, QTableWidgetItem(str(nhap_hang.id_imp)))
        table.setItem(row, 1, QTableWidgetItem(str(nhap_hang.id_emp)))
        table.setItem(row, 2, QTableWidgetItem(nhap_hang.employee_name))
        table.setItem(row, 3, QTableWidgetItem(nhap_hang.date.strftime('%d/%m/%Y %H:%M:%S')))
        table.setItem(row, 4, QTableWidgetItem(f"{nhap_hang.total_price:,.0f} VNĐ"))

        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        btn_layout.setContentsMargins(0, 0, 0, 0)

        detail_btn = QPushButton("Xem chi tiết")
        detail_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(180, 150, 255, 0.3); /* Tím nhạt trong suốt */
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: rgba(180, 150, 255, 0.5);
                border: 1px solid rgba(180, 150, 255, 0.7);
                color: white;
            }
            QPushButton:pressed {
                background-color: rgba(180, 150, 255, 0.7);
                border: 1px solid rgba(180, 150, 255, 0.9);
                box-shadow: 0 0 8px rgba(180, 150, 255, 0.5);
                color: white;
            }
        """)
        detail_btn.clicked.connect(lambda checked, id=nhap_hang.id_imp: show_import_detail(id, parent))

        btn_layout.addWidget(detail_btn)
        btn_layout.setAlignment(Qt.AlignCenter)
        table.setCellWidget(row, 5, btn_widget)

def show_import_detail(id_imp, parent=None):
    """
    Hiển thị dialog chi tiết phiếu nhập
    """
    dialog = ImportDetailDialog(id_imp, parent)
    dialog.exec_()

def them_phieu_nhap(nhap_hang, chi_tiet_list):
    """
    Thêm phiếu nhập mới vào database
    """
    try:
        result = NhapHangDAO.them_phieu_nhap(nhap_hang, chi_tiet_list)
        return result
    except Exception as e:
        print(f"Lỗi khi thêm phiếu nhập: {str(e)}")
        return False