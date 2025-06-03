
from src.database.DAO.employee.ProductEmployeeDAO import ProductDAO

class ProductData:
    def __init__(self):
        self.products = []
        self.load_products_from_db()

    def load_products_from_db(self):
        try:
            db_products = ProductDAO.get_all_products()
            if db_products and len(db_products) > 0:
                print(f"Đã tải {len(db_products)} sản phẩm từ database")
                # Kiểm tra và làm sạch dữ liệu
                self.products = [
                    product for product in db_products
                    if all(key in product for key in ["id", "ten", "gia", "display_price", "mo_ta", "hinh_anh", "id_category", "category_name"])
                    and product["id"] is not None
                    and product["ten"] is not None
                ]
            else:
                print("Không có dữ liệu sản phẩm từ database, sử dụng dữ liệu mẫu")
                self._load_sample_data()
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu sản phẩm từ database: {str(e)}")
            self._load_sample_data()

    def _load_sample_data(self):
        print("Đang tải dữ liệu sản phẩm mẫu...")
        self.products = [
            {"id": "SP001", "ten": "Sổ tay mini", "gia": 10000, "display_price": 10000, "hinh_anh": "", "mo_ta": "Sổ tay mini tiện lợi", "id_category": 1, "category_name": "Văn phòng phẩm"},
            {"id": "SP002", "ten": "Giấy vẽ", "gia": 20000, "display_price": 20000, "hinh_anh": "", "mo_ta": "Giấy vẽ chất lượng cao", "id_category": 1, "category_name": "Văn phòng phẩm"},
            {"id": "SP003", "ten": "Bút viết", "gia": 20000, "display_price": 20000, "hinh_anh": "", "mo_ta": "Bút viết mực gel", "id_category": 1, "category_name": "Văn phòng phẩm"},
            {"id": "SP004", "ten": "Kẹp vở", "gia": 10000, "display_price": 10000, "hinh_anh": "", "mo_ta": "Kẹp vở chắc chắn", "id_category": 1, "category_name": "Văn phòng phẩm"},
            {"id": "SP005", "ten": "Máy cưa", "gia": 10000, "display_price": 10000, "hinh_anh": "", "mo_ta": "Máy cưa mini", "id_category": 2, "category_name": "Công cụ"},
            {"id": "SP006", "ten": "Optimus", "gia": 10000, "display_price": 10000, "hinh_anh": "", "mo_ta": "Bút Optimus cao cấp", "id_category": 1, "category_name": "Văn phòng phẩm"},
        ]
        print(f"Đã tải {len(self.products)} sản phẩm mẫu")

    def get_all_products(self):
        return self.products

    def get_product_by_id(self, product_id):
        try:
            product = ProductDAO.get_product_by_id(product_id)
            if product and all(key in product for key in ["id", "ten", "gia", "display_price", "mo_ta", "hinh_anh", "id_category", "category_name"]):
                return product
        except Exception as e:
            print(f"Lỗi khi lấy sản phẩm từ database: {str(e)}")
        for product in self.products:
            if product["id"] == product_id:
                return product
        return None

    def search_products(self, keyword):
        try:
            if not keyword:
                return self.products

            keyword = str(keyword).lower().strip()
            results = []
            for product in self.products:
                try:
                    id_str = str(product.get("id", "")).lower()
                    ten = str(product.get("ten", "")).lower()
                    mo_ta = str(product.get("mo_ta", "")).lower()
                    category_name = str(product.get("category_name", "")).lower()
                    if keyword in id_str or keyword in ten or keyword in mo_ta or keyword in category_name:
                        results.append(product)
                except Exception as e:
                    print(f"Lỗi khi xử lý sản phẩm ID {product.get('id', 'N/A')}: {str(e)}")
                    continue

            print(f"Tìm thấy {len(results)} sản phẩm khớp với từ khóa '{keyword}'")
            return results
        except Exception as e:
            print(f"Lỗi trong phương thức search_products: {str(e)}")
            return []

    def filter_by_category(self, category_id):
        try:
            if category_id is None:
                return self.products

            category_id = int(category_id)  # Chuyển đổi thành int
            filtered_products = [
                product for product in self.products
                if product.get("id_category") == category_id
            ]
            print(f"Đã lọc {len(filtered_products)} sản phẩm thuộc danh mục ID {category_id}")
            return filtered_products
        except ValueError:
            print(f"Invalid category ID format: {category_id}")
            return []
        except Exception as e:
            print(f"Lỗi khi lọc sản phẩm theo danh mục: {str(e)}")
            return []

    def reload_data(self):
        self.load_products_from_db()
        return self.products