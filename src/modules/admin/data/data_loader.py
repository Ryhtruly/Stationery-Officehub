from PyQt5.QtCore import QDate
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QTableWidgetItem
from src.database.connection import create_connection
from src.database.DAO.admin.StatisticDAO import StatisticDAO

class StatisticDataLoader:
    def __init__(self):
        self.connection = create_connection()
        self.dao = StatisticDAO(self.connection)

    def get_product_statistics(self, from_date, to_date):
        """
        Lấy thống kê sản phẩm trong khoảng thời gian

        Args:
            from_date (str): Ngày bắt đầu (định dạng dd-MM-yyyy)
            to_date (str): Ngày kết thúc (định dạng dd-MM-yyyy)

        Returns:
            tuple: (data, total_quantity, total_revenue, total_cost, total_profit)
        """
        return self.dao.get_product_statistics(from_date, to_date)

    def get_daily_statistics(self, from_date, to_date):
        """
        Lấy thống kê doanh thu theo ngày

        Args:
            from_date (str): Ngày bắt đầu (định dạng dd-MM-yyyy)
            to_date (str): Ngày kết thúc (định dạng dd-MM-yyyy)

        Returns:
            tuple: (dates, revenues)
        """
        return self.dao.get_daily_statistics(from_date, to_date)

    def load_data_to_statistic_table(self, table, from_date, to_date):
        """
        Load dữ liệu thống kê vào bảng

        Args:
            table (QTableWidget): Bảng hiển thị dữ liệu
            from_date (str): Ngày bắt đầu (định dạng dd-MM-yyyy)
            to_date (str): Ngày kết thúc (định dạng dd-MM-yyyy)
        """
        try:
            data, total_quantity, total_revenue, total_cost, total_profit = self.get_product_statistics(
                from_date, to_date)
            table.setRowCount(0)
            for row_idx, (id_prod, name, quantity, revenue, cost, profit) in enumerate(data):
                table.insertRow(row_idx)
                id_str = str(id_prod)
                name_str = str(name)
                quantity_str = str(quantity)
                revenue_str = f"{float(revenue):,.0f}" if revenue is not None else "0"
                cost_str = f"{float(cost):,.0f}" if cost is not None else "0"
                profit_str = f"{float(profit):,.0f}" if profit is not None else "0"
                table.setItem(row_idx, 0, QTableWidgetItem(id_str))
                table.setItem(row_idx, 1, QTableWidgetItem(name_str))
                table.setItem(row_idx, 2, QTableWidgetItem(quantity_str))
                table.setItem(row_idx, 3, QTableWidgetItem(revenue_str))
                table.setItem(row_idx, 4, QTableWidgetItem(cost_str))
                table.setItem(row_idx, 5, QTableWidgetItem(profit_str))

        except Exception as e:
            print(f"Lỗi khi load dữ liệu vào bảng thống kê: {e}")