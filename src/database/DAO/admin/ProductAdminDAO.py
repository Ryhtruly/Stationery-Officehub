from src.database.connection import create_connection
from src.database.models.product import SanPham

class ProductDAO:
    """
    Lớp truy xuất dữ liệu sản phẩm từ database
    """

    @staticmethod
    def get_all_products():
        """
        Lấy tất cả sản phẩm từ database

        Returns:
            list: Danh sách sản phẩm
        """
        try:
            with create_connection() as conn:
                with conn.cursor() as cursor:
                    query = """
                    SELECT p.id_prod, p.name, p.unit, p.price, p.price_import, p.description, p.id_category, p.image_url
                    FROM dbo.Products p
                    """
                    cursor.execute(query)
                    products = []

                    for row in cursor.fetchall():
                        product = SanPham(
                            id_prod=row[0],
                            name=row[1],
                            unit=row[2],
                            price=row[3],
                            price_import=row[4],
                            description=row[5],
                            id_category=row[6],
                            image_url=row[7]
                        )
                        products.append(product)

                    return products
        except Exception as e:
            print(f"Lỗi khi lấy danh sách sản phẩm: {str(e)}")
            return []

    @staticmethod
    def get_product_by_id(product_id):
        """
        Lấy thông tin sản phẩm theo ID

        Args:
            product_id (str): ID sản phẩm

        Returns:
            SanPham: Đối tượng sản phẩm hoặc None nếu không tìm thấy
        """
        try:
            with create_connection() as conn:
                with conn.cursor() as cursor:
                    query = """
                    SELECT p.id_prod, p.name, p.unit, p.price, p.price_import, p.description, p.id_category, p.image_url
                    FROM dbo.Products p
                    WHERE p.id_prod = ?
                    """
                    cursor.execute(query, (product_id,))
                    row = cursor.fetchone()

                    if row:
                        product = SanPham(
                            id_prod=row[0],
                            name=row[1],
                            unit=row[2],
                            price=row[3],
                            price_import=row[4],
                            description=row[5],
                            id_category=row[6],
                            image_url=row[7]
                        )
                        return product
                    return None
        except Exception as e:
            print(f"Lỗi khi lấy thông tin sản phẩm: {str(e)}")
            return None

    @staticmethod
    def get_product_name_by_id(product_id):
        """
        Lấy tên sản phẩm theo ID

        Args:
            product_id (int): ID sản phẩm

        Returns:
            str: Tên sản phẩm hoặc "Không xác định" nếu không tìm thấy
        """
        try:
            print(f"Kết nối database để lấy tên sản phẩm với id_prod: {product_id}")
            with create_connection() as conn:
                if conn is None:
                    print("Không thể kết nối đến database")
                    return "Không xác định"

                print("Tạo cursor để thực hiện truy vấn")
                with conn.cursor() as cursor:
                    query = """
                    SELECT name
                    FROM dbo.Products
                    WHERE id_prod = ?
                    """
                    print(f"Thực hiện truy vấn với id_prod: {product_id}")
                    cursor.execute(query, (product_id,))
                    row = cursor.fetchone()

                    if row:
                        product_name = row[0] if row[0] is not None else "Không xác định"
                        print(f"Tìm thấy tên sản phẩm: {product_name}")
                        return product_name
                    print(f"Không tìm thấy sản phẩm với id_prod: {product_id}")
                    return "Không xác định"
        except Exception as e:
            print(f"Lỗi khi lấy tên sản phẩm với id_prod {product_id}: {str(e)}")
            return "Không xác định"

    @staticmethod
    def search_products_by_name(keyword):
        """
        Tìm kiếm sản phẩm theo tên (không phân biệt hoa thường)

        Args:
            keyword (str): Từ khóa tìm kiếm

        Returns:
            list: Danh sách sản phẩm phù hợp
        """
        try:
            with create_connection() as conn:
                with conn.cursor() as cursor:
                    query = """
                    SELECT p.id_prod, p.name, p.unit, p.price, p.price_import, p.description, p.id_category, p.image_url
                    FROM dbo.Products p
                    WHERE LOWER(p.name) LIKE LOWER(?)
                    """
                    search_term = f"%{keyword}%"
                    cursor.execute(query, (search_term,))
                    products = []

                    for row in cursor.fetchall():
                        product = SanPham(
                            id_prod=row[0],
                            name=row[1],
                            unit=row[2],
                            price=row[3],
                            price_import=row[4],
                            description=row[5],
                            id_category=row[6],
                            image_url=row[7]
                        )
                        products.append(product)

                    return products
        except Exception as e:
            print(f"Lỗi khi tìm kiếm sản phẩm: {str(e)}")
            return []

    @staticmethod
    def add_product(id_prod, name, unit, price_import, id_category, price=0, description=None, image_url=None, conn=None):
        """
        Thêm sản phẩm mới vào database

        Args:
            id_prod (int): ID sản phẩm
            name (str): Tên sản phẩm
            unit (str): Đơn vị tính
            price_import (float): Giá nhập
            id_category (int): ID danh mục
            price (float, optional): Giá bán, mặc định = 0
            description (str, optional): Mô tả
            image_url (str, optional): Đường dẫn hình ảnh
            conn (connection, optional): Kết nối database (dùng trong transaction)

        Returns:
            tuple: (success, message, product_id)
        """
        close_conn = False
        if conn is None:
            conn = create_connection()
            close_conn = True
            conn.autocommit = False

        try:
            with conn.cursor() as cursor:
                check_query = "SELECT COUNT(*) FROM Products WHERE id_prod = ?"
                cursor.execute(check_query, (id_prod,))
                exists = cursor.fetchone()[0] > 0

                if exists:
                    return False, f"Sản phẩm có ID {id_prod} đã tồn tại trong hệ thống.", None

                # Thêm sản phẩm mới
                query = """
                INSERT INTO Products (id_prod, name, unit, price, price_import, description, id_category, image_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(query, (id_prod, name, unit, price, price_import, description, id_category, image_url))

                if close_conn:
                    conn.commit()

                return True, "Thêm sản phẩm thành công", id_prod

        except Exception as e:
            if close_conn:
                conn.rollback()
            return False, f"Lỗi khi thêm sản phẩm: {str(e)}", None
        finally:
            if close_conn:
                conn.close()

    @staticmethod
    def update_product(product_data):
        """
        Cập nhật thông tin sản phẩm
        """
        try:
            with create_connection() as conn:
                with conn.cursor() as cursor:
                    sql = """
                    UPDATE Products 
                    SET name = ?, unit = ?, price = ?, description = ?, 
                        id_category = ?, image_url = ?
                    WHERE id_prod = ?
                    """
                    cursor.execute(sql, (
                        product_data["name"],
                        product_data["unit"],
                        product_data["price"],
                        product_data["description"],
                        product_data["id_category"],
                        product_data["image_url"],
                        product_data["id_prod"]
                    ))
                    conn.commit()
                    return True
        except Exception as e:
            print(f"Lỗi khi cập nhật sản phẩm: {str(e)}")
            return False

    @staticmethod
    def delete_product(product_id):
        """
        Xóa sản phẩm khỏi database sau khi xử lý các ràng buộc FK liên quan

        Args:
            product_id (int): ID sản phẩm cần xóa

        Returns:
            bool: True nếu xóa thành công, False nếu có lỗi
        """
        try:
            with create_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM dbo.Bill_detail WHERE id_prod = ?", (product_id,))
                    cursor.execute("DELETE FROM dbo.Import_detail WHERE id_prod = ?", (product_id,))
                    cursor.execute("DELETE FROM dbo.Warehouse_Product WHERE id_prod = ?", (product_id,))

                    cursor.execute("DELETE FROM dbo.Products WHERE id_prod = ?", (product_id,))
                    conn.commit()
                    return True
        except Exception as e:
            print(f"Lỗi khi xóa sản phẩm: {str(e)}")
            if conn:
                conn.rollback()
            return False