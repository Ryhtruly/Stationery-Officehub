from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QMessageBox
from src.database.DAO.admin.WarehouseDAO import WarehouseDAO


def view_detail(warehouse_id, product_id):
    """
    Xử lý sự kiện khi nhấn nút Xem chi tiết

    Args:
        warehouse_id: ID kho hàng
        product_id: ID sản phẩm
    """
    # TODO: Hiển thị chi tiết sản phẩm trong kho
    print(f"Xem chi tiết sản phẩm {product_id} trong kho {warehouse_id}")


def load_data_to_warehouse_table(table):
    """
    Nạp dữ liệu kho hàng từ database lên QTableWidget

    Args:
        table: QTableWidget để hiển thị dữ liệu
    """
    # Đảm bảo bảng đã được thiết lập đúng cách

    warehouse_products = WarehouseDAO.get_warehouse_products()

    print(f"Số lượng sản phẩm trong kho: {len(warehouse_products)}")

    table.setRowCount(0)

    table.setRowCount(len(warehouse_products))

    for row, product in enumerate(warehouse_products):
        table.setItem(row, 0, QTableWidgetItem(str(product.name)))
        table.setItem(row, 1, QTableWidgetItem(str(product.inventory)))



