from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QWidget, QHBoxLayout
from src.database.DAO.admin.ProductAdminDAO import ProductDAO
from PyQt5.QtWidgets import QComboBox

def load_products_to_combobox(combobox: QComboBox):
    product_dao = ProductDAO()
    products = product_dao.get_all_products()
    combobox.clear()
    for product in products:
        combobox.addItem(product.name, product.id_prod)

def search_products(table, keyword):
    """
    Tìm kiếm sản phẩm theo từ khóa và hiển thị kết quả lên bảng

    Args:
        table: QTableWidget để hiển thị dữ liệu
        keyword: Từ khóa tìm kiếm
    """
    products = ProductDAO.search_products_by_name(keyword)

    table.setRowCount(0)

    if not keyword.strip():
        load_data_to_sanPham_tb(table)
        return

    table.setRowCount(len(products))

    for row, product in enumerate(products):
        table.setItem(row, 0, QTableWidgetItem(str(product.id_prod)))
        table.setItem(row, 1, QTableWidgetItem(product.name))
        table.setItem(row, 2, QTableWidgetItem(product.unit))
        table.setItem(row, 3, QTableWidgetItem(str(product.price)))
        table.setItem(row, 4, QTableWidgetItem(str(product.price_import)))
        table.setItem(row, 5, QTableWidgetItem(product.description))
        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        btn_layout.setContentsMargins(5, 0, 5, 0)
        edit_btn = QPushButton("Sửa")
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(52, 152, 219, 0.3);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px 8px;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: rgba(52, 152, 219, 0.5);
                border: 1px solid rgba(52, 152, 219, 0.7);
                color: white;
            }
            QPushButton:pressed {
                background-color: rgba(52, 152, 219, 0.7);
                border: 1px solid rgba(52, 152, 219, 0.9);
                box-shadow: 0 0 8px rgba(52, 152, 219, 0.5);
                color: white;
            }
        """)
        product_id = product.id_prod
        edit_btn.clicked.connect(lambda checked, r=row, pid=product_id: edit_item(r, pid))
        delete_btn = QPushButton("Xóa")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(231, 76, 60, 0.3);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px 8px;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: rgba(231, 76, 60, 0.5);
                border: 1px solid rgba(231, 76, 60, 0.7);
                color: white;
            }
            QPushButton:pressed {
                background-color: rgba(231, 76, 60, 0.7);
                border: 1px solid rgba(231, 76, 60, 0.9);
                box-shadow: 0 0 8px rgba(231, 76, 60, 0.5);
                color: white;
            }
        """)
        delete_btn.clicked.connect(lambda checked, t=table, r=row, pid=product_id: delete_item(t, r, pid))
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.setSpacing(5)
        table.setCellWidget(row, 6, btn_widget)

def edit_item(row, product_id):
    """
    Xử lý sự kiện khi nhấn nút Sửa

    Args:
        row: Dòng được chọn
        product_id: ID của sản phẩm
    """
    print(f"Sửa sản phẩm có ID: {product_id}")

    try:
        product = ProductDAO.get_product_by_id(product_id)

        if not product:
            print("Không tìm thấy sản phẩm!")
            return

        from PyQt5.QtWidgets import QApplication
        from src.modules.admin.dialog.add_product_dialog import AddProductDialog

        app = QApplication.instance()
        main_window = app.activeWindow()

        from PyQt5.QtWidgets import QTableWidget
        original_table = None

        all_tables = main_window.findChildren(QTableWidget)
        for table in all_tables:
            if table.rowCount() > 0:
                for r in range(table.rowCount()):
                    if table.item(r, 0) and table.item(r, 0).text() == str(product_id):
                        original_table = table
                        break
            if original_table:
                break

        edit_dialog = AddProductDialog(main_window, product_id)

        if hasattr(edit_dialog.ui, "line_name"):
            edit_dialog.ui.line_name.setText(product.name)
        if hasattr(edit_dialog.ui, "line_unit"):
            edit_dialog.ui.line_unit.setText(product.unit)
        if hasattr(edit_dialog.ui, "line_gia_ban"):
            edit_dialog.ui.line_gia_ban.setText(str(product.price))
        if hasattr(edit_dialog.ui, "line_ghiChu"):
            edit_dialog.ui.line_ghiChu.setText(product.description)

        if hasattr(edit_dialog.ui, "line_id"):
            edit_dialog.ui.line_id.setText(str(product.id_prod))
            edit_dialog.ui.line_id.setReadOnly(True)
            edit_dialog.ui.line_id.setEnabled(False)
        elif hasattr(edit_dialog.ui, "id_input"):
            edit_dialog.ui.id_input.setText(str(product.id_prod))
            edit_dialog.ui.id_input.setReadOnly(True)
            edit_dialog.ui.id_input.setEnabled(False)

        result = edit_dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            print("Cập nhật sản phẩm thành công, đang tải lại dữ liệu...")

            # Cách 1: Sử dụng bảng đã lưu từ trước
            if original_table:
                print(f"Đã tìm thấy bảng gốc, tải lại dữ liệu...")
                load_data_to_sanPham_tb(original_table)
                print("Đã tải lại dữ liệu sản phẩm vào bảng gốc")
                return

            # Cách 2: Tìm bảng sản phẩm trong cửa sổ chính (nếu cách 1 không thành công)
            table_widget = None
            for widget in main_window.findChildren(QTableWidget):
                if (widget.columnCount() >= 6 and
                        widget.horizontalHeaderItem(0) and
                        widget.horizontalHeaderItem(1) and
                        "ID" in widget.horizontalHeaderItem(0).text() and
                        "Tên" in widget.horizontalHeaderItem(1).text()):
                    table_widget = widget
                    break

            if table_widget:
                # Sử dụng hàm load_data_to_sanPham_tb có sẵn để tải lại dữ liệu
                load_data_to_sanPham_tb(table_widget)
                print("Đã tải lại dữ liệu sản phẩm vào bảng được tìm thấy")
                return

            # Cách 3: Tìm và cập nhật trực tiếp dòng chứa sản phẩm đã sửa
            for table in all_tables:
                if table.rowCount() > 0:
                    for r in range(table.rowCount()):
                        if table.item(r, 0) and table.item(r, 0).text() == str(product_id):
                            # Lấy thông tin sản phẩm đã cập nhật
                            updated_product = ProductDAO.get_product_by_id(product_id)
                            if updated_product:
                                # Cập nhật thông tin sản phẩm trong bảng
                                table.setItem(r, 1, QtWidgets.QTableWidgetItem(updated_product.name))
                                table.setItem(r, 2, QtWidgets.QTableWidgetItem(updated_product.unit))
                                table.setItem(r, 3, QtWidgets.QTableWidgetItem(str(updated_product.price)))
                                table.setItem(r, 4, QtWidgets.QTableWidgetItem(str(updated_product.price_import)))
                                table.setItem(r, 5, QtWidgets.QTableWidgetItem(updated_product.description))
                                print(f"Đã cập nhật trực tiếp dòng {r} trong bảng")
                                return

            # Cách 4: Nếu không tìm thấy cách nào để cập nhật UI, thử reload toàn bộ trang
            try:
                # Tìm phương thức load_data hoặc refresh trong main_window
                if hasattr(main_window, 'load_data') and callable(getattr(main_window, 'load_data')):
                    main_window.load_data()
                    print("Đã gọi phương thức load_data của cửa sổ chính")
                elif hasattr(main_window, 'refresh') and callable(getattr(main_window, 'refresh')):
                    main_window.refresh()
                    print("Đã gọi phương thức refresh của cửa sổ chính")
                else:
                    print("Không tìm thấy phương thức để tải lại dữ liệu trong cửa sổ chính")
                    print("Không thể tải lại dữ liệu sau khi sửa sản phẩm")
            except Exception as reload_error:
                print(f"Lỗi khi cố gắng tải lại dữ liệu: {reload_error}")

    except Exception as e:
        from PyQt5.QtWidgets import QMessageBox
        print(f"Lỗi khi sửa sản phẩm: {e}")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Lỗi khi sửa sản phẩm")
        msg.setInformativeText(f"Chi tiết lỗi: {str(e)}")
        msg.setWindowTitle("Lỗi")
        msg.exec_()

def delete_item(table, row, product_id):
    """
    Xử lý sự kiện khi nhấn nút Xóa

    Args:
        table: QTableWidget chứa dữ liệu
        row: Dòng được chọn
        product_id: ID của sản phẩm
    """
    # Xóa sản phẩm từ database
    success = ProductDAO.delete_product(product_id)

    if success:
        # Xóa dòng khỏi bảng
        table.removeRow(row)
        print(f"Đã xóa sản phẩm có ID: {product_id}")
    else:
        print(f"Không thể xóa sản phẩm có ID: {product_id}")

def load_data_to_sanPham_tb(table):
    """
    Nạp dữ liệu sản phẩm từ database lên QTableWidget

    Args:
        table: QTableWidget để hiển thị dữ liệu
    """
    products = ProductDAO.get_all_products()

    table.setRowCount(len(products))

    for row, product in enumerate(products):
        # Cột ID
        table.setItem(row, 0, QTableWidgetItem(str(product.id_prod)))

        # Cột Tên sản phẩm
        table.setItem(row, 1, QTableWidgetItem(product.name))

        # Cột Đơn vị
        table.setItem(row, 2, QTableWidgetItem(product.unit))

        # Cột Đơn giá
        table.setItem(row, 3, QTableWidgetItem(str(product.price)))

        # Cột Giá vốn
        table.setItem(row, 4, QTableWidgetItem(str(product.price_import)))

        # Cột Mô tả
        table.setItem(row, 5, QTableWidgetItem(product.description))

        # Tạo nút Sửa và Xóa
        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        btn_layout.setContentsMargins(5, 0, 5, 0)

        # Nút Sửa
        edit_btn = QPushButton("Sửa")
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(52, 152, 219, 0.3);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px 8px;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: rgba(52, 152, 219, 0.5);
                border: 1px solid rgba(52, 152, 219, 0.7);
                color: white;
            }
            QPushButton:pressed {
                background-color: rgba(52, 152, 219, 0.7);
                border: 1px solid rgba(52, 152, 219, 0.9);
                box-shadow: 0 0 8px rgba(52, 152, 219, 0.5);
                color: white;
            }
        """)
        product_id = product.id_prod
        edit_btn.clicked.connect(lambda checked, r=row, pid=product_id: edit_item(r, pid))

        # Nút Xóa
        delete_btn = QPushButton("Xóa")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(231, 76, 60, 0.3);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px 8px;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: rgba(231, 76, 60, 0.5);
                border: 1px solid rgba(231, 76, 60, 0.7);
                color: white;
            }
            QPushButton:pressed {
                background-color: rgba(231, 76, 60, 0.7);
                border: 1px solid rgba(231, 76, 60, 0.9);
                box-shadow: 0 0 8px rgba(231, 76, 60, 0.5);
                color: white;
            }
        """)
        delete_btn.clicked.connect(lambda checked, t=table, r=row, pid=product_id: delete_item(t, r, pid))

        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.setSpacing(5)
        table.setCellWidget(row, 6, btn_widget)