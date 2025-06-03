# app/database/models/customer.py

class KhachHang:
    """
    Model đại diện cho khách hàng
    """

    def __init__(self, id_cust=None, fullname=None, phone=None, rank=None, register_date=None):
        self.id_cust = id_cust
        self.fullname = fullname
        self.phone = phone
        self.rank = rank
        self.register_date = register_date

    def __str__(self):
        return f"KhachHang(id={self.id_cust}, name={self.fullname}, phone={self.phone})"
