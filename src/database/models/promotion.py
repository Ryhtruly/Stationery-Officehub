# promotion.py

from datetime import datetime

class Promotion:
    """
    Model đại diện cho bảng dbo.Promotion
    """

    def __init__(self, id_prom=None, start_date=None, end_date=None, name=None):
        """
        Khởi tạo đối tượng Promotion

        Args:
            id_prom (int): ID của chương trình khuyến mãi
            start_date (datetime): Ngày bắt đầu khuyến mãi
            end_date (datetime): Ngày kết thúc khuyến mãi
        """
        self.id_prom = id_prom
        self.start_date = start_date if start_date else datetime.now()
        self.end_date = end_date if end_date else datetime.now()
        self.name = name

    def __str__(self):
        """
        Trả về chuỗi biểu diễn của đối tượng Promotion
        """
        return f"Promotion(id_prom={self.id_prom}, start_date={self.start_date}, end_date={self.end_date})"
