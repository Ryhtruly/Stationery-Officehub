def create_trigger_update_product_import_price(cursor):
    try:
        # Xóa trigger cũ nếu tồn tại
        drop_sql = "IF EXISTS (SELECT * FROM sys.triggers WHERE name = 'trg_UpdateProductImportPrice') DROP TRIGGER trg_UpdateProductImportPrice"
        cursor.execute(drop_sql)

        # Tạo trigger mới
        create_sql = """
        CREATE TRIGGER trg_UpdateProductImportPrice
        ON dbo.Import_detail
        AFTER INSERT
        AS
        BEGIN
            SET NOCOUNT ON;

            -- Cập nhật giá nhập mới nhất cho sản phẩm
            UPDATE p
            SET price_import = i.price
            FROM dbo.Products p
            INNER JOIN inserted i ON p.id_prod = i.id_prod;
        END
        """
        cursor.execute(create_sql)
        print("Đã tạo trigger trg_UpdateProductImportPrice thành công")
        return True
    except Exception as e:
        print(f"Lỗi khi tạo trigger trg_UpdateProductImportPrice: {str(e)}")
        return False
