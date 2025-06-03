# app/admin/data/import_detail/ImportDAO.py

from src.database.connection import create_connection
from src.database.models.import_product import NhapHang
from src.database.models.import_detail import ChiTietNhapHang

class NhapHangDAO:
    """
    Data Access Object cho bảng dbo.Import và dbo.Import_detail
    """

    @staticmethod
    def get_all_nhap_hang():
        """
        Lấy tất cả phiếu nhập từ database
        """
        nhap_hang_list = []
        try:
            with create_connection() as connection:
                with connection.cursor() as cursor:
                    query = """
                        SELECT i.id_imp, i.id_emp, e.fullname, i.date,
                               (SELECT SUM(id.quantity * id.price) 
                                FROM dbo.Import_detail id 
                                WHERE id.id_imp = i.id_imp) as total_price
                        FROM dbo.Import i
                        JOIN dbo.Employees e ON i.id_emp = e.id_emp
                        ORDER BY i.date DESC
                    """
                    cursor.execute(query)

                    for row in cursor.fetchall():
                        nhap_hang = NhapHang(
                            id_imp=row[0],
                            id_emp=row[1],
                            date=row[3]
                        )
                        nhap_hang.employee_name = row[2]
                        nhap_hang.total_price = row[4] if row[4] else 0

                        nhap_hang_list.append(nhap_hang)
        except Exception as e:
            print(f"Lỗi khi lấy danh sách phiếu nhập: {str(e)}")

        return nhap_hang_list

    @staticmethod
    def get_nhap_hang_by_id(id_imp):
        """
        Lấy thông tin phiếu nhập theo ID
        """
        try:
            with create_connection() as connection:
                with connection.cursor() as cursor:
                    query = """
                        SELECT i.id_imp, i.id_emp, e.fullname, i.date
                        FROM dbo.Import i
                        JOIN dbo.Employees e ON i.id_emp = e.id_emp
                        WHERE i.id_imp = ?
                    """
                    cursor.execute(query, (id_imp,))
                    row = cursor.fetchone()

                    if row:
                        nhap_hang = NhapHang(
                            id_imp=row[0],
                            id_emp=row[1],
                            date=row[3]
                        )
                        nhap_hang.employee_name = row[2]

                        detail_query = """
                            SELECT id.id_prod, p.name, id.quantity, id.price
                            FROM dbo.Import_detail id
                            JOIN dbo.Products p ON id.id_prod = p.id_prod
                            WHERE id.id_imp = ?
                        """
                        cursor.execute(detail_query, (id_imp,))

                        nhap_hang.chi_tiet_list = []
                        total_price = 0

                        for detail_row in cursor.fetchall():
                            chi_tiet = ChiTietNhapHang(
                                id_imp=id_imp,
                                id_prod=detail_row[0],
                                quantity=detail_row[2],
                                price=detail_row[3]
                            )
                            chi_tiet.product_name = detail_row[1]
                            chi_tiet.sub_total = chi_tiet.quantity * chi_tiet.price

                            nhap_hang.chi_tiet_list.append(chi_tiet)
                            total_price += chi_tiet.sub_total

                        nhap_hang.total_price = total_price
                        return nhap_hang

                    return None
        except Exception as e:
            print(f"Lỗi khi lấy thông tin phiếu nhập: {str(e)}")
            return None

    @staticmethod
    def them_phieu_nhap(nhap_hang, chi_tiet_list):
        """
        Thêm phiếu nhập mới vào database
        """
        try:
            with create_connection() as connection:
                with connection.cursor() as cursor:
                    # Thêm phiếu nhập
                    query = """
                        INSERT INTO dbo.Import (id_imp, id_emp, date)
                        VALUES (?, ?, ?)
                    """
                    cursor.execute(query, (nhap_hang.id_imp, nhap_hang.id_emp, nhap_hang.date))

                    for chi_tiet in chi_tiet_list:
                        detail_query = """
                            INSERT INTO dbo.Import_detail (id_imp, id_prod, quantity, price)
                            VALUES (?, ?, ?, ?)
                        """
                        cursor.execute(detail_query, (
                            chi_tiet.id_imp,
                            chi_tiet.id_prod,
                            chi_tiet.quantity,
                            chi_tiet.price
                        ))

                        update_query = """
                            UPDATE dbo.Warehouse_Product
                            SET inventory = inventory + ?
                            WHERE id_prod = ?
                        """
                        cursor.execute(update_query, (chi_tiet.quantity, chi_tiet.id_prod))

                    connection.commit()
                    return True
        except Exception as e:
            print(f"Lỗi khi thêm phiếu nhập: {str(e)}")
            if connection:
                connection.rollback()
            return False