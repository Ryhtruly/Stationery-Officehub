# app/database/models/import_detail.py

class ChiTietNhapHang:
    """
    Model đại diện cho bảng dbo.Import_detail trong cơ sở dữ liệu
    """

    def __init__(self, id_imp=None, id_prod=None, quantity=0, price=0):
        self.id_imp = id_imp
        self.id_prod = id_prod
        self.quantity = quantity
        self.price = price

    @classmethod
    def from_dict(cls, data):
        """
        Tạo đối tượng ChiTietNhapHang từ dictionary
        """
        return cls(
            id_imp=data.get('id_imp'),
            id_prod=data.get('id_prod'),
            quantity=data.get('quantity', 0),
            price=data.get('price', 0)
        )

    def to_dict(self):
        """
        Chuyển đối tượng thành dictionary
        """
        return {
            'id_imp': self.id_imp,
            'id_prod': self.id_prod,
            'quantity': self.quantity,
            'price': self.price
        }
