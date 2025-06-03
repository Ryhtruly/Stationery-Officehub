# app/database/dao/EmployeeDAO.py

from src.database.models.employee import NhanVien
from src.database.models.account import Account
from src.database.connection import create_connection
from src.database.DAO.common.AccountDAO import AccountDAO
import datetime

class EmployeeDAO:
    """
    Data Access Object cho bảng dbo.Employees
    """

    @staticmethod
    def get_all_nhan_vien():
        """
        Lấy tất cả nhân viên từ database
        """
        nhan_vien_list = []
        try:
            connection = create_connection()
            cursor = connection.cursor()

            query = """
                SELECT id_emp, fullname, address, phone, salary, email, status
                FROM Employees
                ORDER BY id_emp
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                nhan_vien = NhanVien(
                    id_emp=row[0],
                    fullname=row[1],
                    address=row[2],
                    phone=row[3],
                    salary=row[4],
                    email=row[5],
                    status=row[6]
                )
                nhan_vien_list.append(nhan_vien)

            cursor.close()
            connection.close()

        except Exception as e:
            print(f"Error in get_all_nhan_vien: {e}")

        return nhan_vien_list

    @staticmethod
    def get_nhan_vien_by_id(id_emp):
        """
        Lấy thông tin nhân viên theo ID
        """
        try:
            connection = create_connection()
            cursor = connection.cursor()

            query = """
                SELECT id_emp, fullname, address, phone, salary, email
                FROM Employees
                WHERE id_emp = ?
            """
            cursor.execute(query, (id_emp,))
            row = cursor.fetchone()

            if row:
                nhan_vien = NhanVien(
                    id_emp=row[0],
                    fullname=row[1],
                    address=row[2],
                    phone=row[3],
                    salary=row[4],
                    email=row[5]
                )
                return nhan_vien
            return None

        except Exception as e:
            print(f"Error in get_nhan_vien_by_id: {e}")
            return None
        finally:
            if 'connection' in locals() and connection:
                cursor.close()
                connection.close()

    @staticmethod
    def search_employees_by_name(keyword):
        """
        Tìm kiếm nhân viên theo họ tên (không phân biệt hoa thường)

        Args:
            keyword (str): Từ khóa tìm kiếm

        Returns:
            list: Danh sách nhân viên phù hợp
        """
        nhan_vien_list = []
        try:
            connection = create_connection()
            cursor = connection.cursor()

            query = """
                SELECT id_emp, fullname, address, phone, salary, email, status
                FROM Employees
                WHERE LOWER(fullname) LIKE LOWER(?)
                ORDER BY id_emp
            """
            search_term = f"%{keyword}%"
            cursor.execute(query, (search_term,))
            rows = cursor.fetchall()

            for row in rows:
                nhan_vien = NhanVien(
                    id_emp=row[0],
                    fullname=row[1],
                    address=row[2],
                    phone=row[3],
                    salary=row[4],
                    email=row[5],
                    status=row[6]
                )
                nhan_vien_list.append(nhan_vien)

            cursor.close()
            connection.close()

        except Exception as e:
            print(f"Error in search_employees_by_name: {e}")

        return nhan_vien_list

    @staticmethod
    def add_nhan_vien(nhan_vien, account=None):
        """
        Thêm nhân viên mới vào database
        """
        try:
            connection = create_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM Employees WHERE id_emp = ?", (nhan_vien.id_emp,))
            count = cursor.fetchone()[0]
            if count > 0:
                cursor.close()
                connection.close()
                return False, f"ID nhân viên {nhan_vien.id_emp} đã tồn tại"

            if account:
                cursor.execute("SELECT COUNT(*) FROM Accounts WHERE username = ?", (account.username,))
                count = cursor.fetchone()[0]
                if count > 0:
                    cursor.close()
                    connection.close()
                    return False, f"Tên đăng nhập {account.username} đã tồn tại"

            connection.autocommit = False

            # Thêm nhân viên
            query = """
                INSERT INTO Employees (id_emp, fullname, address, phone, salary, email)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                nhan_vien.id_emp,
                nhan_vien.fullname,
                nhan_vien.address,
                nhan_vien.phone,
                nhan_vien.salary,
                nhan_vien.email
            ))

            if account:
                query = """
                    INSERT INTO Accounts (username, password, id_emp, role, is_active, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """
                cursor.execute(query, (
                    account.username,
                    account.password,
                    nhan_vien.id_emp,
                    account.role or 'employee',
                    account.is_active if account.is_active is not None else 1,
                    datetime.datetime.now()
                ))

            connection.commit()
            cursor.close()
            connection.close()
            return True, "Thêm nhân viên thành công"

        except Exception as e:
            if 'connection' in locals() and connection:
                connection.rollback()
            print(f"Error in add_nhan_vien: {e}")
            return False, f"Lỗi khi thêm nhân viên: {e}"

    @staticmethod
    def update_nhan_vien(nhan_vien, account=None):
        """
        Cập nhật thông tin nhân viên
        """
        try:
            connection = create_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM Employees WHERE id_emp = ?", (nhan_vien.id_emp,))
            count = cursor.fetchone()[0]
            if count == 0:
                cursor.close()
                connection.close()
                return False, f"Không tìm thấy nhân viên có ID {nhan_vien.id_emp}"

            if account:
                cursor.execute("""
                    SELECT COUNT(*) FROM Accounts 
                    WHERE username = ? AND (id_emp IS NULL OR id_emp <> ?)
                """, (account.username, nhan_vien.id_emp))
                count = cursor.fetchone()[0]
                if count > 0:
                    cursor.close()
                    connection.close()
                    return False, f"Tên đăng nhập {account.username} đã tồn tại"

            connection.autocommit = False

            query = """
                UPDATE Employees
                SET fullname = ?, address = ?, phone = ?, salary = ?, email = ?
                WHERE id_emp = ?
            """
            cursor.execute(query, (
                nhan_vien.fullname,
                nhan_vien.address,
                nhan_vien.phone,
                nhan_vien.salary,
                nhan_vien.email,
                nhan_vien.id_emp
            ))

            if account:
                cursor.execute("SELECT COUNT(*) FROM Accounts WHERE id_emp = ?", (nhan_vien.id_emp,))
                has_account = cursor.fetchone()[0] > 0

                if has_account:
                    query = """
                        UPDATE Accounts
                        SET username = ?, password = ?
                        WHERE id_emp = ?
                    """
                    cursor.execute(query, (
                        account.username,
                        account.password,
                        nhan_vien.id_emp
                    ))
                else:
                    query = """
                        INSERT INTO Accounts (username, password, id_emp, role, is_active, created_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """
                    cursor.execute(query, (
                        account.username,
                        account.password,
                        nhan_vien.id_emp,
                        account.role or 'employee',
                        account.is_active if account.is_active is not None else 1,
                        datetime.datetime.now()
                    ))

            connection.commit()
            cursor.close()
            connection.close()
            return True, "Cập nhật nhân viên thành công"

        except Exception as e:
            if 'connection' in locals() and connection:
                connection.rollback()
            print(f"Error in update_nhan_vien: {e}")
            return False, f"Lỗi khi cập nhật nhân viên: {e}"

    @staticmethod
    def check_id_exists(id_emp):
        """
        Kiểm tra xem ID nhân viên đã tồn tại chưa
        """
        try:
            connection = create_connection()
            cursor = connection.cursor()

            query = "SELECT COUNT(*) FROM Employees WHERE id_emp = ?"
            cursor.execute(query, (id_emp,))
            count = cursor.fetchone()[0]

            cursor.close()
            connection.close()
            return count > 0

        except Exception as e:
            print(f"Error in check_id_exists: {e}")
            return False

    @staticmethod
    def delete_employee(employee_id):
        try:
            conn = create_connection()
            cursor = conn.cursor()

            conn.autocommit = False

            cursor.execute("SELECT COUNT(*) FROM Employees WHERE id_emp = ?", (employee_id,))
            if cursor.fetchone()[0] == 0:
                conn.rollback()
                cursor.close()
                conn.close()
                return False

            cursor.execute("UPDATE Accounts SET id_emp = NULL WHERE id_emp = ?", (employee_id,))
            cursor.execute("SELECT COUNT(*) FROM Bill WHERE id_emp = ?", (employee_id,))
            has_bills = cursor.fetchone()[0] > 0

            if has_bills:
                cursor.execute("UPDATE Bill SET id_emp = NULL WHERE id_emp = ?", (employee_id,))
            cursor.execute("SELECT COUNT(*) FROM Import WHERE id_emp = ?", (employee_id,))
            has_imports = cursor.fetchone()[0] > 0

            if has_imports:
                cursor.execute("UPDATE Import SET id_emp = NULL WHERE id_emp = ?", (employee_id,))
            cursor.execute("DELETE FROM Employees WHERE id_emp = ?", (employee_id,))
            conn.commit()

            cursor.close()
            conn.close()

            return True

        except Exception as e:
            print(f"Lỗi khi xóa nhân viên: {str(e)}")

            if 'conn' in locals() and conn:
                conn.rollback()
                if 'cursor' in locals() and cursor:
                    cursor.close()
                conn.close()

            return False

    @staticmethod
    def toggle_employee_status(employee_id):
        """
        Chuyển đổi trạng thái nhân viên (1 -> 0 hoặc 0 -> 1) và cập nhật is_active trong Accounts

        Args:
            employee_id: ID của nhân viên

        Returns:
            tuple: (success, new_status, message)
        """
        try:
            connection = create_connection()
            cursor = connection.cursor()

            connection.autocommit = False

            query_check = "SELECT status FROM Employees WHERE id_emp = ?"
            cursor.execute(query_check, (employee_id,))
            result = cursor.fetchone()

            if not result:
                cursor.close()
                connection.close()
                return False, None, f"Không tìm thấy nhân viên có ID {employee_id}"

            current_status = result[0]
            new_status = 1 if current_status == 0 else 0
            new_is_active = 1 if new_status == 1 else 0

            query_employee = "UPDATE Employees SET status = ? WHERE id_emp = ?"
            cursor.execute(query_employee, (new_status, employee_id))

            query_account = "UPDATE Accounts SET is_active = ? WHERE id_emp = ?"
            cursor.execute(query_account, (new_is_active, employee_id))

            connection.commit()

            success = cursor.rowcount > 0

            cursor.close()
            connection.close()

            if success:
                status_message = "đã tái hoạt động" if new_status == 1 else "đã dừng làm việc"
                return True, new_status, f"Nhân viên có ID {employee_id} {status_message}"
            else:
                return False, None, "Không thể cập nhật trạng thái nhân viên"

        except Exception as e:
            if 'connection' in locals() and connection:
                connection.rollback()
            print(f"Lỗi khi cập nhật trạng thái nhân viên: {str(e)}")
            return False, None, f"Lỗi khi cập nhật trạng thái nhân viên: {str(e)}"