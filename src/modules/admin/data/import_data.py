from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from src.database.DAO.admin.ImportDAO import NhapHangDAO


def show_chi_tiet(phieu_id, parent=None):
    """
    Xử lý sự kiện khi nhấn nút Xem chi tiết

    Args:
        phieu_id: ID của phiếu nhập
        parent: Widget cha (để dialog có parent)
    """
    try:
        from src.modules.admin.dialog.import_detail_dialog import ImportDetailDialog
        dialog = ImportDetailDialog(phieu_id, parent)
        dialog.exec_()
    except Exception as e:
        pass


def delete_phieu_nhap(table, row, phieu_id):
    """
    Xử lý sự kiện khi nhấn nút Xóa phiếu nhập

    Args:
        table: QTableWidget chứa dữ liệu
        row: Dòng được chọn
        phieu_id: ID của phiếu nhập
    """
    reply = QMessageBox.question(
        None,
        'Xác nhận xóa',
        f'Bạn có chắc chắn muốn xóa phiếu nhập có ID: {phieu_id}?',
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )

    if reply == QMessageBox.Yes:
        success = NhapHangDAO.delete_phieu_nhap(phieu_id)

        if success:
            table.removeRow(row)
            QMessageBox.information(None, 'Thành công', 'Đã xóa phiếu nhập thành công!')
        else:
            QMessageBox.warning(None, 'Lỗi', 'Không thể xóa phiếu nhập!')


def load_data_to_table_nhap(table, parent=None):
    """
    Tải dữ liệu phiếu nhập từ database lên bảng
    """
    phieu_nhap_list = NhapHangDAO.get_all_phieu_nhap()
    table.setRowCount(0)

    for row, phieu_nhap in enumerate(phieu_nhap_list):
        table.insertRow(row)

        item = QTableWidgetItem(str(phieu_nhap.id_imp) if phieu_nhap.id_imp is not None else "")
        item.setTextAlignment(Qt.AlignCenter)
        table.setItem(row, 0, item)

        item = QTableWidgetItem(str(phieu_nhap.id_emp) if phieu_nhap.id_emp is not None else "")
        item.setTextAlignment(Qt.AlignCenter)
        table.setItem(row, 1, item)

        item = QTableWidgetItem(str(phieu_nhap.employee_name) if phieu_nhap.employee_name is not None else "")
        item.setTextAlignment(Qt.AlignCenter)
        table.setItem(row, 2, item)

        item = QTableWidgetItem(str(phieu_nhap.date) if phieu_nhap.date is not None else "")
        item.setTextAlignment(Qt.AlignCenter)
        table.setItem(row, 3, item)

        item = QTableWidgetItem(str(phieu_nhap.total_price) if phieu_nhap.total_price is not None else "")
        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        table.setItem(row, 4, item)

        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)

        btn_detail = QPushButton("Xem chi tiết")
        btn_detail.setStyleSheet("background-color: #2196F3; color: white; border-radius: 5px; padding: 2px;")

        phieu_id = phieu_nhap.id_imp
        btn_detail.clicked.connect(lambda checked, pid=phieu_id: show_chi_tiet(pid, parent))

        layout.addWidget(btn_detail)
        widget.setLayout(layout)

        table.setCellWidget(row, 5, widget)

    # Bật lại chế độ sắp xếp
    table.setSortingEnabled(True)
