class Warehouse:
    """
    Lớp đại diện cho kho hàng
    """

    def __init__(self, id_warehouse, name, address, phone):
        """
        Khởi tạo đối tượng kho hàng

        Args:
            id_warehouse: ID kho hàng
            name: Tên kho
            address: Địa chỉ kho
            phone: Số điện thoại liên hệ
        """
        self.id_warehouse = id_warehouse
        self.name = name
        self.address = address
        self.phone = phone


class WarehouseProduct:
    """
    Lớp đại diện cho sản phẩm trong kho
    """

    def __init__(self, id_warehouse, id_prod, name, inventory):
        """
        Khởi tạo đối tượng sản phẩm trong kho

        Args:
            id_warehouse: ID kho hàng
            id_prod: ID sản phẩm
            name: Tên sản phẩm
            inventory: Số lượng tồn kho
        """
        self.id_warehouse = id_warehouse
        self.id_prod = id_prod
        self.name = name
        self.inventory = inventory
