class AccountDetailData:
    def __init__(self, account_detail_dao):
        self.account_detail_dao = account_detail_dao
        self.current_account_id = None

    def load_user_data(self, account_id, hoten_line, phonenum_line, email_line, addr_line, chucvu_line, username_line, password_line):
        try:
            print(f"Loading user data for account_id: {account_id}")

            if account_id is None:
                print("account_id is None, cannot load user data")
                return False

            self.current_account_id = account_id
            account_info = self.account_detail_dao.get_account_info(account_id)

            if not account_info:
                print(f"Không tìm thấy thông tin cho account_id: {account_id}")
                return False

            print(f"Account info loaded: {account_info}")

            # Gán dữ liệu vào các trường giao diện
            hoten_line.setText(account_info.get('fullname', ""))
            phonenum_line.setText(account_info.get('phone', ""))
            email_line.setText(account_info.get('email', ""))
            addr_line.setText(account_info.get('address', ""))
            chucvu_line.setText(account_info.get('role', ""))
            username_line.setText(account_info.get('username', ""))
            password_line.setText(account_info.get('password', ""))

            fields = [
                hoten_line,
                phonenum_line,
                email_line,
                addr_line,
                chucvu_line,
                username_line,
                password_line
            ]

            for field in fields:
                field.setReadOnly(True)

            print("Data set to UI fields successfully")
            return True
        except Exception as e:
            print(f"Lỗi khi load dữ liệu người dùng: {e}")
            return False

    def update_user_data(self, hoten_line, phonenum_line, email_line, addr_line, username_line, password_line):
        try:
            if not self.current_account_id:
                print("current_account_id is None, cannot update user data")
                return False

            # Get the text from the QLineEdit widgets
            hoten = hoten_line.text().strip()
            phonenum = phonenum_line.text().strip()
            email = email_line.text().strip()
            addr = addr_line.text().strip()
            username = username_line.text().strip()
            password = password_line.text().strip()

            # Validate the inputs (optional, but recommended)
            if not all([hoten, phonenum, email, addr, username, password]):
                print("One or more fields are empty, update aborted")
                return False

            # Gọi AccountDetailDAO để cập nhật dữ liệu
            success = self.account_detail_dao.update_user_data(
                self.current_account_id, hoten, phonenum, email, addr, username, password
            )

            if success:
                print("User data updated successfully via DAO")
                return True
            else:
                print("Failed to update user data via DAO")
                return False

        except Exception as e:
            print(f"Lỗi khi cập nhật dữ liệu người dùng: {e}")
            return False