# app/database/models/bill.py
from datetime import datetime


class HoaDon:
    """
    Model đại diện cho bảng dbo.Bill trong cơ sở dữ liệu
    """

    def __init__(self, id_bill=None, id_cust=None, id_emp=None, total=0, date=None):
        self.id_bill = id_bill
        self.id_cust = id_cust
        self.id_emp = id_emp
        self.total = total
        self.date = date if date else datetime.now()

    @classmethod
    def from_dict(cls, data):
        """
        Tạo đối tượng HoaDon từ dictionary
        """
        return cls(
            id_bill=data.get('id_bill'),
            id_cust=data.get('id_cust'),
            id_emp=data.get('id_emp'),
            total=data.get('total', 0),
            date=data.get('date')
        )

    def to_dict(self):
        """
        Chuyển đối tượng thành dictionary
        """
        return {
            'id_bill': self.id_bill,
            'id_cust': self.id_cust,
            'id_emp': self.id_emp,
            'total': self.total,
            'date': self.date
        }
