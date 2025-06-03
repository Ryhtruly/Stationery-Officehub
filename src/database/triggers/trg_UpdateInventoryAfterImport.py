def create_trigger_update_inventory_after_import(cursor):
    try:
        # Xóa trigger cũ nếu tồn tại
        drop_sql = "IF EXISTS (SELECT * FROM sys.triggers WHERE name = 'trg_UpdateInventoryAfterImport') DROP TRIGGER trg_UpdateInventoryAfterImport"
        cursor.execute(drop_sql)

        # Tạo trigger mới
        create_sql = """
        CREATE TRIGGER trg_UpdateInventoryAfterImport
        ON dbo.Import_detail
        AFTER INSERT
        AS
        BEGIN
            SET NOCOUNT ON;

            -- Cập nhật tồn kho sau khi nhập hàng
            -- Chỉ cập nhật tồn kho ở kho đầu tiên (hoặc kho mặc định)
            UPDATE wp
            SET inventory = wp.inventory + i.quantity
            FROM dbo.Warehouse_Product wp
            INNER JOIN inserted i ON wp.id_prod = i.id_prod
            INNER JOIN dbo.Import imp ON i.id_imp = imp.id_imp
            INNER JOIN dbo.Products p ON i.id_prod = p.id_prod
            WHERE wp.id_warehouse = (SELECT TOP 1 id_warehouse FROM dbo.Warehouse ORDER BY id_warehouse);

            -- Nếu sản phẩm chưa có trong kho đầu tiên, thêm mới
            INSERT INTO dbo.Warehouse_Product (id_warehouse, id_prod, inventory)
            SELECT 
                (SELECT TOP 1 id_warehouse FROM dbo.Warehouse ORDER BY id_warehouse),
                i.id_prod,
                i.quantity
            FROM inserted i
            WHERE NOT EXISTS (
                SELECT 1 FROM dbo.Warehouse_Product wp 
                WHERE wp.id_prod = i.id_prod 
                AND wp.id_warehouse = (SELECT TOP 1 id_warehouse FROM dbo.Warehouse ORDER BY id_warehouse)
            );
        END
        """
        cursor.execute(create_sql)
        print("Đã tạo trigger trg_UpdateInventoryAfterImport thành công")
        return True
    except Exception as e:
        print(f"Lỗi khi tạo trigger trg_UpdateInventoryAfterImport: {str(e)}")
        return False
