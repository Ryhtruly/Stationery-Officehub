import traceback
from src.database.connection import create_connection
from src.database.models.promotion import Promotion

class KhuyenMaiDAO:
    """
    Data Access Object cho bảng dbo.Promotion và Promotion_detail
    """

    def __init__(self, connection=None):
        self.connection = connection

    @staticmethod
    def get_all_khuyen_mai():
        """
        Lấy tất cả khuyến mãi từ database
        """
        khuyen_mai_list = []
        try:
            connection = create_connection()
            cursor = connection.cursor()
            query = """
                SELECT id_prom, name, start_date, end_date
                FROM dbo.Promotion
                ORDER BY id_prom DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                khuyen_mai = Promotion(
                    id_prom=row[0],
                    name=row[1],
                    start_date=row[2],
                    end_date=row[3]
                )
                khuyen_mai_list.append(khuyen_mai)

            cursor.close()
            connection.close()
        except Exception as e:
            print(f"Lỗi khi lấy danh sách khuyến mãi: {str(e)}")
            traceback.print_exc()

        return khuyen_mai_list

    @staticmethod
    def get_khuyen_mai_by_id(promotion_id):
        try:
            connection = create_connection()
            cursor = connection.cursor()
            query = """
                SELECT id_prom, name, start_date, end_date
                FROM dbo.Promotion
                WHERE id_prom = ?
            """
            cursor.execute(query, (promotion_id,))
            result = cursor.fetchone()

            if result:
                return Promotion(
                    id_prom=result[0],
                    name=result[1],
                    start_date=result[2],
                    end_date=result[3]
                )
            return None
        except Exception as e:
            print(f"Lỗi khi lấy thông tin khuyến mãi theo ID: {str(e)}")
            traceback.print_exc()
            return None
        finally:
            if connection:
                connection.close()

    @staticmethod
    def get_promotion_details(id_prom):
        """
        Lấy chi tiết khuyến mãi theo ID khuyến mãi
        """
        details = []
        try:
            connection = create_connection()
            cursor = connection.cursor()

            query = """
                SELECT id_prom, id_category, percent_discount
                FROM dbo.Promotion_detail
                WHERE id_prom = ?
            """
            cursor.execute(query, (id_prom,))
            rows = cursor.fetchall()

            for row in rows:
                percent_discount = row[2]
                # Kiểm tra và xử lý percent_discount
                if percent_discount is None:
                    print(f"percent_discount is None for id_prom {row[0]}, id_category {row[1]}")
                    percent_discount = 0.0  # Giá trị mặc định nếu NULL
                else:
                    try:
                        percent_discount = float(percent_discount)
                        if not (0 <= percent_discount <= 100):
                            print(f"Invalid percent_discount value for id_prom {row[0]}, id_category {row[1]}: {percent_discount}")
                            percent_discount = 0.0
                    except (ValueError, TypeError) as e:
                        print(f"Error converting percent_discount for id_prom {row[0]}, id_category {row[1]}: {str(e)}")
                        percent_discount = 0.0

                detail = {
                    'id_prom': row[0],
                    'id_category': row[1],
                    'percent_discount': percent_discount
                }
                details.append(detail)

            cursor.close()
            connection.close()
        except Exception as e:
            print(f"Lỗi khi lấy chi tiết khuyến mãi: {str(e)}")
            traceback.print_exc()

        return details

    @staticmethod
    def generate_next_promotion_id():
        """
        Tạo ID khuyến mãi tự động
        """
        try:
            connection = create_connection()
            cursor = connection.cursor()

            # Lấy ID lớn nhất hiện tại
            cursor.execute("SELECT MAX(id_prom) FROM dbo.Promotion")
            result = cursor.fetchone()

            max_id = result[0] if result and result[0] else 0
            new_id = max_id + 1

            cursor.close()
            connection.close()

            return new_id
        except Exception as e:
            print(f"Lỗi khi tạo ID khuyến mãi: {str(e)}")
            traceback.print_exc()
            return 1  # Giá trị mặc định nếu có lỗi

    @staticmethod
    def add_promotion(promotion, category_details):
        """
        Thêm mới khuyến mãi và chi tiết khuyến mãi

        Args:
            promotion (KhuyenMai): Đối tượng khuyến mãi
            category_details (list): Danh sách chi tiết khuyến mãi theo danh mục
                Mỗi phần tử là dict {'id_category': id, 'percent_discount': value}

        Returns:
            bool: True nếu thành công, False nếu thất bại
        """
        try:
            connection = create_connection()
            cursor = connection.cursor()

            # Thêm mới khuyến mãi
            cursor.execute("""
                INSERT INTO dbo.Promotion (id_prom, name, start_date, end_date)
                VALUES (?, ?, ?, ?)
            """, (promotion.id_prom, promotion.name, promotion.start_date,
                  promotion.end_date))

            # Thêm chi tiết khuyến mãi
            for detail in category_details:
                cursor.execute("""
                    INSERT INTO dbo.Promotion_detail (id_prom, id_category, percent_discount)
                    VALUES (?, ?, ?)
                """, (promotion.id_prom, detail['id_category'], detail['percent_discount']))

            connection.commit()
            cursor.close()
            connection.close()
            return True

        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Lỗi khi thêm khuyến mãi: {str(e)}")
            traceback.print_exc()
            return False

    @staticmethod
    def update_promotion(promotion, category_details):
        """
        Cập nhật khuyến mãi và chi tiết khuyến mãi

        Args:
            promotion (KhuyenMai): Đối tượng khuyến mãi
            category_details (list): Danh sách chi tiết khuyến mãi theo danh mục
                Mỗi phần tử là dict {'id_category': id, 'percent_discount': value}

        Returns:
            bool: True nếu thành công, False nếu thất bại
        """
        try:
            connection = create_connection()
            cursor = connection.cursor()

            # Cập nhật khuyến mãi
            cursor.execute("""
                UPDATE dbo.Promotion
                SET name = ?, start_date = ?, end_date = ?
                WHERE id_prom = ?
            """, (promotion.name, promotion.start_date, promotion.end_date,
                  promotion.id_prom))

            # Xóa chi tiết khuyến mãi cũ
            cursor.execute("""
                DELETE FROM dbo.Promotion_detail
                WHERE id_prom = ?
            """, (promotion.id_prom,))

            # Thêm chi tiết khuyến mãi mới
            for detail in category_details:
                cursor.execute("""
                    INSERT INTO dbo.Promotion_detail (id_prom, id_category, percent_discount)
                    VALUES (?, ?, ?)
                """, (promotion.id_prom, detail['id_category'], detail['percent_discount']))

            connection.commit()
            cursor.close()
            connection.close()
            return True

        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Lỗi khi cập nhật khuyến mãi: {str(e)}")
            traceback.print_exc()
            return False

    @staticmethod
    def delete_promotion(id_prom):
        """
        Xóa khuyến mãi và chi tiết khuyến mãi

        Args:
            id_prom: ID của khuyến mãi cần xóa

        Returns:
            bool: True nếu thành công, False nếu thất bại
        """
        try:
            connection = create_connection()
            cursor = connection.cursor()

            # Xóa chi tiết khuyến mãi trước
            cursor.execute("""
                DELETE FROM dbo.Promotion_detail
                WHERE id_prom = ?
            """, (id_prom,))

            # Sau đó xóa khuyến mãi
            cursor.execute("""
                DELETE FROM dbo.Promotion
                WHERE id_prom = ?
            """, (id_prom,))

            connection.commit()
            cursor.close()
            connection.close()
            return True

        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Lỗi khi xóa khuyến mãi: {str(e)}")
            traceback.print_exc()
            return False