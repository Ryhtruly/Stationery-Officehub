from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QMessageBox
from src.database.DAO.employee.CustomerDAO import CustomerDAO

def edit_item(sender_button, customer_id):
    try:
        from PyQt5.QtWidgets import QApplication
        main_window = QApplication.activeWindow()

        from src.modules.employee.events.add_customer_handler import CustomerHandler
        handler = CustomerHandler(main_window)
        handler.show_edit_customer_dialog(customer_id)
    except Exception as e:
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(None, "Lỗi", f"Đã xảy ra lỗi khi sửa khách hàng: {str(e)}")
        import traceback
        traceback.print_exc()

def delete_item(row, customer_id):
    """
    Xử lý sự kiện khi nhấn nút Xóa

    Args:
        row: Dòng được chọn
        customer_id: ID của khách hàng
    """
    reply = QMessageBox.question(
        None,
        'Xác nhận',
        f'Bạn có chắc chắn muốn xóa khách hàng này không?',
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )

    if reply == QMessageBox.Yes:
        try:
            success, message = CustomerDAO.delete_customer(customer_id)

            if success:
                parent_widget = row.parent()
                if hasattr(parent_widget, 'tb_customer'):
                    load_data_to_customer_tb(parent_widget.tb_customer)
                QMessageBox.information(None, "Thông báo", message)
            else:
                QMessageBox.warning(None, "Cảnh báo", message)

        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Đã xảy ra lỗi khi xóa khách hàng: {str(e)}")

def load_data_to_customer_tb(table):
    """
    Load dữ liệu vào bảng khách hàng

    Args:
        table: Bảng cần load dữ liệu
    """
    try:
        customers = CustomerDAO.get_all_customers()

        table.setRowCount(0)

        for i, customer in enumerate(customers):
            table.insertRow(i)

            # ID
            table.setItem(i, 0, QTableWidgetItem(str(customer.id_cust)))

            # Tên
            table.setItem(i, 1, QTableWidgetItem(customer.fullname))

            # Số điện thoại
            table.setItem(i, 2, QTableWidgetItem(customer.phone))

            # Rank
            table.setItem(i, 3, QTableWidgetItem(customer.rank))

            # Ngày đăng ký
            table.setItem(i, 4, QTableWidgetItem(str(customer.register_date)))

            # Tạo nút Sửa và Xóa
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.setContentsMargins(0, 0, 0, 0)

            # Nút Sửa
            btn_edit = QPushButton("Sửa")
            btn_edit.setStyleSheet("background-color: #2196F3; color: white; border-radius: 5px; padding: 2px;")
            btn_edit.clicked.connect(lambda checked, row=table, cid=customer.id_cust: edit_item(row, cid))
            layout.addWidget(btn_edit)



            table.setCellWidget(i, 5, widget)

    except Exception as e:
        QMessageBox.critical(None, "Lỗi", f"Đã xảy ra lỗi khi load dữ liệu: {str(e)}")

def get_customer_by_phone(phone, connection):
    """
    Lấy thông tin khách hàng dựa trên số điện thoại

    Args:
        phone (str): Số điện thoại của khách hàng
        connection: Đối tượng kết nối cơ sở dữ liệu

    Returns:
        dict: Thông tin khách hàng (id_cust, fullname, phone, rank, register_date) hoặc None nếu không tìm thấy
    """
    return CustomerDAO.get_customer_by_phone(phone, connection)