import traceback

import pyodbc
from src.database.connection import create_connection
from src.database.models.bill import HoaDon

class BillDAO:
    def __init__(self, connection=None):
        self.conn = connection if connection else create_connection()
        self.cursor = self.conn.cursor()

    def get_employee_id_from_account_id(self, account_id):
        """
        Ánh xạ id_account sang id_emp từ bảng Accounts
        """
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT id_emp
                FROM dbo.Accounts
                WHERE id_account = ?
            """
            cursor.execute(query, (account_id,))
            row = cursor.fetchone()
            if row:
                return row[0]
            return None
        except pyodbc.Error as e:
            print(f"Lỗi khi lấy id_emp từ id_account: {str(e)}")
            return None
        finally:
            cursor.close()

    def insert_bill(self, id_emp, id_cust, total):
        try:
            cursor = self.conn.cursor()
            # Lấy giá trị id_bill lớn nhất hiện tại
            cursor.execute("SELECT MAX(id_bill) FROM dbo.Bill")
            result = cursor.fetchone()
            new_id = 1  # Mặc định là 1 nếu bảng trống
            if result[0] is not None:
                new_id = int(result[0]) + 1

            print(f"Inserting bill with id_emp: {id_emp}")  # Log để kiểm tra

            # Thêm cột id_bill vào câu lệnh INSERT
            query = """
            INSERT INTO dbo.Bill (id_bill, id_emp, id_cust, total, date)
            VALUES (?, ?, ?, ?, GETDATE());
            """
            cursor.execute(query, (new_id, id_emp, id_cust, total))
            self.conn.commit()
            return new_id  # Trả về id_bill vừa chèn
        except pyodbc.Error as e:
            print(f"Lỗi khi chèn hóa đơn: {str(e)}")
            self.conn.rollback()
            return None
        finally:
            cursor.close()

    def safe_str(self, value):
        """Chuyển đổi giá trị thành chuỗi an toàn để xử lý encoding"""
        if value is None:
            return ""
        try:
            return str(value).encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        except (UnicodeEncodeError, UnicodeDecodeError) as e:
            print(f"Lỗi encoding cho giá trị: {value}, lỗi: {str(e)}")
            return str(value).encode('ascii', errors='ignore').decode('ascii')

    def get_all_bills(self):
        """
        Lấy tất cả hóa đơn từ database
        """
        bills = []
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT b.id_bill, b.id_emp, e.fullname AS employee_name, b.id_cust, c.fullname AS customer_name, 
                       b.total, b.date
                FROM dbo.Bill b
                LEFT JOIN dbo.Employees e ON b.id_emp = e.id_emp
                LEFT JOIN dbo.Customers c ON b.id_cust = c.id_cust
                ORDER BY b.date DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                bill = {
                    'id_bill': row[0],
                    'id_emp': row[1],
                    'employee_name': self.safe_str(row[2]),
                    'id_cust': row[3],
                    'customer_name': self.safe_str(row[4]) if row[4] else "Khách hàng",
                    'total': row[5],
                    'date': row[6]
                }
                bills.append(bill)

            cursor.close()
        except pyodbc.Error as e:
            print(f"Lỗi khi lấy danh sách hóa đơn: {str(e)}")
            traceback.print_exc()

        return bills

    def get_bills_by_employee(self, id_emp):
        """
        Lấy danh sách hóa đơn theo nhân viên
        """
        bills = []
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT b.id_bill, b.id_emp, e.fullname AS employee_name, b.id_cust, c.fullname AS customer_name, 
                       b.total, b.date
                FROM dbo.Bill b
                LEFT JOIN dbo.Employees e ON b.id_emp = e.id_emp
                LEFT JOIN dbo.Customers c ON b.id_cust = c.id_cust
                WHERE b.id_emp = ?
                ORDER BY b.date DESC
            """
            cursor.execute(query, (id_emp,))
            rows = cursor.fetchall()

            for row in rows:
                bill = {
                    'id_bill': row[0],
                    'id_emp': row[1],
                    'employee_name': self.safe_str(row[2]),
                    'id_cust': row[3],
                    'customer_name': self.safe_str(row[4]) if row[4] else "Khách hàng",
                    'total': row[5],
                    'date': row[6]
                }
                bills.append(bill)

            cursor.close()
        except pyodbc.Error as e:
            print(f"Lỗi khi lấy danh sách hóa đơn theo nhân viên: {str(e)}")
            traceback.print_exc()

        return bills

    def get_all_employees(self):
        """
        Lấy danh sách tất cả nhân viên
        """
        employees = []
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT id_emp, fullname
                FROM dbo.Employees
                WHERE status = 1  -- Giả định status = 1 là nhân viên đang hoạt động
                ORDER BY fullname
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                employee = {
                    'id': row[0],
                    'hoten': self.safe_str(row[1])  # Sẽ giữ tên key là 'hoten' để đồng bộ với code trước đó
                }
                employees.append(employee)

            cursor.close()
        except pyodbc.Error as e:
            print(f"Lỗi khi lấy danh sách nhân viên: {str(e)}")
            traceback.print_exc()

        return employees

    def get_bill_by_id(self, bill_id):
        """
        Lấy thông tin hóa đơn theo ID
        """
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT b.id_bill, b.id_emp, e.fullname AS employee_name, b.id_cust, c.fullname AS customer_name, 
                       b.total, b.date
                FROM dbo.Bill b
                LEFT JOIN dbo.Employees e ON b.id_emp = e.id_emp
                LEFT JOIN dbo.Customers c ON b.id_cust = c.id_cust
                WHERE b.id_bill = ?
            """
            cursor.execute(query, (bill_id,))
            row = cursor.fetchone()

            if row:
                return {
                    'id_bill': row[0],
                    'id_emp': row[1],
                    'employee_name': self.safe_str(row[2]),
                    'id_cust': row[3],
                    'customer_name': self.safe_str(row[4]) if row[4] else "Khách hàng",
                    'total': row[5],
                    'date': row[6]
                }
            return None
        except pyodbc.Error as e:
            print(f"Lỗi khi lấy thông tin hóa đơn theo ID: {str(e)}")
            traceback.print_exc()
            return None

    def update_bill(self, id_bill, id_employee, id_cust, total):
        """
        Cập nhật hóa đơn
        """
        try:
            cursor = self.conn.cursor()
            query = """
                UPDATE dbo.Bill
                SET id_emp = ?, id_cust = ?, total = ?
                WHERE id_bill = ?
            """
            cursor.execute(query, (id_employee, id_cust, total, id_bill))
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            print(f"Lỗi khi cập nhật hóa đơn: {str(e)}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def delete_bill(self, id_bill):
        """
        Xóa hóa đơn và chi tiết hóa đơn
        """
        try:
            cursor = self.conn.cursor()
            # Xóa chi tiết hóa đơn trước
            cursor.execute("DELETE FROM dbo.Bill_detail WHERE id_bill = ?", (id_bill,))
            # Xóa hóa đơn
            cursor.execute("DELETE FROM dbo.Bill WHERE id_bill = ?", (id_bill,))
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            print(f"Lỗi khi xóa hóa đơn: {str(e)}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()