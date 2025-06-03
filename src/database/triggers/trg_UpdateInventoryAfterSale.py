def create_trigger_update_inventory_after_sale(cursor):
    try:
        # Xóa trigger cũ nếu tồn tại
        drop_sql = "IF EXISTS (SELECT * FROM sys.triggers WHERE name = 'trg_UpdateInventoryAfterSale') DROP TRIGGER trg_UpdateInventoryAfterSale"
        cursor.execute(drop_sql)

        # Tạo trigger mới
        create_sql = """
        CREATE TRIGGER trg_UpdateInventoryAfterSale
        ON dbo.Bill_detail
        AFTER INSERT
        AS
        BEGIN
            SET NOCOUNT ON;

            -- Tạo bảng tạm để lưu số lượng cần trừ cho từng sản phẩm
            DECLARE @RemainingQuantities TABLE (
                id_prod INT,
                quantity INT
            );

            -- Khởi tạo số lượng cần trừ cho từng sản phẩm
            INSERT INTO @RemainingQuantities (id_prod, quantity)
            SELECT id_prod, quantity FROM inserted;

            -- Xử lý từng kho theo thứ tự id_warehouse
            DECLARE @CurrentWarehouse INT;

            -- Lặp qua các kho theo thứ tự
            DECLARE warehouse_cursor CURSOR FOR 
            SELECT id_warehouse FROM dbo.Warehouse ORDER BY id_warehouse;

            OPEN warehouse_cursor;
            FETCH NEXT FROM warehouse_cursor INTO @CurrentWarehouse;

            WHILE @@FETCH_STATUS = 0 AND EXISTS (SELECT 1 FROM @RemainingQuantities WHERE quantity > 0)
            BEGIN
                -- Cập nhật tồn kho từ kho hiện tại và số lượng còn lại
                UPDATE wp
                SET wp.inventory = CASE 
                    WHEN wp.inventory >= rq.quantity THEN wp.inventory - rq.quantity
                    ELSE 0
                END
                FROM dbo.Warehouse_Product wp
                INNER JOIN @RemainingQuantities rq ON wp.id_prod = rq.id_prod
                WHERE wp.id_warehouse = @CurrentWarehouse
                AND rq.quantity > 0;

                -- Cập nhật số lượng còn lại cần trừ
                UPDATE rq
                SET quantity = CASE 
                    WHEN wp.inventory >= rq.quantity THEN 0
                    ELSE rq.quantity - wp.inventory
                END
                FROM @RemainingQuantities rq
                INNER JOIN dbo.Warehouse_Product wp ON rq.id_prod = wp.id_prod
                WHERE wp.id_warehouse = @CurrentWarehouse
                AND rq.quantity > 0;

                FETCH NEXT FROM warehouse_cursor INTO @CurrentWarehouse;
            END

            CLOSE warehouse_cursor;
            DEALLOCATE warehouse_cursor;
        END
        """
        cursor.execute(create_sql)
        print("Đã tạo trigger trg_UpdateInventoryAfterSale thành công")
        return True
    except Exception as e:
        print(f"Lỗi khi tạo trigger trg_UpdateInventoryAfterSale: {str(e)}")
        return False
