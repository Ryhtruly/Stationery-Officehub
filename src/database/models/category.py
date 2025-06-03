# app/database/models/category.py

class DanhMuc:
    """
    Lớp đại diện cho đối tượng Danh mục
    """

    def __init__(self, id_category, name, description=""):
        """
        Khởi tạo đối tượng Danh mục

        Args:
            id_category: ID của danh mục
            name: Tên danh mục
            description: Mô tả danh mục (mặc định là chuỗi rỗng vì bảng không có cột này)
        """
        self.id_category = id_category
        self.name = name
        self.description = description

    def __str__(self):
        """
        Chuyển đối tượng thành chuỗi

        Returns:
            str: Chuỗi đại diện cho đối tượng
        """
        return f"DanhMuc(id_category={self.id_category}, name={self.name})"

    @classmethod
    def from_dict(cls, data):
        """
        Tạo đối tượng DanhMuc từ dictionary
        """
        return cls(
            id_category=data.get('id_category'),
            name=data.get('name')
        )

    def to_dict(self):
        """
        Chuyển đối tượng thành dictionary
        """
        return {
            'id_category': self.id_category,
            'name': self.name
        }
