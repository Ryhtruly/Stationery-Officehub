def create_trigger_apply_discount_on_promotion(cursor):
    try:
        # Xóa trigger cũ nếu tồn tại
        drop_sql = "IF EXISTS (SELECT * FROM sys.triggers WHERE name = 'trg_ApplyDiscountOnPromotion') DROP TRIGGER trg_ApplyDiscountOnPromotion"
        cursor.execute(drop_sql)

        # Tạo trigger mới
        create_sql = """
        CREATE TRIGGER trg_ApplyDiscountOnPromotion
        ON dbo.Promotion_detail
        AFTER INSERT, UPDATE
        AS
        BEGIN
            SET NOCOUNT ON;

            -- Lấy danh sách các danh mục và phần trăm giảm giá từ bản ghi vừa thêm/cập nhật
            DECLARE @id_prom INT, @id_category INT, @percent_discount FLOAT;

            DECLARE discount_cursor CURSOR FOR
            SELECT i.id_prom, i.id_category, i.percent_discount
            FROM inserted i;

            OPEN discount_cursor;
            FETCH NEXT FROM discount_cursor INTO @id_prom, @id_category, @percent_discount;

            WHILE @@FETCH_STATUS = 0
            BEGIN
                -- Kiểm tra xem chương trình khuyến mãi có đang trong thời gian hiệu lực không
                IF EXISTS (
                    SELECT 1
                    FROM dbo.Promotion p
                    WHERE p.id_prom = @id_prom
                      AND GETDATE() BETWEEN p.start_date AND p.end_date
                )
                BEGIN
                    -- Cập nhật promotion_price cho các sản phẩm thuộc danh mục này
                    UPDATE p
                    SET promotion_price = p.price * (1 - @percent_discount / 100)
                    FROM dbo.Products p
                    WHERE p.id_category = @id_category;
                END

                FETCH NEXT FROM discount_cursor INTO @id_prom, @id_category, @percent_discount;
            END;

            CLOSE discount_cursor;
            DEALLOCATE discount_cursor;
        END
        """
        cursor.execute(create_sql)
        print("Đã tạo trigger trg_ApplyDiscountOnPromotion thành công")
        return True
    except Exception as e:
        print(f"Lỗi khi tạo trigger trg_ApplyDiscountOnPromotion: {str(e)}")
        return False