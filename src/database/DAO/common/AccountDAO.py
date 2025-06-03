# app/database/dao/AccountDAO.py

from src.database.models.account import Account
from src.database.connection import create_connection
import datetime


class AccountDAO:
    """
    Data Access Object cho bảng dbo.Accounts
    """

    @staticmethod
    def get_account_by_id(account_id):
        """
        Lấy thông tin tài khoản theo ID
        """
        try:
            connection = create_connection()
            cursor = connection.cursor()

            query = """
                SELECT id_account, username, password, id_emp, id_ad, role, is_active, created_at
                FROM dbo.Accounts
                WHERE id_account = ?
            """
            cursor.execute(query, (account_id,))
            row = cursor.fetchone()

            if row:
                account = Account(
                    id_account=row[0],
                    username=row[1],
                    password=row[2],
                    id_emp=row[3],
                    id_ad=row[4],
                    role=row[5],
                    is_active=row[6],
                    created_at=row[7]
                )
                return account
            return None

        except Exception as e:
            print(f"Error in get_account_by_id: {e}")
            return None
        finally:
            if 'connection' in locals() and connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_account_by_employee_id(employee_id):
        """
        Lấy thông tin tài khoản theo ID nhân viên
        """
        try:
            connection = create_connection()
            cursor = connection.cursor()

            query = """
                SELECT id_account, username, password, id_emp, id_ad, role, is_active, created_at
                FROM dbo.Accounts
                WHERE id_emp = ?
            """
            cursor.execute(query, (employee_id,))
            row = cursor.fetchone()

            if row:
                account = Account(
                    id_account=row[0],
                    username=row[1],
                    password=row[2],
                    id_emp=row[3],
                    id_ad=row[4],
                    role=row[5],
                    is_active=row[6],
                    created_at=row[7]
                )
                return account
            return None

        except Exception as e:
            print(f"Error in get_account_by_employee_id: {e}")
            return None
        finally:
            if 'connection' in locals() and connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_account_by_username(username):
        """
        Lấy thông tin tài khoản theo username
        """
        try:
            connection = create_connection()
            cursor = connection.cursor()

            query = """
                SELECT id_account, username, password, id_emp, id_ad, role, is_active, created_at
                FROM dbo.Accounts
                WHERE username = ?
            """
            cursor.execute(query, (username,))
            row = cursor.fetchone()

            if row:
                account = Account(
                    id_account=row[0],
                    username=row[1],
                    password=row[2],
                    id_emp=row[3],
                    id_ad=row[4],
                    role=row[5],
                    is_active=row[6],
                    created_at=row[7]
                )
                return account
            return None

        except Exception as e:
            print(f"Error in get_account_by_username: {e}")
            return None
        finally:
            if 'connection' in locals() and connection:
                cursor.close()
                connection.close()

    @staticmethod
    def check_username_exists(username, exclude_emp_id=None):
        """
        Kiểm tra xem username đã tồn tại chưa
        Nếu exclude_emp_id được cung cấp, kiểm tra sẽ loại trừ tài khoản của nhân viên này
        """
        try:
            connection = create_connection()
            cursor = connection.cursor()

            if exclude_emp_id is not None:
                query = """
                    SELECT COUNT(*) 
                    FROM dbo.Accounts
                    WHERE username = ? AND (id_emp IS NULL OR id_emp <> ?)
                """
                cursor.execute(query, (username, exclude_emp_id))
            else:
                query = """
                    SELECT COUNT(*) 
                    FROM dbo.Accounts
                    WHERE username = ?
                """
                cursor.execute(query, (username,))

            count = cursor.fetchone()[0]
            return count > 0

        except Exception as e:
            print(f"Error in check_username_exists: {e}")
            return False
        finally:
            if 'connection' in locals() and connection:
                cursor.close()
                connection.close()
