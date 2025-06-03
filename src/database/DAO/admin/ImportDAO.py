from src.database.connection import create_connection
from src.database.models.import_product import NhapHang
from datetime import datetime

class NhapHangDAO:
    """
    Lớp truy xuất dữ liệu phiếu nhập hàng từ database
    """

    @staticmethod
    def get_all_phieu_nhap():
        """
        Lấy tất cả phiếu nhập từ database

        Returns:
            list: Danh sách phiếu nhập
        """
        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = """
            SELECT i.id_imp AS ID, 
                   i.id_emp AS ID_Emp, 
                   e.fullname AS Employee_Name, 
                   i.date AS Date_Import,
                   (SELECT SUM(ct.quantity * ct.price) 
                    FROM dbo.Import_detail ct 
                    WHERE ct.id_imp = i.id_imp) AS total_price
            FROM dbo.Import i
            LEFT JOIN dbo.Employees e ON i.id_emp = e.id_emp
            ORDER BY i.date DESC
            """

            cursor.execute(query)
            phieu_nhap_list = []

            for row in cursor.fetchall():
                date_str = row[3].strftime('%d-%m-%Y %H:%M:%S') if row[3] else ""

                phieu_nhap = NhapHang(
                    id_imp=row[0],
                    id_emp=row[1],
                    employee_name=row[2],
                    date=date_str,
                    total_price=row[4] if row[4] else 0
                )
                phieu_nhap_list.append(phieu_nhap)

            return phieu_nhap_list
        except Exception as e:
            print(f"Lỗi khi lấy danh sách phiếu nhập: {e}")
            return []
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete_phieu_nhap(phieu_id):
        """
        Xóa phiếu nhập từ database

        Args:
            phieu_id: ID của phiếu nhập cần xóa

        Returns:
            bool: True nếu xóa thành công, False nếu thất bại
        """
        try:
            conn = create_connection()
            cursor = conn.cursor()

            query_detail = "DELETE FROM dbo.Import_detail WHERE id_imp = ?"
            cursor.execute(query_detail, (phieu_id,))

            query_import = "DELETE FROM dbo.Import WHERE id_imp = ?"
            cursor.execute(query_import, (phieu_id,))

            conn.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi xóa phiếu nhập: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def create_phieu_nhap(phieu_nhap_data):
        """
        Tạo phiếu nhập mới trong database

        Args:
            phieu_nhap_data (dict): Dữ liệu phiếu nhập, bao gồm id_emp và các thông tin khác

        Returns:
            tuple: (success, id_imp) - success là True nếu thành công, id_imp là ID của phiếu nhập mới
        """
        try:
            conn = create_connection()
            cursor = conn.cursor()

            current_date = datetime.now()

            query = """
            INSERT INTO dbo.Import (id_emp, date)
            VALUES (?, ?)
            """

            cursor.execute(query, (phieu_nhap_data['id_emp'], current_date))

            cursor.execute("SELECT @@IDENTITY")
            id_imp = cursor.fetchone()[0]

            conn.commit()

            cursor.close()
            conn.close()

            return True, id_imp
        except Exception as e:
            print(f"Lỗi khi tạo phiếu nhập: {str(e)}")
            return False, None

    @staticmethod
    def add_phieu_nhap(import_data, new_products=None):
        """
        Thêm phiếu nhập hàng vào cơ sở dữ liệu với transaction

        Args:
            import_data: Dữ liệu phiếu nhập từ form
            new_products: Danh sách sản phẩm mới cần thêm vào Products (nếu có)

        Returns:
            tuple: (success, message, id_phieu_nhap)
        """
        id_imp = import_data.get('id_phieu_nhap')
        id_emp = import_data.get('id_nhan_vien')
        product_list = import_data.get('san_pham_list', [])

        if not id_imp or not id_emp or not product_list:
            return False, "Dữ liệu phiếu nhập không hợp lệ: Thiếu ID phiếu nhập, ID nhân viên hoặc danh sách sản phẩm.", None

        conn = None
        try:
            conn = create_connection()
            with conn:
                conn.autocommit = False  # Tắt autocommit để sử dụng transaction
                cursor = conn.cursor()

                cursor.execute("SELECT COUNT(*) FROM dbo.Import WHERE id_imp = ?", (id_imp,))
                if cursor.fetchone()[0] > 0:
                    raise ValueError(f"ID phiếu nhập {id_imp} đã tồn tại.")

                query_import = """
                    INSERT INTO dbo.Import (id_imp, id_emp, date)
                    VALUES (?, ?, GETDATE())
                """
                cursor.execute(query_import, (id_imp, id_emp))

                if new_products:
                    query_product = """
                        INSERT INTO dbo.Products (id_prod, name, unit, price, price_import, description, id_category, image_url)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    for product in new_products:
                        cursor.execute(query_product, (
                            product['id'],
                            product['name'],
                            product['unit'],
                            product.get('price', 0),
                            product['price_import'],
                            product.get('description'),
                            product['id_category'],
                            product.get('image_url')
                        ))

                query_detail = """
                    INSERT INTO dbo.Import_detail 
                    (id_imp, id_prod, quantity, price)
                    VALUES (?, ?, ?, ?)
                """
                for san_pham in product_list:
                    id_prod = san_pham['id']
                    quantity = san_pham['so_luong']
                    price = san_pham['gia_nhap']
                    cursor.execute(query_detail, (id_imp, id_prod, quantity, price))

                    warehouse_name = san_pham.get('kho', '')
                    if not warehouse_name:
                        raise ValueError("Tên kho không được để trống.")

                    query_get_warehouse = """
                        SELECT id_warehouse FROM dbo.Warehouse 
                        WHERE name = ?
                    """
                    cursor.execute(query_get_warehouse, (warehouse_name,))
                    warehouse_result = cursor.fetchone()

                    if not warehouse_result:
                        raise ValueError(f"Kho '{warehouse_name}' không tồn tại.")

                    id_warehouse = warehouse_result[0]
                    query_check_warehouse_product = """
                        SELECT inventory FROM dbo.Warehouse_Product
                        WHERE id_prod = ? AND id_warehouse = ?
                    """
                    cursor.execute(query_check_warehouse_product, (id_prod, id_warehouse))
                    existing_product = cursor.fetchone()

                    if existing_product:
                        query_update_inventory = """
                            UPDATE dbo.Warehouse_Product
                            SET inventory = inventory + ?
                            WHERE id_prod = ? AND id_warehouse = ?
                        """
                        cursor.execute(query_update_inventory, (quantity, id_prod, id_warehouse))
                    else:
                        query_insert_warehouse_product = """
                            INSERT INTO dbo.Warehouse_Product
                            (id_prod, id_warehouse, inventory)
                            VALUES (?, ?, ?)
                        """
                        cursor.execute(query_insert_warehouse_product, (id_prod, id_warehouse, quantity))

                conn.commit()
                return True, "Thêm phiếu nhập thành công", id_imp

        except ValueError as ve:
            error_message = f"Lỗi dữ liệu: {str(ve)}"
            print(error_message)
            if conn:
                conn.rollback()
            return False, error_message, None
        except Exception as e:
            error_message = f"Lỗi khi thêm phiếu nhập: {str(e)}"
            print(error_message)
            if conn:
                conn.rollback()
            return False, error_message, None
        finally:
            if conn:
                conn.close()