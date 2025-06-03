def create_trigger_restore_price_on_promotion_delete(cursor):
    try:
        # Xóa trigger cũ nếu tồn tại
        drop_sql = "IF EXISTS (SELECT * FROM sys.triggers WHERE name = 'trg_RestorePriceOnPromotionDelete') DROP TRIGGER trg_RestorePriceOnPromotionDelete"
        cursor.execute(drop_sql)

        # Tạo trigger mới
        create_sql = """
        CREATE TRIGGER trg_RestorePriceOnPromotionDelete
        ON dbo.Promotion_detail
        AFTER DELETE
        AS
        BEGIN
            SET NOCOUNT ON;

            -- Lấy danh sách các danh mục từ bản ghi vừa xóa
            DECLARE @id_category INT;

            DECLARE deleted_cursor CURSOR FOR
            SELECT d.id_category
            FROM deleted d;

            OPEN deleted_cursor;
            FETCH NEXT FROM deleted_cursor INTO @id_category;

            WHILE @@FETCH_STATUS = 0
            BEGIN
                -- Đặt promotion_price về NULL cho các sản phẩm thuộc danh mục này
                UPDATE p
                SET promotion_price = NULL
                FROM dbo.Products p
                WHERE p.id_category = @id_category;

                FETCH NEXT FROM deleted_cursor INTO @id_category;
            END;

            CLOSE deleted_cursor;
            DEALLOCATE deleted_cursor;
        END
        """
        cursor.execute(create_sql)
        print("Đã tạo trigger trg_RestorePriceOnPromotionDelete thành công")
        return True
    except Exception as e:
        print(f"Lỗi khi tạo trigger trg_RestorePriceOnPromotionDelete: {str(e)}")
        return False