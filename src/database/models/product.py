# app/database/models/product.py

class SanPham:
    """
    Model đại diện cho bảng dbo.Products trong cơ sở dữ liệu
    """

    def __init__(self, id_prod=None, name=None, unit=None, price=0,
                 promotion_price=None, description=None, id_category=None,
                 price_import=0, image_url=None, id_warehouse=None):
        self.id_prod = id_prod
        self.name = name
        self.unit = unit
        self.price = price
        self.promotion_price = promotion_price
        self.display_price = promotion_price if promotion_price is not None else price  # Giá hiển thị
        self.description = description
        self.id_category = id_category
        self.price_import = price_import
        self.image_url = image_url
        self.id_warehouse = id_warehouse

    @classmethod
    def from_dict(cls, data):
        """
        Tạo đối tượng SanPham từ dictionary
        """
        return cls(
            id_prod=data.get('id_prod'),
            name=data.get('name'),
            unit=data.get('unit'),
            price=data.get('price', 0),
            promotion_price=data.get('promotion_price'),
            description=data.get('description'),
            id_category=data.get('id_category'),
            price_import=data.get('price_import', 0),
            image_url=data.get('image_url'),
            id_warehouse=data.get('id_warehouse')
        )

    def to_dict(self):
        """
        Chuyển đối tượng thành dictionary
        """
        return {
            'id_prod': self.id_prod,
            'name': self.name,
            'unit': self.unit,
            'price': self.price,
            'promotion_price': self.promotion_price,
            'display_price': self.display_price,
            'description': self.description,
            'id_category': self.id_category,
            'price_import': self.price_import,
            'image_url': self.image_url,
            'id_warehouse': self.id_warehouse
        }