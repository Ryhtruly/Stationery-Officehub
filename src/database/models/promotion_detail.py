
class PromotionDetail:
    def __init__(self, id_prom=None, id_category=None, percent_discount=0.0):
        """
        Khởi tạo đối tượng PromotionDetail

        Args:
            id_prom (int): ID của chương trình khuyến mãi
            id_category (int): ID của danh mục sản phẩm
            percent_discount (float): Phần trăm giảm giá
        """
        self.id_prom = id_prom
        self.id_category = id_category
        self.percent_discount = percent_discount

    def __str__(self):

        return f"PromotionDetail(id_prom={self.id_prom}, id_category={self.id_category}, percent_discount={self.percent_discount})"
