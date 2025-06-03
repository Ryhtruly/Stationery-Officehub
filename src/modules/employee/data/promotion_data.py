from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QMessageBox
from datetime import datetime
from src.database.DAO.admin.PromotionDAO import KhuyenMaiDAO
from src.modules.admin.dialog.add_promotion_dialog import AddPromotionDialog  # Tái sử dụng từ admin


def load_promotion_data(table, parent=None):
    """
    Tải dữ liệu khuyến mãi đang hiện hành vào bảng giao diện
    """
    promotion_dao = KhuyenMaiDAO()
    promotions = promotion_dao.get_all_khuyen_mai()

    table.setRowCount(0)  # Xóa dữ liệu cũ
    current_date = datetime.now().date()  # Lấy ngày hiện tại

    for promotion in promotions:
        if isinstance(promotion.start_date, str):
            start_date = datetime.strptime(promotion.start_date, '%Y-%m-%d')
        else:
            start_date = promotion.start_date

        if isinstance(promotion.end_date, str):
            end_date = datetime.strptime(promotion.end_date, '%Y-%m-%d')
        else:
            end_date = promotion.end_date

        # Chỉ hiển thị khuyến mãi đang hiện hành
        if start_date.date() <= current_date <= end_date.date():
            row_position = table.rowCount()
            table.insertRow(row_position)

            table.setItem(row_position, 0, QTableWidgetItem(str(promotion.id_prom)))
            table.setItem(row_position, 1, QTableWidgetItem(promotion.name))
            table.setItem(row_position, 2, QTableWidgetItem(start_date.strftime('%Y-%m-%d')))
            table.setItem(row_position, 3, QTableWidgetItem(end_date.strftime('%Y-%m-%d')))
            table.setItem(row_position, 4, QTableWidgetItem("Đang diễn ra"))

            detail_button = QPushButton('Xem chi tiết')
            detail_button.clicked.connect(
                lambda _, r=row_position, id=promotion.id_prom: view_promotion_details(id, parent))

            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            button_layout.addWidget(detail_button)
            button_layout.setContentsMargins(0, 0, 0, 0)
            table.setCellWidget(row_position, 5, button_widget)


def view_promotion_details(promotion_id, parent):
    """
    Hiển thị dialog chi tiết khuyến mãi (chỉ xem)
    """
    dialog = AddPromotionDialog(parent, promotion_id)
    dialog.setWindowTitle("Chi tiết khuyến mãi")
    dialog.ui.input_Id_khuyenmai.setReadOnly(True)
    dialog.ui.input_ten_khuyenmai.setReadOnly(True)
    dialog.ui.start_date.setReadOnly(True)
    dialog.ui.end_date.setReadOnly(True)
    for checkbox in dialog.category_checkboxes.values():
        checkbox.setEnabled(False)
    for spinbox in dialog.category_discount_spinboxes.values():
        spinbox.setReadOnly(True)
    dialog.ui.them_btn.hide()
    dialog.ui.huy_btn.setText("Đóng")

    dialog.exec_()