import pyodbc
class CardDAO:
    def __init__(self, connection):
        self.conn = connection

    def get_discount_by_rank(self, rank):
        """
        Lấy giá trị discount từ bảng Card dựa trên rank.

        Args:
            rank (str): Hạng của khách hàng (Bronze, Silver, Gold, Platinum, Diamond).

        Returns:
            float: Giá trị discount, mặc định là 0.0 nếu không tìm thấy.
        """
        try:
            cursor = self.conn.cursor()
            query = "SELECT discount FROM dbo.Card WHERE rank = ?"
            cursor.execute(query, (rank,))
            row = cursor.fetchone()
            if row and row[0] is not None:
                return float(row[0])
            return 0.0  # Trả về 0.0 nếu không tìm thấy rank hoặc discount là NULL
        except pyodbc.Error as e:
            print(f"Lỗi khi lấy discount từ bảng Card: {str(e)}")
            return 0.0
        finally:
            cursor.close()