import traceback
from datetime import datetime

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from src.modules.admin.dialog.add_promotion_dialog import AddPromotionDialog
from src.database.DAO.admin.PromotionDAO import KhuyenMaiDAO


class PromotionHandler:
    def __init__(self, parent=None):
        self.parent = parent
        self.promotion_dao = KhuyenMaiDAO()

    def show_add_promotion_dialog(self, promotion_id=None):
        """
        Hiển thị dialog thêm khuyến mãi mới
        """
        try:
            # Tạo dialog với parent là cửa sổ chính
            dialog = AddPromotionDialog(self.parent, promotion_id)

            # Hiển thị dialog và chờ kết quả
            result = dialog.exec_()

            # Nếu người dùng chấp nhận (nhấn OK/Thêm)
            if result == QtWidgets.QDialog.Accepted:
                # Lấy thông tin khuyến mãi từ dialog
                promotion_data = {
                    'id': dialog.ui.input_Id_khuyenmai.text().strip(),
                    'name': dialog.ui.input_ten_khuyenmai.text().strip(),
                    'start_date': dialog.ui.start_date.date().toString("yyyy-MM-dd"),
                    'end_date': dialog.ui.end_date.date().toString("yyyy-MM-dd"),
                }
                return True, promotion_data
            else:
                return False, None
        except Exception as e:
            print(f"Lỗi khi mở hoặc đóng dialog khuyến mãi: {str(e)}")
            traceback.print_exc()
            return False, None

    def show_edit_promotion_dialog(self, promotion_id):
        """
        Hiển thị dialog chỉnh sửa khuyến mãi
        """
        return self.show_add_promotion_dialog(promotion_id)

    def delete_promotion(self, promotion_id):
        """
        Xóa khuyến mãi
        """
        try:
            # Hiển thị hộp thoại xác nhận
            reply = QMessageBox.question(self.parent, 'Xác nhận xóa',
                                         f'Bạn có chắc chắn muốn xóa khuyến mãi có ID {promotion_id} không?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                # Sử dụng DAO để xóa khuyến mãi
                success = self.promotion_dao.delete_promotion(promotion_id)
                if success:
                    QMessageBox.information(self.parent, "Thành công", "Đã xóa khuyến mãi thành công!")
                    return True
                else:
                    QMessageBox.critical(self.parent, "Lỗi", "Không thể xóa khuyến mãi. Vui lòng thử lại sau!")
                    return False
            else:
                return False

        except Exception as e:
            print(f"Lỗi khi xóa khuyến mãi: {str(e)}")
            traceback.print_exc()
            QMessageBox.critical(self.parent, "Lỗi", f"Đã xảy ra lỗi khi xóa khuyến mãi: {str(e)}")
            return False
