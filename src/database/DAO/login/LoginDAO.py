from typing import Optional, Dict, Any
import sys
import os

# Thêm đường dẫn gốc vào sys.path để import được các module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.database.connection import create_connection


class LoginDAO:
    """
    Data Access Object cho các thao tác liên quan đến đăng nhập và đăng ký
    """

    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
        try:
            connection = create_connection()
            cursor = connection.cursor()
            query = """
                SELECT id_account, username, role
                FROM dbo.Accounts
                WHERE username = ? AND password = ? AND is_active = 1
            """
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            print(f"Result from authenticate_user: {result}")  # Debug line
            if result:
                return {'account_id': result[0], 'username': result[1], 'role': result[2]}
            else:
                return None
        except Exception as e:
            print(f"Lỗi khi xác thực người dùng: {e}")
            return None

    @staticmethod
    def check_username_exists(username: str) -> bool:
        """Kiểm tra xem tên đăng nhập đã tồn tại chưa"""
        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Accounts WHERE username = ?", (username,))
            return cursor.fetchone() is not None
        except Exception as e:
            print(f"Lỗi kiểm tra username: {e}")
            return False
        finally:
            if 'connection' in locals() and connection:
                connection.close()

    @staticmethod
    def check_contact_exists(email: str = None, phone: str = None) -> bool:
        """Kiểm tra xem email hoặc số điện thoại đã tồn tại chưa"""
        try:
            connection = create_connection()
            cursor = connection.cursor()
            if email:
                # Kiểm tra trong cả Employees và Admin
                cursor.execute("SELECT * FROM Employees WHERE email = ?", (email,))
                if cursor.fetchone():
                    return True
                cursor.execute("SELECT * FROM Admin WHERE email = ?", (email,))
                return cursor.fetchone() is not None
            elif phone:
                cursor.execute("SELECT * FROM Employees WHERE phone = ?", (phone,))
                if cursor.fetchone():
                    return True
                cursor.execute("SELECT * FROM Admin WHERE phone = ?", (phone,))
                return cursor.fetchone() is not None
            else:
                return False

        except Exception as e:
            print(f"Lỗi kiểm tra contact: {e}")
            return False
        finally:
            if 'connection' in locals() and connection:
                connection.close()

    @staticmethod
    def register_user(sdt_email: str, username: str, password: str) -> bool:
        """
        Đăng ký người dùng mới

        Args:
            sdt_email: Email hoặc số điện thoại
            username: Tên đăng nhập
            password: Mật khẩu

        Returns:
            True nếu đăng ký thành công, False nếu thất bại
        """
        connection = None
        try:
            connection = create_connection()
            cursor = connection.cursor()

            # Bắt đầu transaction để đảm bảo tính toàn vẹn dữ liệu
            connection.autocommit = False

            # Lấy id_emp lớn nhất hiện tại và tăng lên 1
            cursor.execute("SELECT MAX(id_emp) FROM Employees WITH (UPDLOCK, HOLDLOCK)")
            max_id = cursor.fetchone()[0]
            new_id_emp = (max_id if max_id is not None else 0) + 1

            # Phân loại sdt_email thành email hoặc phone
            is_email = "@" in sdt_email
            email = sdt_email if is_email else None
            phone = sdt_email if not is_email else None

            # Thêm nhân viên mới vào bảng Employees với id_emp được sinh thủ công
            cursor.execute(
                """
                INSERT INTO Employees (id_emp, fullname, phone, email, salary, status)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (new_id_emp, username, phone, email, 0.0, 1)  # salary mặc định 0, status mặc định 1
            )

            # Thêm tài khoản vào bảng Accounts với role là "employee"
            cursor.execute(
                """
                INSERT INTO Accounts (username, password, id_emp, role, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, GETDATE())
                """,
                (username, password, new_id_emp, "employee", 1)  # role mặc định là employee, is_active = 1
            )

            # Commit transaction
            connection.commit()
            print(f"Registered new employee with id_emp: {new_id_emp}, username: {username}")
            return True

        except Exception as e:
            print(f"Lỗi đăng ký: {e}")
            if connection:
                connection.rollback()
            return False
        finally:
            if 'connection' in locals() and connection:
                cursor.close()
                connection.close()