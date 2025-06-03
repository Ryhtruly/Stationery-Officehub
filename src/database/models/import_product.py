# app/database/models/import_product.py
from datetime import datetime


class NhapHang:
    """
    Model đại diện cho bảng dbo.Import trong cơ sở dữ liệu
    """

    def __init__(self, id_imp=None, id_emp=None, date=None, total_price=None, employee_name=None):
        self.id_imp = id_imp
        self.id_emp = id_emp
        self.date = date
        self.total_price = total_price
        self.employee_name = employee_name

    @classmethod
    def from_dict(cls, data):
        """
        Tạo đối tượng NhapHang từ dictionary
        """
        return cls(
            id_imp=data.get('id_imp'),
            id_emp=data.get('id_emp'),
            date=data.get('date')
        )

    def to_dict(self):
        """
        Chuyển đối tượng thành dictionary
        """
        return {
            'id_imp': self.id_imp,
            'id_emp': self.id_emp,
            'date': self.date
        }
