
class ChiTietHoaDon:
    """
    Model đại diện cho bảng dbo.Bill_detail trong cơ sở dữ liệu
    """

    def __init__(self, id_bill=None, id_prod=None, quantity=0, price=0, discount=0):
        self.id_bill = id_bill
        self.id_prod = id_prod
        self.quantity = quantity
        self.price = price
        self.discount = discount

    @classmethod
    def from_dict(cls, data):
        """
        Tạo đối tượng ChiTietHoaDon từ dictionary
        """
        return cls(
            id_bill=data.get('id_bill'),
            id_prod=data.get('id_prod'),
            quantity=data.get('quantity', 0),
            price=data.get('price', 0),
            discount=data.get('discount', 0)
        )

    def to_dict(self):
        """
        Chuyển đối tượng thành dictionary
        """
        return {
            'id_bill': self.id_bill,
            'id_prod': self.id_prod,
            'quantity': self.quantity,
            'price': self.price,
            'discount': self.discount
        }
