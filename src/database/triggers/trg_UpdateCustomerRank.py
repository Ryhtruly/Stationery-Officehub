def create_trigger_update_customer_rank(cursor):
    try:
        # Xóa trigger cũ nếu tồn tại
        drop_sql = "IF EXISTS (SELECT * FROM sys.triggers WHERE name = 'trg_UpdateCustomerRank') DROP TRIGGER trg_UpdateCustomerRank"
        cursor.execute(drop_sql)

        # Tạo trigger mới
        create_sql = """
        CREATE TRIGGER trg_UpdateCustomerRank
        ON dbo.Bill
        AFTER INSERT, UPDATE
        AS
        BEGIN
            SET NOCOUNT ON;

            -- Cập nhật hạng khách hàng dựa trên tổng chi tiêu
            UPDATE c
            SET rank = CASE
                    WHEN (SELECT SUM(total) FROM dbo.Bill WHERE id_cust = c.id_cust) >= 10000000 THEN 'Diamond'
                    WHEN (SELECT SUM(total) FROM dbo.Bill WHERE id_cust = c.id_cust) >= 5000000 THEN 'Platinum'
                    WHEN (SELECT SUM(total) FROM dbo.Bill WHERE id_cust = c.id_cust) >= 2000000 THEN 'Gold'
                    WHEN (SELECT SUM(total) FROM dbo.Bill WHERE id_cust = c.id_cust) >= 1000000 THEN 'Silver'
                    ELSE 'Bronze'
                END
            FROM dbo.Customers c
            WHERE c.id_cust IN (
                SELECT id_cust FROM inserted
            );
        END
        """
        cursor.execute(create_sql)
        print("Đã tạo trigger trg_UpdateCustomerRank thành công")
        return True
    except Exception as e:
        print(f"Lỗi khi tạo trigger trg_UpdateCustomerRank: {str(e)}")
        return False
