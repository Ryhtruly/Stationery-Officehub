# app/database/models/card.py

class TheThanhVien:
    """
    Model đại diện cho bảng dbo.Card trong cơ sở dữ liệu
    """

    def __init__(self, rank=None, discount=None):
        self.rank = rank
        self.discount = discount

    @classmethod
    def from_dict(cls, data):
        """
        Tạo đối tượng TheThanhVien từ dictionary
        """
        return cls(
            rank=data.get('rank'),
            discount=data.get('discount')
        )

    def to_dict(self):
        """
        Chuyển đối tượng thành dictionary
        """
        return {
            'rank': self.rank,
            'discount': self.discount
        }
