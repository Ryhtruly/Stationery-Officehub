import datetime


class Account:
    """
    Đối tượng tài khoản người dùng
    """

    def __init__(self, id_account=None, username=None, password=None, id_emp=None, id_ad=None,
                 role=None, is_active=None, created_at=None):
        self.id_account = id_account
        self.username = username
        self.password = password
        self.id_emp = id_emp
        self.id_ad = id_ad
        self.role = role
        self.is_active = is_active
        self.created_at = created_at if created_at else datetime.datetime.now()

    def __str__(self):
        return f"Account(id_account={self.id_account}, username={self.username}, role={self.role})"
