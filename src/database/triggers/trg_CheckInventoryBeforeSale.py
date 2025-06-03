def create_trigger_check_inventory_before_sale(cursor):
    try:
        # Xóa trigger cũ nếu tồn tại
        drop_sql = "IF EXISTS (SELECT * FROM sys.triggers WHERE name = 'trg_CheckInventoryBeforeSale') DROP TRIGGER trg_CheckInventoryBeforeSale"
        cursor.execute(drop_sql)

        # Tạo trigger mới
        create_sql = """
        CREATE TRIGGER trg_CheckInventoryBeforeSale
        ON dbo.Bill_detail
        INSTEAD OF INSERT
        AS
        BEGIN
            SET NOCOUNT ON;

            -- Kiểm tra tổng tồn kho trên tất cả các kho
            IF EXISTS (
                SELECT 1
                FROM inserted i
                WHERE i.quantity > (
                    SELECT ISNULL(SUM(wp.inventory), 0)
                    FROM dbo.Warehouse_Product wp 
                    WHERE wp.id_prod = i.id_prod
                )
            )
            BEGIN
                RAISERROR('Số lượng sản phẩm bán vượt quá tổng tồn kho hiện có', 16, 1);
                RETURN;
            END

            -- Nếu đủ tồn kho, thực hiện thêm chi tiết hóa đơn
            INSERT INTO dbo.Bill_detail (id_bill, id_prod, quantity, price, discount)
            SELECT id_bill, id_prod, quantity, price, discount
            FROM inserted;
        END
        """
        cursor.execute(create_sql)
        print("Đã tạo trigger trg_CheckInventoryBeforeSale thành công")
        return True
    except Exception as e:
        print(f"Lỗi khi tạo trigger trg_CheckInventoryBeforeSale: {str(e)}")
        return False
