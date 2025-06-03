# app/database/models/admin.py

class Admin:
    """
    Model đại diện cho bảng dbo.Admin
    """

    def __init__(self, id_ad=None, fullname=None, address=None, phone=None, email=None):
        """
        Khởi tạo đối tượng Admin

        Args:
            id_ad (int): ID của admin
            fullname (str): Họ tên đầy đủ của admin
            address (str): Địa chỉ của admin
            phone (str): Số điện thoại của admin
            email (str): Địa chỉ email của admin
        """
        self.id_ad = id_ad
        self.fullname = fullname
        self.address = address
        self.phone = phone
        self.email = email

    def __str__(self):
        """
        Trả về chuỗi biểu diễn của đối tượng Admin
        """
        return f"Admin(id_ad={self.id_ad}, fullname='{self.fullname}', email='{self.email}')"
