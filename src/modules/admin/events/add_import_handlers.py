from PyQt5 import QtWidgets
from src.modules.admin.dialog.add_import_dialog import AddImportDialog
from PyQt5.QtWidgets import QMessageBox
from src.database.DAO.admin.ImportDAO import NhapHangDAO
import gc  # Thư viện garbage collector


class ImportHandler:
    def __init__(self, parent=None):
        self.parent = parent
        self.table_phieu_nhap = None  # Thêm biến để lưu tham chiếu đến bảng phiếu nhập

    def set_table_phieu_nhap(self, table):
        """Thiết lập tham chiếu đến bảng phiếu nhập"""
        self.table_phieu_nhap = table

    def show_add_import_dialog(self):
        """Hiển thị dialog thêm phiếu nhập hàng"""
        try:
            dialog = AddImportDialog(self.parent)
            result = dialog.exec_()

            if result == QtWidgets.QDialog.Accepted:
                try:
                    # Tạo bản sao dữ liệu từ dialog
                    import_data = dialog.get_import_data().copy()

                    # Đảm bảo dialog không còn được tham chiếu
                    dialog.deleteLater()
                    dialog = None

                    # Yêu cầu garbage collector chạy
                    gc.collect()

                    # Kiểm tra dữ liệu
                    if self.validate_import_data(import_data):
                        # Thêm phiếu nhập vào database
                        success = self.add_import_to_database(import_data)
                        if success:
                            QMessageBox.information(
                                self.parent,
                                "Thành công",
                                "Thêm phiếu nhập thành công!",
                                QMessageBox.Ok
                            )
                            # Reload lại bảng phiếu nhập sau khi thêm thành công
                            if self.table_phieu_nhap is not None:
                                self.reload_import_table()
                            return True
                        else:
                            QMessageBox.warning(
                                self.parent,
                                "Lỗi",
                                "Không thể thêm phiếu nhập vào database!",
                                QMessageBox.Ok
                            )
                except Exception as e:
                    import traceback
                    print(f"Lỗi khi xử lý dữ liệu từ dialog: {str(e)}")
                    print(traceback.format_exc())
                    QMessageBox.critical(
                        self.parent,
                        "Lỗi",
                        f"Đã xảy ra lỗi khi xử lý dữ liệu: {str(e)}",
                        QMessageBox.Ok
                    )
            else:
                # Đảm bảo dialog không còn được tham chiếu khi người dùng hủy
                dialog.deleteLater()
                dialog = None
                gc.collect()

            return False
        except Exception as e:
            import traceback
            print(f"Lỗi khi hiển thị dialog: {str(e)}")
            print(traceback.format_exc())
            QMessageBox.critical(
                self.parent,
                "Lỗi",
                f"Đã xảy ra lỗi khi hiển thị dialog: {str(e)}",
                QMessageBox.Ok
            )
            return False

    def validate_import_data(self, import_data):
        """Kiểm tra dữ liệu phiếu nhập"""
        try:
            # Kiểm tra ID nhân viên
            if not import_data.get('id_emp'):
                pass
                return False

            # Kiểm tra danh sách sản phẩm
            product_list = import_data.get('product_list', [])
            if not product_list:
                QMessageBox.warning(
                    self.parent,
                    "Lỗi",
                    "Vui lòng thêm ít nhất một sản phẩm vào phiếu nhập!",
                    QMessageBox.Ok
                )
                return False

            # Kiểm tra từng sản phẩm
            for i, product in enumerate(product_list):
                if not product.get('id_prod'):
                    QMessageBox.warning(
                        self.parent,
                        "Lỗi",
                        f"Sản phẩm thứ {i + 1} không có ID!",
                        QMessageBox.Ok
                    )
                    return False

                if not product.get('warehouse'):
                    QMessageBox.warning(
                        self.parent,
                        "Lỗi",
                        f"Sản phẩm '{product.get('name', 'Không tên')}' không có thông tin kho!",
                        QMessageBox.Ok
                    )
                    return False

                if not product.get('quantity') or product.get('quantity') <= 0:
                    QMessageBox.warning(
                        self.parent,
                        "Lỗi",
                        f"Sản phẩm '{product.get('name', 'Không tên')}' có số lượng không hợp lệ!",
                        QMessageBox.Ok
                    )
                    return False

                if not product.get('price') or product.get('price') <= 0:
                    QMessageBox.warning(
                        self.parent,
                        "Lỗi",
                        f"Sản phẩm '{product.get('name', 'Không tên')}' có giá không hợp lệ!",
                        QMessageBox.Ok
                    )
                    return False

            return True

        except Exception as e:
            QMessageBox.critical(
                self.parent,
                "Lỗi",
                f"Lỗi khi kiểm tra dữ liệu: {str(e)}",
                QMessageBox.Ok
            )
            return False

    def add_import_to_database(self, import_data):
        """Thêm phiếu nhập vào database"""
        try:
            # Đây là nơi bạn sẽ thêm code để lưu vào database
            # Ví dụ:
            # import_dao = ImportDAO()
            # success = import_dao.add_import(import_data)

            # Tạm thời trả về True để giả lập thành công
            return True
        except Exception as e:
            QMessageBox.warning(
                self.parent,
                "Lỗi",
                f"Không thể thêm phiếu nhập vào database: {str(e)}",
                QMessageBox.Ok
            )
            return False

    def reload_import_table(self):
        """Tải lại dữ liệu phiếu nhập vào bảng"""
        try:
            # Xóa tất cả dữ liệu hiện có trong bảng
            self.table_phieu_nhap.setRowCount(0)

            # Lấy danh sách phiếu nhập từ database
            phieu_nhap_list = NhapHangDAO.get_all_phieu_nhap()

            # Đổ dữ liệu vào bảng
            for row, phieu_nhap in enumerate(phieu_nhap_list):
                self.table_phieu_nhap.insertRow(row)

                # Thêm dữ liệu vào từng cột
                self.table_phieu_nhap.setItem(row, 0, QtWidgets.QTableWidgetItem(str(phieu_nhap.id_imp)))
                self.table_phieu_nhap.setItem(row, 1, QtWidgets.QTableWidgetItem(str(phieu_nhap.id_emp)))
                self.table_phieu_nhap.setItem(row, 2, QtWidgets.QTableWidgetItem(phieu_nhap.emp_name))

                # Định dạng ngày tháng
                date_formatted = phieu_nhap.date.strftime('%d/%m/%Y %H:%M:%S') if phieu_nhap.date else ""
                self.table_phieu_nhap.setItem(row, 3, QtWidgets.QTableWidgetItem(date_formatted))

                # Thêm tổng tiền nếu có
                if hasattr(phieu_nhap, 'total_amount'):
                    self.table_phieu_nhap.setItem(row, 4,
                                                  QtWidgets.QTableWidgetItem(f"{phieu_nhap.total_amount:,.0f} VNĐ"))

            # Điều chỉnh kích thước cột cho phù hợp
            self.table_phieu_nhap.resizeColumnsToContents()

        except Exception as e:
            import traceback
            print(f"Lỗi khi tải lại dữ liệu phiếu nhập: {str(e)}")
            print(traceback.format_exc())
            QMessageBox.critical(
                self.parent,
                "Lỗi",
                f"Không thể tải lại dữ liệu phiếu nhập: {str(e)}",
                QMessageBox.Ok
            )
