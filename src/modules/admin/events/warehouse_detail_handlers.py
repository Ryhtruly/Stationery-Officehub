from PyQt5 import QtCore, QtWidgets
from src.modules.admin.dialog.warehouse_detail_dialog import WareHouseDetailDialog
from src.database.DAO.admin.WarehouseDAO import WarehouseDAO


class WarehouseHandler:
    def __init__(self, parent=None):
        self.parent = parent

    def show_warehouse_detail_dialog(self, warehouse_id=None):
        """
        Hiển thị dialog chi tiết kho hàng
        """
        dialog = WareHouseDetailDialog(self.parent)

        try:
            warehouses = WarehouseDAO.get_all_warehouses()

            # Debug: Kiểm tra số lượng kho nhận được
            print(f"Số lượng kho hàng lấy được từ database: {len(warehouses)}")

            if not warehouses or len(warehouses) == 0:
                QtWidgets.QMessageBox.warning(dialog, "Thông báo", "Không có dữ liệu kho hàng nào!")
            else:
                if len(warehouses) > 0:
                    self.display_warehouse_info(dialog, warehouses[0], 2)

                if len(warehouses) > 1:
                    self.display_warehouse_info(dialog, warehouses[1], 1)

        except Exception as e:
            print(f"Lỗi khi lấy danh sách kho: {str(e)}")
            QtWidgets.QMessageBox.critical(dialog, "Lỗi", f"Không thể lấy dữ liệu kho hàng: {str(e)}")

        dialog.exec_()

    def display_warehouse_info(self, dialog, warehouse, position):
        """
        Hiển thị thông tin kho lên vị trí cụ thể trong dialog
        """
        try:
            container = None
            if position == 1:
                container = dialog.findChild(QtWidgets.QWidget, "inf_kho_1")
            elif position == 2:
                container = dialog.findChild(QtWidgets.QWidget, "inf_kho_2")

            if not container:
                print(f"Không tìm thấy container cho vị trí {position}")
                return

            for child in container.findChildren(QtWidgets.QWidget):
                child.deleteLater()

            container_width = container.width()
            print(f"Container {position} width: {container_width}px")

            layout = QtWidgets.QVBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            # Tạo scroll area
            scroll_area = QtWidgets.QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
            scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

            scroll_area.setMinimumWidth(container_width)

            content_widget = QtWidgets.QWidget()
            content_layout = QtWidgets.QVBoxLayout(content_widget)
            content_layout.setContentsMargins(0, 0, 0, 0)

            content_widget.setMinimumWidth(container_width - 2)  # Trừ đi một chút để tránh thanh cuộn ngang

            # Tạo label để hiển thị thông tin
            label = QtWidgets.QLabel()
            label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

            # Đảm bảo label mở rộng hết chiều rộng của content widget
            label.setMinimumWidth(container_width - 5)

            # Tạo HTML cho thông tin kho, truyền vào chiều rộng của container
            # Đảm bảo chiều rộng đủ lớn để bảng hiển thị đúng
            html_content = self.create_warehouse_html(warehouse, container_width - 5)

            # Hiển thị thông tin lên label
            label.setText(html_content)
            label.setTextFormat(QtCore.Qt.RichText)
            label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
            label.setWordWrap(True)

            # Thêm một chút style cho label để đảm bảo nội dung hiển thị đúng
            label.setStyleSheet("padding: 0px; margin: 0px;")

            # Thêm label vào content widget
            content_layout.addWidget(label)

            # Đặt content widget vào scroll area
            scroll_area.setWidget(content_widget)

            # Thêm scroll area vào container
            layout.addWidget(scroll_area)

            # Áp dụng layout mới cho container
            container.setLayout(layout)

            print(f"Đã hiển thị thông tin kho {warehouse.name} lên vị trí {position}")

        except Exception as e:
            print(f"Lỗi khi hiển thị thông tin kho: {str(e)}")
            import traceback
            traceback.print_exc()

    def create_warehouse_html(self, warehouse, width=None):
        """
        Tạo nội dung HTML cho thông tin kho
        @param width: Chiều rộng của container để điều chỉnh bảng cho phù hợp
        """
        try:
            # Lấy danh sách sản phẩm trong kho
            warehouse_products = WarehouseDAO.get_warehouse_products_by_warehouse_id(warehouse.id_warehouse)

            # Đảm bảo width là một giá trị hợp lệ
            if width is None or width <= 0:
                width = 300  # Giá trị mặc định nếu width không hợp lệ

            # Tạo HTML với container bao quanh toàn bộ nội dung và căn giữa
            html = f"""
            <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; padding: 10px;'>
                <div style='text-align: center; width: {width}px;'>
                    <h3 style='color: #8b5e3c; margin-top: 0;'>{warehouse.name}</h3>
                    <p style='margin: 5px 0;'><b>Mã kho:</b> {warehouse.id_warehouse}</p>
                    <p style='margin: 5px 0;'><b>Địa chỉ:</b> {warehouse.address}</p>
                    <p style='margin: 5px 0;'><b>Điện thoại:</b> {warehouse.phone}</p>
                </div>
                <hr style='width: {width}px; margin: 10px 0;'>
                <div style='width: {width}px; text-align: center;'>
                    <p style='margin: 5px 0;'><b>Danh sách sản phẩm</b></p>
            """

            # Thêm bảng sản phẩm nếu có
            if warehouse_products and len(warehouse_products) > 0:
                # Tính toán chiều rộng cột
                col1_width = int(width * 0.15)  # Mã SP
                col3_width = int(width * 0.20)  # SL
                col2_width = width - col1_width - col3_width - 2  # Tên SP

                html += f"""
                <div style='display: flex; justify-content: center; width: 100%;'>
                    <table style='width: {width}px; border-collapse: collapse; table-layout: fixed;'>
                        <colgroup>
                            <col style='width: {col1_width}px;'>
                            <col style='width: {col2_width}px;'>
                            <col style='width: {col3_width}px;'>
                        </colgroup>
                        <tr style='background-color: #d4a373; color: white;'>
                            <th style='border: 1px solid #8c5c3f; padding: 5px; text-align: center;'>Mã SP</th>
                            <th style='border: 1px solid #8c5c3f; padding: 5px; text-align: center;'>Tên SP</th>
                            <th style='border: 1px solid #8c5c3f; padding: 5px; text-align: center;'>SL</th>
                        </tr>
                """

                for i, product in enumerate(warehouse_products):
                    bg_color = "#f5f5f5" if i % 2 == 0 else "#ffffff"

                    # Sử dụng đúng tên thuộc tính của đối tượng WarehouseProduct
                    product_id = product.id_prod if hasattr(product, 'id_prod') else "Chưa có mã"
                    product_name = product.name if hasattr(product, 'name') else "Chưa có tên"
                    quantity = product.inventory if hasattr(product, 'inventory') else "0"

                    # Đảm bảo các giá trị không phải None
                    product_id = str(product_id) if product_id is not None else "Chưa có mã"
                    product_name = str(product_name) if product_name is not None else "Chưa có tên"
                    quantity = str(quantity) if quantity is not None else "0"

                    html += f"""
                    <tr style='background-color: {bg_color};'>
                        <td style='border: 1px solid #ddd; padding: 5px; text-align: center; overflow: hidden; text-overflow: ellipsis;'>{product_id}</td>
                        <td style='border: 1px solid #ddd; padding: 5px; overflow: hidden; text-overflow: ellipsis;'>{product_name}</td>
                        <td style='border: 1px solid #ddd; padding: 5px; text-align: center;'>{quantity}</td>
                    </tr>
                    """

                html += """
                    </table>
                </div>
                """
            else:
                html += "<p style='text-align: center; color: gray; width: 100%;'>Không có sản phẩm nào trong kho này</p>"

            html += """
                </div>
            </div>
            """

            return html

        except Exception as e:
            print(f"Lỗi khi tạo HTML cho thông tin kho: {str(e)}")
            import traceback
            traceback.print_exc()
            return f"<p style='color: red;'>Lỗi khi tải thông tin kho: {str(e)}</p>"
