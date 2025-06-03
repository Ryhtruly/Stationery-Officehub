def create_trigger_default_product_values(cursor):
    try:
        # Xóa trigger cũ nếu tồn tại
        drop_sql = "IF EXISTS (SELECT * FROM sys.triggers WHERE name = 'trg_DefaultProductValues') DROP TRIGGER trg_DefaultProductValues"
        cursor.execute(drop_sql)

        # Tạo trigger mới
        create_sql = """
        CREATE TRIGGER trg_DefaultProductValues
        ON dbo.Products
        AFTER INSERT
        AS
        BEGIN
            SET NOCOUNT ON;

            UPDATE p
            SET 
                price_import = CASE WHEN i.price_import IS NULL THEN 0 ELSE i.price_import END,
                price = CASE WHEN i.price IS NULL THEN 0 ELSE i.price END,
                unit = CASE WHEN i.unit IS NULL THEN 'Cái' ELSE i.unit END
            FROM dbo.Products p
            INNER JOIN inserted i ON p.id_prod = i.id_prod;
        END
        """
        cursor.execute(create_sql)
        print("Đã tạo trigger trg_DefaultProductValues thành công")
        return True
    except Exception as e:
        print(f"Lỗi khi tạo trigger trg_DefaultProductValues: {str(e)}")
        return False
