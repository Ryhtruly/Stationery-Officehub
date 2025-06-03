from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from src.modules.admin.dialog.add_product_to_import_dialog import AddProductToImportDialog


class AddProductToImportHandler:
    def __init__(self, parent=None, import_table=None):
        self.parent = parent
        self.import_table = import_table
        self.products_in_import = []
    def show_add_product_dialog(self):
        """Hiển thị dialog thêm sản phẩm vào phiếu nhập"""
        try:
            dialog = AddProductToImportDialog(self.parent)
            result = dialog.exec_()

            if result == QtWidgets.QDialog.Accepted:
                product_data = dialog.get_product_data()
                if product_data:
                    success = self.add_product_to_import_table(product_data)
                    if success:
                        total = self.calculate_total_amount()
                        if hasattr(self.parent.ui, 'line_tong_tien'):
                            self.parent.ui.line_tong_tien.setText(f"{total:,.0f}")
                        return True, product_data

            return False, None
        except Exception as e:
            QMessageBox.warning(
                self.parent,
                "Lỗi",
                f"Không thể thêm sản phẩm: {str(e)}",
                QMessageBox.Ok
            )
            return False, None

    def add_product_to_import_table(self, product_data):
        """Thêm sản phẩm vào bảng phiếu nhập"""
        try:
            if not self.import_table:
                QMessageBox.warning(
                    self.parent,
                    "Lỗi",
                    "Không tìm thấy bảng sản phẩm",
                    QMessageBox.Ok
                )
                return False

            product_id = product_data['id_prod']
            for i in range(self.import_table.rowCount()):
                if self.import_table.item(i, 0) and self.import_table.item(i, 0).text() == product_id:
                    try:
                        # Cập nhật số lượng nếu sản phẩm đã tồn tại
                        old_quantity = float(self.import_table.item(i, 4).text())
                        new_quantity = float(product_data['quantity'])
                        updated_quantity = old_quantity + new_quantity

                        self.import_table.setItem(i, 4, QTableWidgetItem(str(updated_quantity)))

                        # Cập nhật trong danh sách
                        for j, product in enumerate(self.products_in_import):
                            if product['id_prod'] == product_id:
                                self.products_in_import[j]['quantity'] = str(updated_quantity)
                                break

                        self.calculate_total_amount()
                        return True
                    except Exception as e:
                        QMessageBox.warning(
                            self.parent,
                            "Lỗi",
                            f"Không thể cập nhật sản phẩm: {str(e)}",
                            QMessageBox.Ok
                        )
                        return False

            row_count = self.import_table.rowCount()
            self.import_table.insertRow(row_count)

            # Thêm dữ liệu vào bảng theo thứ tự cột mới
            self.import_table.setItem(row_count, 0, QTableWidgetItem(str(product_data['id_prod'])))
            self.import_table.setItem(row_count, 1, QTableWidgetItem(str(product_data['name'])))
            self.import_table.setItem(row_count, 2, QTableWidgetItem(str(product_data['category_name'])))
            self.import_table.setItem(row_count, 3, QTableWidgetItem(str(product_data['warehouse_name'])))
            self.import_table.setItem(row_count, 4, QTableWidgetItem(str(product_data['quantity'])))
            self.import_table.setItem(row_count, 5, QTableWidgetItem(str(product_data['unit'])))
            self.import_table.setItem(row_count, 6, QTableWidgetItem(str(product_data['import_price'])))

            # Thêm nút chỉnh sửa vào cột cuối cùng
            edit_btn = QtWidgets.QPushButton("Chỉnh sửa")
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #d4a373;
                    color: #ffffff;
                    border: 2px solid #8c5c3f;
                    border-radius: 10px;
                    font-family: "Georgia", serif;
                    font-size: 10px;
                    font-weight: bold;
                    padding: 5px 10px;
                    text-transform: uppercase;
                    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
                }
                QPushButton:hover {
                    background-color: #c28e62;
                }
            """)

            # Tạo hàm xử lý sự kiện riêng thay vì lambda
            def handle_edit_click():
                self.show_product_detail(row_count)

            edit_btn.clicked.connect(handle_edit_click)
            self.import_table.setCellWidget(row_count, 7, edit_btn)

            # Thêm vào danh sách sản phẩm
            self.products_in_import.append(product_data)

            return True
        except Exception as e:
            QMessageBox.warning(
                self.parent,
                "Lỗi",
                f"Không thể thêm sản phẩm: {str(e)}",
                QMessageBox.Ok
            )
            return False

    def calculate_total_amount(self):
        """Tính tổng tiền của phiếu nhập"""
        total = 0
        try:
            for i in range(self.import_table.rowCount()):
                quantity = self.import_table.item(i, 4).text()  # Số lượng ở cột 4
                price = self.import_table.item(i, 6).text()  # Giá nhập ở cột 6
                try:
                    subtotal = float(quantity) * float(price)
                    total += subtotal
                except:
                    pass

            # Cập nhật tổng tiền trong UI nếu có
            if hasattr(self.parent, 'ui') and hasattr(self.parent.ui, 'line_tong_tien'):
                self.parent.ui.line_tong_tien.setText(f"{total:,.0f}")

            return total
        except Exception as e:
            print(f"Lỗi khi tính tổng tiền: {str(e)}")
            return 0

    def show_product_detail(self, row):
        """Hiển thị chi tiết sản phẩm và cho phép chỉnh sửa hoặc xóa"""
        try:
            if row < 0 or row >= len(self.products_in_import):
                return

            product_data = self.products_in_import[row].copy()  # Tạo bản sao để tránh tham chiếu

            # Hiển thị dialog với thông tin sản phẩm
            dialog = AddProductToImportDialog(self.parent)

            # Điền thông tin sản phẩm vào dialog
            dialog.ui.line_id.setText(product_data['id_prod'])
            dialog.ui.line_id.setReadOnly(True)  # Không cho phép sửa ID
            dialog.ui.line_name.setText(product_data['name'])
            dialog.ui.line_unit.setText(product_data['unit'])
            dialog.ui.line_soLuong.setText(product_data['quantity'])
            dialog.ui.line_gia_nhap.setText(product_data['import_price'])

            # Chọn danh mục
            index = dialog.ui.combo_box_danhmuc.findText(product_data['category_name'])
            if index >= 0:
                dialog.ui.combo_box_danhmuc.setCurrentIndex(index)

            # Chọn kho
            index = dialog.ui.combo_box_kho.findText(product_data['warehouse_name'])
            if index >= 0:
                dialog.ui.combo_box_kho.setCurrentIndex(index)

            # Thay đổi tiêu đề và nút
            dialog.ui.them_sua_label.setText("CHỈNH SỬA SẢN PHẨM")
            dialog.ui.them_btn.setText("LƯU")

            # Thêm nút xóa
            if not hasattr(dialog.ui, 'xoa_btn'):
                dialog.ui.xoa_btn = QtWidgets.QPushButton("XÓA")
                dialog.ui.xoa_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #d9534f;
                        color: #ffffff;
                        border: 2px solid #c9302c;
                        border-radius: 10px;
                        font-family: "Georgia", serif;
                        font-size: 10px;
                        font-weight: bold;
                        padding: 5px 10px;
                        text-transform: uppercase;
                    }
                    QPushButton:hover {
                        background-color: #c9302c;
                    }
                """)
                dialog.ui.horizontalLayout_3.addWidget(dialog.ui.xoa_btn)
                dialog.ui.xoa_btn.clicked.connect(lambda: self.remove_product_from_table(row))

            result = dialog.exec_()

            if result == QtWidgets.QDialog.Accepted:
                # Lấy dữ liệu đã chỉnh sửa
                updated_data = dialog.get_product_data()
                if updated_data:
                    # Cập nhật dữ liệu trong bảng
                    self.import_table.setItem(row, 1, QTableWidgetItem(str(updated_data['name'])))
                    self.import_table.setItem(row, 2, QTableWidgetItem(str(updated_data['category_name'])))
                    self.import_table.setItem(row, 3, QTableWidgetItem(str(updated_data['warehouse_name'])))
                    self.import_table.setItem(row, 4, QTableWidgetItem(str(updated_data['quantity'])))
                    self.import_table.setItem(row, 5, QTableWidgetItem(str(updated_data['unit'])))
                    self.import_table.setItem(row, 6, QTableWidgetItem(str(updated_data['import_price'])))

                    # Cập nhật trong danh sách
                    self.products_in_import[row] = updated_data

                    # Cập nhật tổng tiền
                    self.calculate_total_amount()
                    return True

            return False
        except Exception as e:
            QMessageBox.warning(
                self.parent,
                "Lỗi",
                f"Không thể hiển thị chi tiết sản phẩm: {str(e)}",
                QMessageBox.Ok
            )
            return False

    def remove_product_from_table(self, row):
        """Xóa sản phẩm khỏi bảng"""
        try:
            if row < 0 or row >= self.import_table.rowCount():
                return False

            # Xóa sản phẩm khỏi bảng
            self.import_table.removeRow(row)

            # Xóa sản phẩm khỏi danh sách
            if row < len(self.products_in_import):
                self.products_in_import.pop(row)

            # Cập nhật tổng tiền
            self.calculate_total_amount()

            # Đóng dialog
            if self.parent and hasattr(self.parent, 'reject'):
                self.parent.reject()

            return True
        except Exception as e:
            QMessageBox.warning(
                self.parent,
                "Lỗi",
                f"Không thể xóa sản phẩm: {str(e)}",
                QMessageBox.Ok
            )
            return False
