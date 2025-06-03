def create_trigger_default_customer_rank(cursor):
    try:
        # Xóa trigger cũ nếu tồn tại
        drop_sql = "IF EXISTS (SELECT * FROM sys.triggers WHERE name = 'trg_DefaultCustomerRank') DROP TRIGGER trg_DefaultCustomerRank"
        cursor.execute(drop_sql)

        # Tạo trigger mới
        create_sql = """
        CREATE TRIGGER trg_DefaultCustomerRank
        ON dbo.Customers
        AFTER INSERT
        AS
        BEGIN
            SET NOCOUNT ON;

            UPDATE c
            SET rank = 'Bronze'
            FROM dbo.Customers c
            INNER JOIN inserted i ON c.id_cust = i.id_cust
            WHERE i.rank IS NULL;
        END
        """
        cursor.execute(create_sql)
        print("Đã tạo trigger trg_DefaultCustomerRank thành công")
        return True
    except Exception as e:
        print(f"Lỗi khi tạo trigger trg_DefaultCustomerRank: {str(e)}")
        return False
