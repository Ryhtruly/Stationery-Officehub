# src/modules/login/data/login_data.py

import re
from typing import Optional, Dict, Any, Tuple
from src.database.DAO.login.LoginDAO import LoginDAO
from src.database.connection import create_connection


class LoginData:
    """
    Lớp xử lý logic cho đăng nhập và đăng ký
    """

    @staticmethod
    def validate_login(username: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        if not username or not password:
            return False, "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.", None

        user_info = LoginDAO.authenticate_user(username, password)
        print(f"user_info from LoginDAO: {user_info}")  # Log để debug

        if user_info:
            try:
                connection = create_connection()
                cursor = connection.cursor()

                # Truy vấn kiểm tra is_active
                query = """
                    SELECT id_account, is_active, role
                    FROM Accounts
                    WHERE username = ? AND password = ?
                """
                cursor.execute(query, (username, password))
                row = cursor.fetchone()
                print(f"Account validation result: {row}")  # Log để debug

                if row:
                    id_account, is_active, role = row

                    # Kiểm tra is_active
                    if is_active == 0:
                        print(f"Account disabled: is_active = {is_active}")  # Log để debug
                        return False, "Tài khoản đã vô hiệu hóa.", None

                    # Trả về user_info nếu hợp lệ
                    return True, "Đăng nhập thành công.", {
                        "account_id": id_account,
                        "role": role
                    }
                else:
                    print(f"No account found for username: {username}")
                    return False, "Tên đăng nhập hoặc mật khẩu không đúng.", None

            except Exception as e:
                print(f"Error validating account: {e}")
                return False, "Lỗi hệ thống khi kiểm tra trạng thái tài khoản.", None
            finally:
                if 'connection' in locals() and connection:
                    cursor.close()
                    connection.close()
        else:
            print(f"LoginDAO authentication failed for username: {username}")
            return False, "Tên đăng nhập hoặc mật khẩu không đúng.", None

    @staticmethod
    def validate_signup_data(sdt_email: str, username: str, password: str, confirm_password: str) -> Tuple[bool, str]:
        """
        Kiểm tra tính hợp lệ của dữ liệu đăng ký

        Args:
            sdt_email: Email hoặc số điện thoại
            username: Tên đăng nhập
            password: Mật khẩu
            confirm_password: Xác nhận mật khẩu

        Returns:
            Tuple (hợp lệ, thông báo lỗi)
        """
        if not sdt_email or not username or not password or not confirm_password:
            return False, "Vui lòng điền đầy đủ thông tin."

        is_email = "@" in sdt_email
        if is_email:
            email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(email_pattern, sdt_email):
                return False, "Email không hợp lệ."
        else:
            phone_pattern = r'^[0-9]{10}$'
            if not re.match(phone_pattern, sdt_email):
                return False, "Số điện thoại không hợp lệ (phải có 10 số)."

        if password != confirm_password:
            return False, "Mật khẩu xác nhận không khớp."

        if len(password) < 6:
            return False, "Mật khẩu phải có ít nhất 6 ký tự."

        if LoginDAO.check_username_exists(username):
            return False, "Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác."

        if is_email:
            if LoginDAO.check_contact_exists(email=sdt_email):
                return False, "Email đã được sử dụng. Vui lòng sử dụng email khác."
        else:
            if LoginDAO.check_contact_exists(phone=sdt_email):
                return False, "Số điện thoại đã được sử dụng. Vui lòng sử dụng số khác."

        return True, ""

    @staticmethod
    def register_user(sdt_email: str, username: str, password: str) -> Tuple[bool, str]:
        """
        Đăng ký người dùng mới

        Args:
            sdt_email: Email hoặc số điện thoại
            username: Tên đăng nhập
            password: Mật khẩu

        Returns:
            Tuple (thành công, thông báo)
        """
        is_email = "@" in sdt_email

        # Đăng ký nhân viên mới và liên kết với tài khoản
        success = LoginDAO.register_user(sdt_email, username, password)

        if success:
            return True, "Đăng ký tài khoản thành công!"
        else:
            return False, "Có lỗi xảy ra khi đăng ký. Vui lòng thử lại sau."# src/modules/login/data/login_data.py

import re
from typing import Optional, Dict, Any, Tuple
from src.database.DAO.login.LoginDAO import LoginDAO
from src.database.connection import create_connection


class LoginData:
    """
    Lớp xử lý logic cho đăng nhập và đăng ký
    """

    @staticmethod
    def validate_login(username: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        if not username or not password:
            return False, "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.", None

        user_info = LoginDAO.authenticate_user(username, password)
        print(f"user_info from LoginDAO: {user_info}")  # Log để debug

        if user_info:
            try:
                connection = create_connection()
                cursor = connection.cursor()

                # Truy vấn kiểm tra is_active
                query = """
                    SELECT id_account, is_active, role
                    FROM Accounts
                    WHERE username = ? AND password = ?
                """
                cursor.execute(query, (username, password))
                row = cursor.fetchone()
                print(f"Account validation result: {row}")  # Log để debug

                if row:
                    id_account, is_active, role = row

                    # Kiểm tra is_active
                    if is_active == 0:
                        print(f"Account disabled: is_active = {is_active}")  # Log để debug
                        return False, "Tài khoản đã vô hiệu hóa.", None

                    # Trả về user_info nếu hợp lệ
                    return True, "Đăng nhập thành công.", {
                        "account_id": id_account,
                        "role": role
                    }
                else:
                    print(f"No account found for username: {username}")
                    return False, "Tên đăng nhập hoặc mật khẩu không đúng.", None

            except Exception as e:
                print(f"Error validating account: {e}")
                return False, "Lỗi hệ thống khi kiểm tra trạng thái tài khoản.", None
            finally:
                if 'connection' in locals() and connection:
                    cursor.close()
                    connection.close()
        else:
            print(f"LoginDAO authentication failed for username: {username}")
            return False, "Tên đăng nhập hoặc mật khẩu không đúng.", None

    @staticmethod
    def validate_signup_data(sdt_email: str, username: str, password: str, confirm_password: str) -> Tuple[bool, str]:
        """
        Kiểm tra tính hợp lệ của dữ liệu đăng ký

        Args:
            sdt_email: Email hoặc số điện thoại
            username: Tên đăng nhập
            password: Mật khẩu
            confirm_password: Xác nhận mật khẩu

        Returns:
            Tuple (hợp lệ, thông báo lỗi)
        """
        # Kiểm tra trường rỗng
        if not sdt_email or not username or not password or not confirm_password:
            return False, "Vui lòng điền đầy đủ thông tin."

        # Kiểm tra định dạng email
        is_email = "@" in sdt_email
        if is_email:
            email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(email_pattern, sdt_email):
                return False, "Email không hợp lệ."
        # Kiểm tra định dạng số điện thoại
        else:
            phone_pattern = r'^[0-9]{10}$'
            if not re.match(phone_pattern, sdt_email):
                return False, "Số điện thoại không hợp lệ (phải có 10 số)."

        # Kiểm tra mật khẩu khớp
        if password != confirm_password:
            return False, "Mật khẩu xác nhận không khớp."

        # Kiểm tra độ dài mật khẩu
        if len(password) < 6:
            return False, "Mật khẩu phải có ít nhất 6 ký tự."

        # Kiểm tra username đã tồn tại chưa
        if LoginDAO.check_username_exists(username):
            return False, "Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác."

        # Kiểm tra email/sdt đã tồn tại chưa
        if is_email:
            if LoginDAO.check_contact_exists(email=sdt_email):
                return False, "Email đã được sử dụng. Vui lòng sử dụng email khác."
        else:
            if LoginDAO.check_contact_exists(phone=sdt_email):
                return False, "Số điện thoại đã được sử dụng. Vui lòng sử dụng số khác."

        return True, ""

    @staticmethod
    def register_user(sdt_email: str, username: str, password: str) -> Tuple[bool, str]:
        """
        Đăng ký người dùng mới

        Args:
            sdt_email: Email hoặc số điện thoại
            username: Tên đăng nhập
            password: Mật khẩu

        Returns:
            Tuple (thành công, thông báo)
        """
        is_email = "@" in sdt_email

        # Đăng ký nhân viên mới và liên kết với tài khoản
        success = LoginDAO.register_user(sdt_email, username, password)

        if success:
            return True, "Đăng ký tài khoản thành công!"
        else:
            return False, "Có lỗi xảy ra khi đăng ký. Vui lòng thử lại sau."