from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QMessageBox
from src.database.DAO.admin.CategoryDAO import CategoryDAO

def edit_item(row, category_id, parent=None):
    """
    Xử lý sự kiện khi nhấn nút Sửa

    Args:
        row: Dòng được chọn
        category_id: ID của danh mục
        parent: Widget cha để hiển thị dialog
    """
    print(f"Đang chỉnh sửa danh mục có ID: {category_id} tại dòng {row}")
    from src.modules.admin.dialog.add_category_dialog import AddCategoryDialog

    dialog = AddCategoryDialog(parent, category_id)
    result = dialog.exec_()

    if result == QtWidgets.QDialog.Accepted and parent:
        table = None
        for child in parent.findChildren(QtWidgets.QTableWidget):
            if child.objectName() == "danhMuc_tb":
                table = child
                break

        if table:
            load_data_to_danhMuc_tb(table)
        else:
            print("Không tìm thấy bảng danh mục để cập nhật")

def delete_item(table, row, category_id):
    """
    Xử lý sự kiện khi nhấn nút Xóa

    Args:
        table: QTableWidget chứa dữ liệu
        row: Dòng được chọn
        category_id: ID của danh mục
    """
    try:
        reply = QMessageBox.question(table.parentWidget(), 'Xác nhận xóa',
                                    f'Bạn có chắc chắn muốn xóa danh mục có ID: {category_id}?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            success = CategoryDAO.delete_category(category_id)

            if success:
                table.removeRow(row)
                QMessageBox.information(table.parentWidget(), 'Thông báo', f"Đã xóa danh mục có ID: {category_id}")
            else:
                QMessageBox.warning(table.parentWidget(), 'Cảnh báo',
                                  f"Không thể xóa danh mục có ID: {category_id} vì có sản phẩm thuộc danh mục này")
    except Exception as e:
        QMessageBox.critical(table.parentWidget(), 'Lỗi', f"Đã xảy ra lỗi khi xóa danh mục: {str(e)}")

def load_data_to_danhMuc_tb(table):
    """
    Nạp dữ liệu danh mục từ database lên QTableWidget

    Args:
        table: QTableWidget để hiển thị dữ liệu
    """

    if table.columnCount() < 3:
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["ID", "Tên danh mục", "Chỉnh sửa"])

    categories = CategoryDAO.get_all_categories()

    print(f"Số lượng danh mục: {len(categories)}")

    table.setRowCount(0)

    table.setRowCount(len(categories))

    for row, category in enumerate(categories):
        category_id = category.id_category

        table.setItem(row, 0, QTableWidgetItem(str(category_id)))
        table.setItem(row, 1, QTableWidgetItem(category.name))
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 2, 5, 2)

        # Nút Sửa
        btn_edit = QPushButton("Sửa")
        btn_edit.setStyleSheet("""
            QPushButton {
                background-color: rgba(80, 200, 200, 0.3); /* Xanh ngọc trong suốt */
                color: white;
                border: none;
                border-radius: 5px;
                padding: 2px;
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
        # Sử dụng partial thay vì lambda để tránh vấn đề với biến
        from functools import partial
        btn_edit.clicked.connect(partial(edit_item, row, category_id, table.parentWidget()))

        # Nút Xóa
        btn_delete = QPushButton("Xóa")
        btn_delete.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 150, 150, 0.3); /* Hồng phấn trong suốt */
                color: white;
                border: none;
                border-radius: 5px;
                padding: 2px;
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
        btn_delete.clicked.connect(partial(delete_item, table, row, category_id))
        layout.addWidget(btn_edit)
        layout.addWidget(btn_delete)
        widget.setLayout(layout)
        table.setCellWidget(row, 2, widget)
    table.resizeRowsToContents()

def search_categories(keyword, table):
    """
    Tìm kiếm danh mục theo từ khóa và hiển thị kết quả lên bảng

    Args:
        keyword: Từ khóa tìm kiếm
        table: QTableWidget để hiển thị kết quả
    """
    # Tìm kiếm danh mục
    categories = CategoryDAO.search_categories(keyword)

    print(f"Tìm thấy {len(categories)} danh mục với từ khóa: '{keyword}'")
    table.setRowCount(0)
    table.setRowCount(len(categories))

    # Nạp dữ liệu vào bảng
    for row, category in enumerate(categories):
        table.setItem(row, 0, QTableWidgetItem(str(category.id_category)))
        table.setItem(row, 1, QTableWidgetItem(category.name))
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        btn_edit = QPushButton("Sửa")
        btn_edit.setStyleSheet("""
            QPushButton {
                background-color: rgba(80, 200, 200, 0.3); /* Xanh ngọc trong suốt */
                color: white;
                border: none;
                border-radius: 5px;
                padding: 2px;
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
        btn_edit.clicked.connect(
            lambda checked=False, r=row, id=category.id_category: edit_item(r, id, table.parentWidget()))

        # Nút Xóa
        btn_delete = QPushButton("Xóa")
        btn_delete.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 150, 150, 0.3); /* Hồng phấn trong suốt */
                color: white;
                border: none;
                border-radius: 5px;
                padding: 2px;
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
        btn_delete.clicked.connect(lambda checked=False, r=row, id=category.id_category: delete_item(table, r, id))

        layout.addWidget(btn_edit)
        layout.addWidget(btn_delete)

        widget.setLayout(layout)
        table.setCellWidget(row, 2, widget)
    table.resizeRowsToContents()