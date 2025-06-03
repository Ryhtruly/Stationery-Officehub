def create_trigger_update_bill_total(cursor):
    try:
        # Xóa trigger cũ nếu tồn tại
        drop_sql = "IF EXISTS (SELECT * FROM sys.triggers WHERE name = 'trg_UpdateBillTotal') DROP TRIGGER trg_UpdateBillTotal"
        cursor.execute(drop_sql)

        # Tạo trigger mới
        create_sql = """
        CREATE TRIGGER trg_UpdateBillTotal
        ON dbo.Bill_detail
        AFTER INSERT, UPDATE, DELETE
        AS
        BEGIN
            SET NOCOUNT ON;

            -- Cập nhật tổng tiền cho các hóa đơn bị ảnh hưởng
            UPDATE b
            SET total = (
                SELECT SUM(bd.quantity * bd.price * (1 - ISNULL(bd.discount, 0)))
                FROM dbo.Bill_detail bd
                WHERE bd.id_bill = b.id_bill
            )
            FROM dbo.Bill b
            WHERE b.id_bill IN (
                SELECT id_bill FROM inserted
                UNION
                SELECT id_bill FROM deleted
            );
        END
        """
        cursor.execute(create_sql)
        print("Đã tạo trigger trg_UpdateBillTotal thành công")
        return True
    except Exception as e:
        print(f"Lỗi khi tạo trigger trg_UpdateBillTotal: {str(e)}")
        return False
