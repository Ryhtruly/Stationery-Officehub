import datetime
from src.database.connection import create_connection

class StatisticDAO:
    def __init__(self, connection):
        self.connection = connection

    def get_product_statistics(self, from_date, to_date):
        """
        Lấy thống kê sản phẩm trong khoảng thời gian

        Args:
            from_date (str): Ngày bắt đầu (định dạng dd-MM-yyyy)
            to_date (str): Ngày kết thúc (định dạng dd-MM-yyyy)

        Returns:
            tuple: (data, total_quantity, total_revenue, total_cost, total_profit)
        """
        try:
            # Chuyển đổi định dạng ngày
            from_date_obj = datetime.datetime.strptime(from_date, "%d-%m-%Y")
            to_date_obj = datetime.datetime.strptime(to_date, "%d-%m-%Y")

            # Định dạng lại cho SQL Server
            from_date_sql = from_date_obj.strftime("%Y-%m-%d")
            to_date_sql = to_date_obj.strftime("%Y-%m-%d") + " 23:59:59"

            cursor = self.connection.cursor()

            query = """
            SELECT 
                p.id_prod AS ID,
                p.name AS TenSanPham,
                SUM(bd.quantity) AS SoLuong,
                SUM(bd.quantity * bd.price * (1-bd.discount)) AS TongThuNhap,
                SUM(bd.quantity * p.price_import) AS TongVon,
                SUM(bd.quantity * bd.price * (1-bd.discount)) - SUM(bd.quantity * p.price_import) AS LoiNhuan
            FROM 
                dbo.Bill b
            JOIN 
                dbo.Bill_detail bd ON b.id_bill = bd.id_bill
            JOIN 
                dbo.Products p ON bd.id_prod = p.id_prod
            WHERE 
                b.date BETWEEN ? AND ?
            GROUP BY 
                p.id_prod, p.name
            ORDER BY 
                p.id_prod
            """

            cursor.execute(query, (from_date_sql, to_date_sql))
            rows = cursor.fetchall()

            data = []
            total_quantity = 0
            total_revenue = 0
            total_cost = 0
            total_profit = 0

            for row in rows:
                id_prod = row[0]
                name = row[1]
                quantity = row[2] if row[2] is not None else 0
                revenue = row[3] if row[3] is not None else 0
                cost = row[4] if row[4] is not None else 0
                profit = row[5] if row[5] is not None else 0

                data.append((id_prod, name, quantity, revenue, cost, profit))

                # Cộng dồn vào tổng
                total_quantity += quantity
                total_revenue += revenue
                total_cost += cost
                total_profit += profit

            return data, total_quantity, total_revenue, total_cost, total_profit

        except Exception as e:
            print(f"Lỗi khi lấy thống kê sản phẩm: {e}")
            # Trả về giá trị mặc định khi có lỗi
            return [], 0, 0, 0, 0

    def get_daily_statistics(self, from_date, to_date):
        try:
            # Chuyển đổi định dạng ngày
            from_date_obj = datetime.datetime.strptime(from_date, "%d-%m-%Y")
            to_date_obj = datetime.datetime.strptime(to_date, "%d-%m-%Y")

            # Định dạng lại cho SQL Server
            from_date_sql = from_date_obj.strftime("%Y-%m-%d")
            to_date_sql = to_date_obj.strftime("%Y-%m-%d") + " 23:59:59"

            cursor = self.connection.cursor()

            query = """
            SELECT 
                CONVERT(varchar, b.date, 103) AS NgayBan,
                SUM(bd.quantity * bd.price * (1-bd.discount)) AS DoanhThu
            FROM 
                dbo.Bill b
            JOIN 
                dbo.Bill_detail bd ON b.id_bill = bd.id_bill
            WHERE 
                b.date BETWEEN ? AND ?
            GROUP BY 
                CONVERT(varchar, b.date, 103),
                CONVERT(date, b.date)
            ORDER BY 
                CONVERT(date, b.date)
            """

            cursor.execute(query, (from_date_sql, to_date_sql))
            rows = cursor.fetchall()

            dates = []
            revenues = []

            for row in rows:
                date_str, revenue = row
                dates.append(date_str)  # Ngày đã được định dạng từ SQL
                revenues.append(float(revenue))

            cursor.close()
            return dates, revenues

        except Exception as e:
            print(f"Lỗi khi lấy thống kê theo ngày: {e}")
            return [], []