from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QMessageBox, QComboBox
from src.database.DAO.common.BillDAO import BillDAO
from src.modules.admin.dialog.bill_detail_dialog import BillDetailDialog  # Import dialog mới


def load_bill_data(table, parent=None):
    """
    Tải dữ liệu hóa đơn từ database vào bảng giao diện
    """
    bill_dao = BillDAO()

    id_emp = None
    if parent and hasattr(parent, 'ui') and hasattr(parent.ui, 'cbb_tennhanvien'):
        id_emp = parent.ui.cbb_tennhanvien.currentData()

    # Lấy danh sách hóa đơn
    if id_emp:
        bills = bill_dao.get_bills_by_employee(id_emp)
    else:
        bills = bill_dao.get_all_bills()

    table.setRowCount(0)

    for bill in bills:
        row_position = table.rowCount()
        table.insertRow(row_position)

        table.setItem(row_position, 0, QTableWidgetItem(str(bill['id_bill'])))
        table.setItem(row_position, 1, QTableWidgetItem(bill['customer_name']))
        table.setItem(row_position, 2, QTableWidgetItem(bill['employee_name']))
        table.setItem(row_position, 3, QTableWidgetItem(f"{bill['total']:,} VNĐ"))
        table.setItem(row_position, 4,
                      QTableWidgetItem(bill['date'].strftime('%Y-%m-%d %H:%M:%S') if bill['date'] else ""))

        detail_button = QPushButton('Xem chi tiết')

        detail_button.clicked.connect(lambda _, r=row_position, id=bill['id_bill']: view_bill_details(id, parent))
        detail_button.setStyleSheet("""
                   QPushButton {
                       background-color: #3498db;
                       color: white;
                       border: none;
                       border-radius: 5px;
                       padding: 5px 10px;
                   }
                   QPushButton:hover {
                       background-color: #2980b9;
                   }
               """)

        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.addWidget(detail_button)
        button_layout.setContentsMargins(0, 0, 0, 0)
        table.setCellWidget(row_position, 5, button_widget)


def load_employees_to_combobox(combobox):
    """
    Load danh sách nhân viên vào QComboBox
    """
    bill_dao = BillDAO()
    employees = bill_dao.get_all_employees()

    combobox.addItem("Tất cả nhân viên", None)

    for employee in employees:
        combobox.addItem(employee['hoten'], employee['id'])


def view_bill_details(bill_id, parent):
    """
    Hiển thị dialog chi tiết hóa đơn
    """
    dialog = BillDetailDialog(bill_id, parent)
    dialog.exec_()


