from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QMessageBox
from src.database.DAO.common.BillDAO import BillDAO
from src.modules.admin.dialog.bill_detail_dialog import BillDetailDialog  # Tái sử dụng từ admin

def load_bill_data(table, employee_id, parent=None):
    """
    Tải dữ liệu hóa đơn của nhân viên đang đăng nhập vào bảng giao diện
    """
    bill_dao = BillDAO()

    # Lấy danh sách hóa đơn của nhân viên đang đăng nhập
    bills = bill_dao.get_bills_by_employee(employee_id)

    table.setRowCount(0)  # Xóa dữ liệu cũ

    for bill in bills:
        row_position = table.rowCount()
        table.insertRow(row_position)

        table.setItem(row_position, 0, QTableWidgetItem(str(bill['id_bill'])))
        table.setItem(row_position, 1, QTableWidgetItem(bill['customer_name']))
        table.setItem(row_position, 2, QTableWidgetItem(bill['employee_name']))
        table.setItem(row_position, 3, QTableWidgetItem(f"{bill['total']:,} VNĐ"))
        table.setItem(row_position, 4, QTableWidgetItem(bill['date'].strftime('%Y-%m-%d %H:%M:%S') if bill['date'] else ""))

        # Thêm nút Xem chi tiết
        detail_button = QPushButton('Xem chi tiết')
        detail_button.setStyleSheet("background-color: #2196F3; color: white; border-radius: 5px; padding: 2px;")
        detail_button.clicked.connect(lambda _, r=row_position, id=bill['id_bill']: view_bill_details(id, parent))

        # Tạo một widget để chứa nút
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.addWidget(detail_button)
        button_layout.setContentsMargins(0, 0, 0, 0)  # Loại bỏ khoảng cách

        # Thêm widget vào cột thứ 5
        table.setCellWidget(row_position, 5, button_widget)

def view_bill_details(bill_id, parent):
    """
    Hiển thị dialog chi tiết hóa đơn
    """
    dialog = BillDetailDialog(bill_id, parent)
    dialog.exec_()