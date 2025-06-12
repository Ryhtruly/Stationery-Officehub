from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QHBoxLayout, QPushButton, QMessageBox, QDialog
from src.database.DAO.admin.EmployeeDAO import EmployeeDAO

def load_employee_data(table):
    """
    Tải dữ liệu nhân viên từ database lên bảng
    """
    nhan_vien_list = EmployeeDAO.get_all_nhan_vien()
    table.setRowCount(0)
    table.setRowCount(len(nhan_vien_list))
    for row, nhan_vien in enumerate(nhan_vien_list):
        # Lưu ID nhân viên để sử dụng trong các hàm callback
        employee_id = nhan_vien.id_emp

        # ID nhân viên
        table.setItem(row, 0, QTableWidgetItem(str(employee_id)))

        # Họ tên
        table.setItem(row, 1, QTableWidgetItem(nhan_vien.fullname))

        status_text = "Đang làm việc" if nhan_vien.status == 1 else "Đã nghỉ"
        status_item = QTableWidgetItem(status_text)
        table.setItem(row, 2, status_item)

        # Địa chỉ
        table.setItem(row, 3, QTableWidgetItem(nhan_vien.address))
        email_value = nhan_vien.email if nhan_vien.email else "NULL"
        table.setItem(row, 4, QTableWidgetItem(email_value))
        table.setItem(row, 5, QTableWidgetItem(nhan_vien.phone))
        table.setItem(row, 6, QTableWidgetItem(str(nhan_vien.salary)))
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 2, 5, 2)
        from functools import partial

        # Nút sửa
        edit_button = QPushButton("Sửa")
        edit_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(80, 200, 200, 0.3); /* Xanh ngọc trong suốt */
                color: white;
                border: none;
                border-radius: 4px;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: rgba(80, 200, 200, 0.5);
                border: 1px solid rgba(80, 200, 200, 0.7);
                color: white;
            }
            QPushButton:pressed {
                background-color: rgba(80, 200, 200, 0.7);
                border: 1px solid rgba(80, 200, 200, 0.9);
                box-shadow: 0 0 8px rgba(80, 200, 200, 0.5);
                color: white;
            }
        """)
        edit_button.clicked.connect(partial(edit_employee, table, employee_id))
        layout.addWidget(edit_button)

        # Nút xóa
        if nhan_vien.status == 1:
            delete_button = QPushButton("Dừng làm việc")
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 150, 150, 0.3); /* Hồng phấn trong suốt */
                    color: white;
                    border: none;
                    border-radius: 6px;
                    transition: all 0.3s ease;
                }
                QPushButton:hover {
                    background-color: rgba(255, 150, 150, 0.5);
                    border: 1px solid rgba(255, 150, 150, 0.7);
                    color: white;
                }
                QPushButton:pressed {
                    background-color: rgba(255, 150, 150, 0.7);
                    border: 1px solid rgba(255, 150, 150, 0.9);
                    box-shadow: 0 0 8px rgba(255, 150, 150, 0.5);
                    color: white;
                }
            """)
            delete_button.clicked.connect(partial(delete_employee, table, employee_id))
            layout.addWidget(delete_button)
        else:
            delete_button = QPushButton("Tái hoạt động")
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 150, 150, 0.3); /* Hồng phấn trong suốt */
                    color: white;
                    border: none;
                    border-radius: 6px;
                    transition: all 0.3s ease;
                }
                QPushButton:hover {
                    background-color: rgba(255, 150, 150, 0.5);
                    border: 1px solid rgba(255, 150, 150, 0.7);
                    color: white;
                }
                QPushButton:pressed {
                    background-color: rgba(255, 150, 150, 0.7);
                    border: 1px solid rgba(255, 150, 150, 0.9);
                    box-shadow: 0 0 8px rgba(255, 150, 150, 0.5);
                    color: white;
                }
            """)
            delete_button.clicked.connect(partial(delete_employee, table, employee_id))
            layout.addWidget(delete_button)

        widget.setLayout(layout)
        table.setCellWidget(row, 7, widget)

def search_employees(table, keyword):
    """
    Tìm kiếm nhân viên theo họ tên và hiển thị kết quả lên bảng

    Args:
        table: QTableWidget để hiển thị dữ liệu
        keyword: Từ khóa tìm kiếm
    """
    nhan_vien_list = EmployeeDAO.search_employees_by_name(keyword)
    table.setRowCount(0)

    if not keyword.strip():
        load_employee_data(table)
        return

    table.setRowCount(len(nhan_vien_list))

    # Đổ dữ liệu vào bảng
    for row, nhan_vien in enumerate(nhan_vien_list):
        # Lưu ID nhân viên để sử dụng trong các hàm callback
        employee_id = nhan_vien.id_emp

        # ID nhân viên
        table.setItem(row, 0, QTableWidgetItem(str(employee_id)))

        # Họ tên
        table.setItem(row, 1, QTableWidgetItem(nhan_vien.fullname))

        status_text = "Đang làm việc" if nhan_vien.status == 1 else "Đã nghỉ"
        status_item = QTableWidgetItem(status_text)
        table.setItem(row, 2, status_item)

        # Địa chỉ
        table.setItem(row, 3, QTableWidgetItem(nhan_vien.address))
        email_value = nhan_vien.email if nhan_vien.email else "NULL"
        table.setItem(row, 4, QTableWidgetItem(email_value))
        table.setItem(row, 5, QTableWidgetItem(nhan_vien.phone))

        # Lương
        table.setItem(row, 6, QTableWidgetItem(str(nhan_vien.salary)))
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # Sử dụng functools.partial thay vì lambda để tránh vấn đề với biến
        from functools import partial

        # Nút sửa
        edit_button = QPushButton("Sửa")
        edit_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(80, 200, 200, 0.3); /* Xanh ngọc trong suốt */
                color: white;
                border: none;
                border-radius: 4px;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: rgba(80, 200, 200, 0.5);
                border: 1px solid rgba(80, 200, 200, 0.7);
                color: white;
            }
            QPushButton:pressed {
                background-color: rgba(80, 200, 200, 0.7);
                border: 1px solid rgba(80, 200, 200, 0.9);
                box-shadow: 0 0 8px rgba(80, 200, 200, 0.5);
                color: white;
            }
        """)
        edit_button.clicked.connect(partial(edit_employee, table, employee_id))
        layout.addWidget(edit_button)

        # Nút xóa
        if nhan_vien.status == 1:
            delete_button = QPushButton("Dừng làm việc")
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 150, 150, 0.3); /* Hồng phấn trong suốt */
                    color: white;
                    border: none;
                    border-radius: 6px;
                    transition: all 0.3s ease;
                }
                QPushButton:hover {
                    background-color: rgba(255, 150, 150, 0.5);
                    border: 1px solid rgba(255, 150, 150, 0.7);
                    color: white;
                }
                QPushButton:pressed {
                    background-color: rgba(255, 150, 150, 0.7);
                    border: 1px solid rgba(255, 150, 150, 0.9);
                    box-shadow: 0 0 8px rgba(255, 150, 150, 0.5);
                    color: white;
                }
            """)
            delete_button.clicked.connect(partial(delete_employee, table, employee_id))
            layout.addWidget(delete_button)
        else:
            delete_button = QPushButton("Tái hoạt động")
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 150, 150, 0.3); /* Hồng phấn trong suốt */
                    color: white;
                    border: none;
                    border-radius: 6px;
                    transition: all 0.3s ease;
                }
                QPushButton:hover {
                    background-color: rgba(255, 150, 150, 0.5);
                    border: 1px solid rgba(255, 150, 150, 0.7);
                    color: white;
                }
                QPushButton:pressed {
                    background-color: rgba(255, 150, 150, 0.7);
                    border: 1px solid rgba(255, 150, 150, 0.9);
                    box-shadow: 0 0 8px rgba(255, 150, 150, 0.5);
                    color: white;
                }
            """)
            delete_button.clicked.connect(partial(delete_employee, table, employee_id))
            layout.addWidget(delete_button)

        widget.setLayout(layout)
        table.setCellWidget(row, 7, widget)
    table.resizeColumnsToContents()

def edit_employee(table, employee_id):
    """
    Mở dialog sửa thông tin nhân viên
    """
    from src.modules.admin.dialog.add_employee_dialog import AddEmployeeDialog
    nhan_vien = EmployeeDAO.get_nhan_vien_by_id(employee_id)
    if not nhan_vien:
        QtWidgets.QMessageBox.critical(
            table.parent(),
            "Lỗi",
            f"Không thể tìm thấy thông tin nhân viên có ID {employee_id}!"
        )
        return

    dialog = AddEmployeeDialog(table.parent(), employee_id)
    if dialog.exec_() == QDialog.Accepted:
        # Nếu thành công, tải lại dữ liệu
        load_employee_data(table)

def delete_employee(table, employee_id):
    """
    Chuyển đổi trạng thái nhân viên: 1 -> 0 hoặc 0 -> 1
    """
    print(f"Đang chuyển đổi trạng thái nhân viên có ID: {employee_id}")

    try:
        from PyQt5.QtWidgets import QApplication, QMessageBox
        app = QApplication.instance()
        main_window = app.activeWindow()

        # Lấy thông tin nhân viên để kiểm tra trạng thái
        nhan_vien = EmployeeDAO.get_nhan_vien_by_id(employee_id)
        if not nhan_vien:
            QMessageBox.critical(main_window, 'Lỗi', f"Không tìm thấy nhân viên có ID {employee_id}")
            return

        # Xác định hành động và thông điệp dựa trên trạng thái
        action = "dừng hoạt động" if nhan_vien.status == 1 else "tái hoạt động"
        confirm_message = f"Bạn có muốn {action} nhân viên {nhan_vien.fullname} (ID: {employee_id}) không?"

        # Hiển thị dialog xác nhận
        reply = QMessageBox.question(
            main_window,
            'Xác nhận',
            confirm_message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Thực hiện chuyển đổi trạng thái
            success, new_status, message = EmployeeDAO.toggle_employee_status(employee_id)

            if success:
                QMessageBox.information(main_window, 'Thành công', message)
                table.setRowCount(0)
                load_employee_data(table)
            else:
                QMessageBox.critical(main_window, 'Lỗi', message)
        else:
            print(f"Hủy {action} nhân viên ID: {employee_id}")

    except Exception as e:
        print(f"Lỗi khi cập nhật trạng thái nhân viên: {str(e)}")
        import traceback
        traceback.print_exc()
        QMessageBox.critical(main_window, 'Lỗi', f"Đã xảy ra lỗi: {str(e)}")