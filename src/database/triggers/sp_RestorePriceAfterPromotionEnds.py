def create_sp_restore_price_after_promotion_ends(cursor):
    try:
        # Xóa stored procedure cũ nếu tồn tại
        drop_sql = "IF EXISTS (SELECT * FROM sys.procedures WHERE name = 'sp_RestorePriceAfterPromotionEnds') DROP PROCEDURE sp_RestorePriceAfterPromotionEnds"
        cursor.execute(drop_sql)

        # Tạo stored procedure mới
        create_sql = """
        CREATE PROCEDURE sp_RestorePriceAfterPromotionEnds
        AS
        BEGIN
            SET NOCOUNT ON;

            -- Tìm các chương trình khuyến mãi đã hết hạn
            DECLARE @id_prom INT, @id_category INT;

            DECLARE expired_prom_cursor CURSOR FOR
            SELECT pd.id_prom, pd.id_category
            FROM dbo.Promotion_detail pd
            JOIN dbo.Promotion p ON pd.id_prom = p.id_prom
            WHERE p.end_date < GETDATE();

            OPEN expired_prom_cursor;
            FETCH NEXT FROM expired_prom_cursor INTO @id_prom, @id_category;

            WHILE @@FETCH_STATUS = 0
            BEGIN
                -- Đặt promotion_price về NULL cho các sản phẩm thuộc danh mục này
                UPDATE p
                SET promotion_price = NULL
                FROM dbo.Products p
                WHERE p.id_category = @id_category;

                -- Xóa chi tiết khuyến mãi đã hết hạn
                DELETE FROM dbo.Promotion_detail
                WHERE id_prom = @id_prom AND id_category = @id_category;

                FETCH NEXT FROM expired_prom_cursor INTO @id_prom, @id_category;
            END;

            CLOSE expired_prom_cursor;
            DEALLOCATE expired_prom_cursor;

            -- Xóa các chương trình khuyến mãi không còn chi tiết nào
            DELETE FROM dbo.Promotion
            WHERE id_prom NOT IN (SELECT DISTINCT id_prom FROM dbo.Promotion_detail)
              AND end_date < GETDATE();
        END
        """
        cursor.execute(create_sql)
        print("Đã tạo stored procedure sp_RestorePriceAfterPromotionEnds thành công")
        return True
    except Exception as e:
        print(f"Lỗi khi tạo stored procedure sp_RestorePriceAfterPromotionEnds: {str(e)}")
        return False