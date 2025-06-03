
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from src.modules.employee.data.product_data import ProductData
from src.modules.employee.view.product_view import ProductItemView


class ProductEvents:
    def __init__(self, product_view):
        self.product_view = product_view
        self.product_data = ProductData()

        self.load_products()

    def load_products(self):
        """
        Tải tất cả sản phẩm lên giao diện
        """
        # Xóa sản phẩm hiện tại
        self.product_view.clear_products()

        # Lấy tất cả sản phẩm
        products = self.product_data.get_all_products()

        for product in products:
            self.product_view.add_product_item(
                product["id"],
                product["ten"],
                product["gia"],
                product.get("mo_ta", ""),
                product.get("hinh_anh", "")
            )

    def reload_data(self):
        """
        Tải lại dữ liệu từ database
        """
        self.product_data.load_products_from_db()
        self.load_products()

    def sort_products_by_name(self, ascending=True):
        """Sắp xếp sản phẩm theo tên"""
        try:
            # Lấy tất cả sản phẩm từ database
            products = self.product_data.get_all_products()

            # Sắp xếp theo tên
            sorted_products = sorted(
                products,
                key=lambda x: x["ten"].lower(),  # Chuyển về chữ thường để sắp xếp không phân biệt hoa thường
                reverse=not ascending
            )

            # Xóa sản phẩm hiện tại
            self.product_view.clear_products()

            # Thêm sản phẩm đã sắp xếp vào giao diện
            for product in sorted_products:
                self.product_view.add_product_item(
                    product["id"],
                    product["ten"],
                    product["gia"],
                    product.get("mo_ta", ""),
                    product.get("hinh_anh", "")
                )
        except Exception as e:
            print(f"Lỗi khi sắp xếp theo tên: {str(e)}")

    def sort_products_by_price(self, ascending=True):
        """Sắp xếp sản phẩm theo giá"""
        try:
            # Lấy tất cả sản phẩm từ database
            products = self.product_data.get_all_products()

            # Sắp xếp theo giá
            sorted_products = sorted(
                products,
                key=lambda x: float(x["gia"]) if isinstance(x["gia"], str) else x["gia"],
                reverse=not ascending
            )

            # Xóa sản phẩm hiện tại
            self.product_view.clear_products()

            # Thêm sản phẩm đã sắp xếp vào giao diện
            for product in sorted_products:
                self.product_view.add_product_item(
                    product["id"],
                    product["ten"],
                    product["gia"],
                    product.get("mo_ta", ""),
                    product.get("hinh_anh", "")
                )
        except Exception as e:
            print(f"Lỗi khi sắp xếp theo giá: {str(e)}")

    def search_products(self, keyword):
        """Tìm kiếm sản phẩm theo từ khóa"""
        try:
            # Nếu từ khóa trống, hiển thị tất cả sản phẩm
            if not keyword:
                self.load_products()
                return

            # Lấy tất cả sản phẩm từ database
            all_products = self.product_data.get_all_products()

            # Chuyển từ khóa về chữ thường
            keyword = keyword.lower()

            # Lọc sản phẩm theo từ khóa
            filtered_products = [
                product for product in all_products
                if keyword in product["ten"].lower() or
                   (product.get("mo_ta") and keyword in product["mo_ta"].lower())
            ]

            # Xóa sản phẩm hiện tại
            self.product_view.clear_products()

            # Thêm sản phẩm đã lọc vào giao diện
            if filtered_products:
                for product in filtered_products:
                    self.product_view.add_product_item(
                        product["id"],
                        product["ten"],
                        product["gia"],
                        product.get("mo_ta", ""),
                        product.get("hinh_anh", "")
                    )
            else:
                # Hiển thị thông báo không tìm thấy sản phẩm
                self.product_view.show_no_results_message()
        except Exception as e:
            print(f"Lỗi khi tìm kiếm sản phẩm: {str(e)}")

