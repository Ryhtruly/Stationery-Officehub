# ProductAdminDAO.py
from src.database.connection import create_connection

class ProductDAO:
    @staticmethod
    def get_all_products():
        try:
            conn = create_connection()
            cursor = conn.cursor()
            query = """
                SELECT p.id_prod, p.name, p.price, p.promotion_price, p.description, p.image_url, p.id_category, c.name AS category_name
                FROM Products p
                LEFT JOIN Categories c ON p.id_category = c.id_category
                ORDER BY p.name
            """
            cursor.execute(query)
            products = []

            for row in cursor.fetchall():
                product = {
                    "id": row[0],
                    "ten": row[1] or "",  # Tránh None
                    "gia": float(row[2]) if row[2] is not None else 0.0,  # Chuyển thành float
                    "promotion_price": float(row[3]) if row[3] is not None else None,
                    "display_price": float(row[3] if row[3] is not None else row[2]) if row[2] is not None else 0.0,
                    "mo_ta": row[4] or "",
                    "hinh_anh": row[5] or "",
                    "id_category": row[6] if row[6] is not None else 0,
                    "category_name": row[7] or "Chưa phân loại"
                }
                products.append(product)

            return products
        except Exception as e:
            print(f"Lỗi khi lấy danh sách sản phẩm: {str(e)}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_product_by_id(product_id):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            query = """
                SELECT p.id_prod, p.name, p.price, p.promotion_price, p.description, p.image_url, p.id_category, c.name AS category_name
                FROM Products p
                LEFT JOIN Categories c ON p.id_category = c.id_category
                WHERE p.id_prod = ?
            """
            cursor.execute(query, (product_id,))
            row = cursor.fetchone()

            if row:
                product = {
                    "id": row[0],
                    "ten": row[1] or "",
                    "gia": float(row[2]) if row[2] is not None else 0.0,
                    "promotion_price": float(row[3]) if row[3] is not None else None,
                    "display_price": float(row[3] if row[3] is not None else row[2]) if row[2] is not None else 0.0,
                    "mo_ta": row[4] or "",
                    "hinh_anh": row[5] or "",
                    "id_category": row[6] if row[6] is not None else 0,
                    "category_name": row[7] or "Chưa phân loại"
                }
                return product

            return None
        except Exception as e:
            print(f"Lỗi khi lấy thông tin sản phẩm: {str(e)}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()