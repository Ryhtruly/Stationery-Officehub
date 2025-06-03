class CartData:
    def __init__(self):
        self.items = []
        self.total_price = 0
        self.cart_updated_callback = None

    def add_item(self, product_id, product_name, price, quantity=1):
        for item in self.items:
            if item["id"] == product_id:
                item["so_luong"] += quantity
                self._update_total_price()
                if self.cart_updated_callback:
                    self.cart_updated_callback()
                return

        new_item = {
            "id": product_id,
            "ten": product_name,
            "gia": price,
            "so_luong": quantity
        }
        self.items.append(new_item)
        self._update_total_price()

        if self.cart_updated_callback:
            self.cart_updated_callback()

    def update_quantity(self, product_id, quantity):
        """Cập nhật số lượng sản phẩm trong giỏ hàng"""
        if quantity <= 0:
            self.remove_item(product_id)
            return

        for item in self.items:
            if item["id"] == product_id:
                item["so_luong"] = quantity
                self._update_total_price()
                if self.cart_updated_callback:
                    self.cart_updated_callback()
                return

    def remove_item(self, product_id):
        """Xóa sản phẩm khỏi giỏ hàng"""
        self.items = [item for item in self.items if item["id"] != product_id]
        self._update_total_price()
        if self.cart_updated_callback:
            self.cart_updated_callback()

    def clear_cart(self):
        """Xóa toàn bộ giỏ hàng"""
        self.items = []
        self.total_price = 0
        if self.cart_updated_callback:
            self.cart_updated_callback()

    def _update_total_price(self):
        """Cập nhật tổng giá trị giỏ hàng"""
        self.total_price = sum(item["gia"] * item["so_luong"] for item in self.items)

    def set_cart_updated_callback(self, callback):
        """Đặt callback khi giỏ hàng thay đổi"""
        self.cart_updated_callback = callback

    def increase_quantity(self, item_id):
        for item in self.items:
            if item['id'] == item_id:
                item['quantity'] += 1
                break

    def decrease_quantity(self, item_id):
        for item in self.items:
            if item['id'] == item_id:
                if item['quantity'] > 1:
                    item['quantity'] -= 1
                else:
                    self.remove_item(item_id)
                break

