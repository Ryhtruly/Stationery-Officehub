from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QMessageBox
from datetime import datetime
from src.database.DAO.admin.PromotionDAO import KhuyenMaiDAO

def load_promotion_data(table, parent=None):
    """
    Tải dữ liệu khuyến mãi từ database vào bảng giao diện
    """
    promotions = KhuyenMaiDAO.get_all_khuyen_mai()
    table.setRowCount(0)

    current_date = datetime.now().date()

    for promotion in promotions:
        row_position = table.rowCount()
        table.insertRow(row_position)

        table.setItem(row_position, 0, QTableWidgetItem(str(promotion.id_prom)))
        table.setItem(row_position, 1, QTableWidgetItem(promotion.name))

        if isinstance(promotion.start_date, str):
            start_date = datetime.strptime(promotion.start_date, '%Y-%m-%d')
        else:
            start_date = promotion.start_date

        if isinstance(promotion.end_date, str):
            end_date = datetime.strptime(promotion.end_date, '%Y-%m-%d')
        else:
            end_date = promotion.end_date

        table.setItem(row_position, 2, QTableWidgetItem(start_date.strftime('%Y-%m-%d')))
        table.setItem(row_position, 3, QTableWidgetItem(end_date.strftime('%Y-%m-%d')))

        if start_date.date() <= current_date <= end_date.date():
            status = "Đang diễn ra"
        else:
            status = "Không hoạt động"

        table.setItem(row_position, 4, QTableWidgetItem(status))  # Hiển thị trạng thái

        edit_button = QPushButton('Sửa')
        edit_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(80, 200, 200, 0.3); /* Xanh ngọc trong suốt */
                color: white;
                border: none;
                border-radius: 4px;
                padding: 2px 5px;
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
        delete_button = QPushButton('Xóa')
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 150, 150, 0.3); /* Hồng phấn trong suốt */
                color: white;
                border: none;
                border-radius: 4px;
                padding: 2px 5px;
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

        edit_button.clicked.connect(lambda _, r=row_position, id=promotion.id_prom: edit_item(r, id, parent))

        delete_button.clicked.connect(lambda _, r=row_position, id=promotion.id_prom: delete_item(table, r, id, parent))

        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        button_layout.setContentsMargins(0, 0, 0, 0)
        table.setCellWidget(row_position, 5, button_widget)

def edit_item(row, promotion_id, parent):
    """
    Xử lý sự kiện khi nhấn nút Sửa
    """
    print(f"Đang chỉnh sửa khuyến mãi có ID: {promotion_id} tại dòng {row}")
    if parent and hasattr(parent, 'promotion_handler'):
        success, _ = parent.promotion_handler.show_edit_promotion_dialog(promotion_id)
        if success:
            load_promotion_data(parent.ui.table_khuyenmai, parent)

def delete_item(table, row, promotion_id, parent):
    """
    Xử lý sự kiện khi nhấn nút Xóa
    """
    try:
        reply = QMessageBox.question(table.parentWidget(), 'Xác nhận xóa',
                                     f'Bạn có chắc chắn muốn xóa khuyến mãi có ID: {promotion_id}?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            success = KhuyenMaiDAO.delete_promotion(promotion_id)
            if success:
                table.removeRow(row)
                QMessageBox.information(table.parentWidget(), 'Thông báo', f"Đã xóa khuyến mãi có ID: {promotion_id}")
                load_promotion_data(table, parent)
            else:
                QMessageBox.warning(table.parentWidget(), 'Cảnh báo',
                                    f"Không thể xóa khuyến mãi có ID: {promotion_id}")
    except Exception as e:
        QMessageBox.critical(table.parentWidget(), 'Lỗi', f"Đã xảy ra lỗi khi xóa khuyến mãi: {str(e)}")