class AccountDetailDAO:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_account_id(self, username, password):
        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT id_account
                FROM dbo.Accounts
                WHERE username = ? AND password = ?
            """
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            print(f"get_account_id result: {result}")
            return result[0] if result else None
        except Exception as e:
            print(f"Lỗi khi lấy account_id: {e}")
            return None

    def get_user_id(self, account_id):
        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT id_emp, id_ad 
                FROM dbo.Accounts 
                WHERE id_account = ?
            """
            cursor.execute(query, (account_id,))
            result = cursor.fetchone()
            print(f"get_user_id result: {result}")
            return result[0], result[1] if result else (None, None)
        except Exception as e:
            print(f"Lỗi khi lấy ID người dùng: {e}")
            return None, None

    def get_account_info(self, account_id):
        try:
            cursor = self.db_connection.cursor()
            query = """
            SELECT a.id_account, a.username, a.password, a.role, a.id_emp, a.id_ad,
                   COALESCE(e.fullname, ad.fullname, '') as fullname,
                   COALESCE(e.phone, ad.phone, '') as phone,
                   COALESCE(e.email, ad.email, '') as email,
                   COALESCE(e.address, ad.address, '') as address
            FROM dbo.Accounts a
            LEFT JOIN dbo.Employees e ON a.id_emp = e.id_emp
            LEFT JOIN dbo.Admin ad ON a.id_ad = ad.id_ad
            WHERE a.id_account = ?
            """
            cursor.execute(query, (account_id,))
            result = cursor.fetchone()
            print(f"get_account_info result: {result}")

            if result:
                return {
                    'id_account': result[0],
                    'username': result[1],
                    'password': result[2],
                    'role': result[3],
                    'id_emp': result[4],
                    'id_ad': result[5],
                    'fullname': result[6],
                    'phone': result[7],
                    'email': result[8],
                    'address': result[9],
                }
            return None
        except Exception as e:
            print(f"Lỗi khi lấy thông tin tài khoản: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()

    def update_user_data(self, account_id, hoten, phonenum, email, addr, username, password):
        """
        Cập nhật thông tin tài khoản và thông tin người dùng (Employees hoặc Admin)

        Args:
            account_id: ID của tài khoản
            hoten: Họ tên
            phonenum: Số điện thoại
            email: Email
            addr: Địa chỉ
            username: Tên đăng nhập
            password: Mật khẩu

        Returns:
            bool: True nếu thành công, False nếu thất bại
        """
        try:
            cursor = self.db_connection.cursor()

            # Update the Accounts table with username and password
            query_account = """
                UPDATE dbo.Accounts
                SET username = ?, password = ?
                WHERE id_account = ?
            """
            cursor.execute(query_account, (username, password, account_id))

            # Get the associated id_emp or id_ad to determine which table to update
            id_emp, id_ad = self.get_user_id(account_id)
            if id_emp is None and id_ad is None:
                print(f"No associated user found for account_id: {account_id}")
                return False

            # Update either Employees or Admin table based on id_emp or id_ad
            if id_emp:
                query_user = """
                    UPDATE dbo.Employees
                    SET fullname = ?, phone = ?, email = ?, address = ?
                    WHERE id_emp = ?
                """
                cursor.execute(query_user, (hoten, phonenum, email, addr, id_emp))
            elif id_ad:
                query_user = """
                    UPDATE dbo.Admin
                    SET fullname = ?, phone = ?, email = ?, address = ?
                    WHERE id_ad = ?
                """
                cursor.execute(query_user, (hoten, phonenum, email, addr, id_ad))

            # Commit the transaction
            self.db_connection.commit()
            print("User data updated successfully")
            return True

        except Exception as e:
            print(f"Lỗi khi cập nhật dữ liệu người dùng: {e}")
            # Rollback the transaction in case of an error
            self.db_connection.rollback()
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()