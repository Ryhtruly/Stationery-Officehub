import traceback

import pyodbc
from src.database.connection import create_connection

class BillDetailDAO:
    def __init__(self, connection=None):
        self.conn = connection if connection else create_connection()
        self.cursor = self.conn.cursor()

    def insert_bill_detail(self, bill_id, id_prod, quantity, price, discount):
        try:
            cursor = self.conn.cursor()
            print(f"Inserting bill detail with bill_id: {bill_id}, id_prod: {id_prod}, quantity: {quantity}, price: {price}, discount: {discount}")  # Log tham số đầu vào
            query = """
            INSERT INTO dbo.Bill_detail (id_bill, id_prod, quantity, price, discount)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (bill_id, id_prod, quantity, price, discount))
            self.conn.commit()
            print(f"Successfully inserted bill detail for bill_id: {bill_id}, id_prod: {id_prod}")
            return True
        except pyodbc.Error as e:
            print(f"Lỗi khi chèn chi tiết hóa đơn: {str(e)}")
            print(f"Parameters: bill_id={bill_id}, id_prod={id_prod}, quantity={quantity}, price={price}, discount={discount}")
            traceback.print_exc()
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def get_bill_details(self, bill_id):
        """
        Lấy chi tiết hóa đơn theo ID hóa đơn
        """
        details = []
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT id_bill, id_prod, quantity, price, discount
                FROM dbo.Bill_detail
                WHERE id_bill = ?
            """
            cursor.execute(query, (bill_id,))
            rows = cursor.fetchall()

            for row in rows:
                detail = {
                    'id_bill': row[0],
                    'id_prod': row[1],
                    'quantity': row[2],
                    'price': row[3],
                    'discount': row[4] if row[4] is not None else 0
                }
                details.append(detail)

            cursor.close()
            print(f"Bill details loaded for bill_id {bill_id}: {details}")  # Log
        except pyodbc.Error as e:
            print(f"Lỗi khi lấy chi tiết hóa đơn: {str(e)}")
            traceback.print_exc()
            return []

        return details