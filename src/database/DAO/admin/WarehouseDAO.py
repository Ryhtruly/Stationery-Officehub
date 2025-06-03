from src.database.connection import create_connection
from src.database.models.warehouse import Warehouse, WarehouseProduct


class WarehouseDAO:
    """
    Lớp truy xuất dữ liệu kho hàng từ database
    """

    @staticmethod
    def get_all_warehouses():
        """
        Lấy tất cả kho hàng từ database

        Returns:
            list: Danh sách kho hàng
        """
        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = """
            SELECT id_warehouse, name, address, phone
            FROM dbo.Warehouse
            """

            cursor.execute(query)
            warehouses = []

            for row in cursor.fetchall():
                warehouse = Warehouse(
                    id_warehouse=row[0],
                    name=row[1],
                    address=row[2],
                    phone=row[3]
                )
                warehouses.append(warehouse)

            return warehouses

        except Exception as e:
            print(f"Lỗi khi lấy danh sách kho hàng: {str(e)}")
            return []
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_warehouse_products():
        """
        Lấy tất cả sản phẩm trong kho từ database

        Returns:
            list: Danh sách sản phẩm trong kho
        """
        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = """
            SELECT wp.id_warehouse, wp.id_prod, p.name, wp.inventory
            FROM dbo.Warehouse_Product wp
            JOIN dbo.Products p ON wp.id_prod = p.id_prod
            """

            cursor.execute(query)
            warehouse_products = []

            for row in cursor.fetchall():
                product = WarehouseProduct(
                    id_warehouse=row[0],
                    id_prod=row[1],
                    name=row[2],
                    inventory=row[3]
                )
                warehouse_products.append(product)

            return warehouse_products

        except Exception as e:
            print(f"Lỗi khi lấy danh sách sản phẩm trong kho: {str(e)}")
            return []
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_warehouse_products_by_warehouse_id(warehouse_id):
        """
        Lấy tất cả sản phẩm trong một kho cụ thể

        Args:
            warehouse_id: ID kho hàng

        Returns:
            list: Danh sách sản phẩm trong kho
        """
        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = """
            SELECT wp.id_warehouse, wp.id_prod, p.name, wp.inventory
            FROM dbo.Warehouse_Product wp
            JOIN dbo.Products p ON wp.id_prod = p.id_prod
            WHERE wp.id_warehouse = ?
            """

            cursor.execute(query, (warehouse_id,))
            warehouse_products = []

            for row in cursor.fetchall():
                product = WarehouseProduct(
                    id_warehouse=row[0],
                    id_prod=row[1],
                    name=row[2],
                    inventory=row[3]
                )
                warehouse_products.append(product)

            return warehouse_products

        except Exception as e:
            print(f"Lỗi khi lấy danh sách sản phẩm trong kho: {str(e)}")
            return []
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def add_product_to_warehouse(id_warehouse, id_prod, inventory):
        """
        Thêm sản phẩm vào kho

        Args:
            id_warehouse (int): ID kho
            id_prod (int): ID sản phẩm
            inventory (int): Số lượng tồn kho

        Returns:
            tuple: (success, message)
        """
        try:
            conn = create_connection()
            cursor = conn.cursor()

            # Kiểm tra xem sản phẩm đã tồn tại trong kho chưa
            check_query = "SELECT COUNT(*) FROM Warehouse_Product WHERE id_warehouse = ? AND id_prod = ?"
            cursor.execute(check_query, (id_warehouse, id_prod))
            exists = cursor.fetchone()[0] > 0

            if exists:
                # Cập nhật số lượng nếu sản phẩm đã tồn tại
                update_query = "UPDATE Warehouse_Product SET inventory = inventory + ? WHERE id_warehouse = ? AND id_prod = ?"
                cursor.execute(update_query, (inventory, id_warehouse, id_prod))
            else:
                # Thêm mới nếu sản phẩm chưa tồn tại trong kho
                insert_query = "INSERT INTO Warehouse_Product (id_warehouse, id_prod, inventory) VALUES (?, ?, ?)"
                cursor.execute(insert_query, (id_warehouse, id_prod, inventory))

            conn.commit()
            return True, "Thêm sản phẩm vào kho thành công"

        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Lỗi khi thêm sản phẩm vào kho: {str(e)}"

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
