class NhanVien:
    """
    Đối tượng Nhân viên
    """

    def __init__(self, id_emp=None, fullname=None, address=None, phone=None, salary=None, email=None, status=1):
        self.id_emp = id_emp
        self.fullname = fullname
        self.address = address
        self.phone = phone
        self.salary = salary
        self.email = email
        self.status = status

    def __str__(self):
        return f"NhanVien(id_emp={self.id_emp}, fullname={self.fullname})"
