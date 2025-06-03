from src.database.connection import create_connection
from src.database.models.category import DanhMuc

class CategoryDAO:
    """
    Lớp truy xuất dữ liệu danh mục từ database
    """

    @staticmethod
    def get_all_categories():
        """
        Lấy tất cả danh mục từ database

        Returns:
            list: Danh sách danh mục
        """
        conn = None
        cursor = None
        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = """
            SELECT id_category, name
            FROM dbo.Categories
            """

            cursor.execute(query)
            categories = []

            for row in cursor.fetchall():
                print(f"Raw category row from database: {row}")
                category = DanhMuc(
                    id_category=row[0],
                    name=row[1] if row[1] else "Chưa đặt tên",
                    description=""
                )
                categories.append(category)

            print(f"Loaded {len(categories)} categories from database")
            return categories

        except Exception as e:
            print(f"Lỗi khi lấy danh sách danh mục: {str(e)}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_category_by_id(category_id):
        """
        Lấy thông tin danh mục theo ID

        Args:
            category_id: ID của danh mục cần lấy (int hoặc str)

        Returns:
            DanhMuc: Đối tượng danh mục nếu tìm thấy, None nếu không tìm thấy
        """
        conn = None
        cursor = None
        try:
            # Chuyển category_id thành int để đảm bảo đúng kiểu dữ liệu
            category_id = int(category_id)
            conn = create_connection()
            cursor = conn.cursor()

            query = """
            SELECT id_category, name 
            FROM dbo.Categories 
            WHERE id_category = ?
            """

            cursor.execute(query, (category_id,))
            row = cursor.fetchone()

            if row:
                print(f"Found category for ID {category_id}: {row}")
                return DanhMuc(
                    id_category=row[0],
                    name=row[1] if row[1] else "Chưa đặt tên",
                    description=""
                )
            print(f"Không tìm thấy danh mục có ID: {category_id}")
            return None
        except ValueError:
            print(f"Invalid category ID format: {category_id}")
            return None
        except Exception as e:
            print(f"Error in get_category_by_id for ID {category_id}: {str(e)}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def insert_category(category):
        """
        Thêm danh mục mới vào database

        Args:
            category (DanhMuc): Đối tượng danh mục cần thêm

        Returns:
            bool: True nếu thành công, False nếu thất bại
        """
        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO dbo.Categories (id_category, name)
            VALUES (?, ?)
            """

            cursor.execute(query, (
                category.id_category,
                category.name
            ))

            conn.commit()
            return True

        except Exception as e:
            print(f"Lỗi khi thêm danh mục: {str(e)}")
            return False
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update_category(category_id, name, description=""):
        """
        Cập nhật thông tin danh mục trong database

        Args:
            category_id: ID của danh mục cần cập nhật
            name: Tên danh mục mới
            description: Mô tả danh mục mới (mặc định là chuỗi rỗng)

        Returns:
            bool: True nếu cập nhật thành công, False nếu thất bại
        """
        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = """
            UPDATE dbo.Categories
            SET name = ?
            WHERE id_category = ?
            """

            cursor.execute(query, (name, category_id))
            conn.commit()

            print(f"Đã cập nhật danh mục có ID {category_id} thành: {name}")
            return True

        except Exception as e:
            print(f"Lỗi khi cập nhật danh mục: {e}")
            return False

    @staticmethod
    def delete_category(category_id):
        """
        Xóa danh mục khỏi database

        Args:
            category_id (str): ID danh mục cần xóa

        Returns:
            bool: True nếu thành công, False nếu thất bại
        """
        conn = None
        cursor = None
        try:
            conn = create_connection()
            cursor = conn.cursor()

            check_query = """
            SELECT COUNT(*) FROM dbo.Products WHERE id_category = ?
            """
            cursor.execute(check_query, (category_id,))
            count = cursor.fetchone()[0]

            if count > 0:
                print(f"Không thể xóa danh mục {category_id} vì có {count} sản phẩm thuộc danh mục này")
                return False

            delete_query = """
            DELETE FROM dbo.Categories WHERE id_category = ?
            """
            cursor.execute(delete_query, (category_id,))

            conn.commit()
            return True

        except Exception as e:
            print(f"Lỗi khi xóa danh mục: {str(e)}")
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def search_categories(keyword):
        """
        Tìm kiếm danh mục theo từ khóa

        Args:
            keyword (str): Từ khóa tìm kiếm

        Returns:
            list: Danh sách danh mục phù hợp
        """
        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = """
            SELECT c.id_category, c.name
            FROM dbo.Categories c
            WHERE CAST(c.id_category AS VARCHAR) LIKE ? OR c.name LIKE ?
            """

            search_param = f'%{keyword}%'
            cursor.execute(query, (search_param, search_param))

            categories = []
            for row in cursor.fetchall():
                category = DanhMuc(
                    id_category=row[0],
                    name=row[1] if row[1] else "Chưa đặt tên",
                    description=""
                )
                categories.append(category)

            return categories

        except Exception as e:
            print(f"Lỗi khi tìm kiếm danh mục: {str(e)}")
            return []
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def add_category(name, description=""):
        """
        Thêm danh mục mới vào database

        Args:
            name: Tên danh mục
            description: Mô tả danh mục (mặc định là chuỗi rỗng)

        Returns:
            bool: True nếu thêm thành công, False nếu thất bại
        """
        try:
            conn = create_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT MAX(id_category) FROM dbo.Categories")
            result = cursor.fetchone()
            max_id = result[0] if result[0] is not None else 0
            new_id = max_id + 1

            query = """
            INSERT INTO dbo.Categories (id_category, name)
            VALUES (?, ?)
            """

            cursor.execute(query, (new_id, name))
            conn.commit()

            print(f"Đã thêm danh mục: {name} với ID: {new_id}")
            return True

        except Exception as e:
            print(f"Lỗi khi thêm danh mục: {e}")
            return False