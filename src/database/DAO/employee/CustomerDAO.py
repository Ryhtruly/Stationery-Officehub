from src.database.connection import create_connection
from src.database.models.customer import KhachHang
from datetime import datetime

class CustomerDAO:
    """
    Lớp truy xuất dữ liệu khách hàng từ database
    """

    @staticmethod
    def get_all_customers():
        """
        Lấy tất cả khách hàng từ database

        Returns:
            list: Danh sách khách hàng
        """
        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = """
               SELECT c.id_cust, c.fullname, c.phone, c.rank, c.register_date
               FROM Customers c
               """

            cursor.execute(query)
            customers = []
            for row in cursor.fetchall():
                customer = KhachHang(
                    id_cust=row[0],
                    fullname=row[1],
                    phone=row[2],
                    rank=row[3],
                    register_date=row[4]
                )
                customers.append(customer)

            cursor.close()
            conn.close()
            return customers
        except Exception as e:
            print(f"Error fetching customers: {e}")
            return []

    @staticmethod
    def get_customer_by_id(customer_id):
        """
        Lấy thông tin khách hàng theo ID

        Args:
            customer_id: ID của khách hàng

        Returns:
            KhachHang: Đối tượng khách hàng
        """
        conn = None
        cursor = None
        try:
            conn = create_connection()
            if not conn:
                print("Không thể kết nối đến database")
                return None

            cursor = conn.cursor()

            query = """
            SELECT id_cust, fullname, phone, rank, register_date
            FROM Customers
            WHERE id_cust = ?
            """

            cursor.execute(query, (customer_id,))
            row = cursor.fetchone()

            if row:
                customer = KhachHang(
                    id_cust=row[0],
                    fullname=row[1],
                    phone=row[2],
                    rank=row[3],
                    register_date=row[4]
                )
                return customer
            return None
        except Exception as e:
            print(f"Lỗi khi lấy thông tin khách hàng: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def add_customer(fullname, phone):
        """
        Thêm khách hàng mới vào database

        Args:
            fullname (str): Tên khách hàng
            phone (str): Số điện thoại khách hàng
        """
        try:
            conn = create_connection()
            cursor = conn.cursor()

            # Thiết lập rank mặc định
            rank = 'Bronze'  # Hoặc bất kỳ giá trị mặc định nào bạn mong muốn

            # Ngày đăng ký là ngày hiện tại
            register_date = datetime.now().strftime('%Y-%m-%d')

            # Tìm ID lớn nhất hiện tại và tăng lên 1
            cursor.execute("SELECT MAX(id_cust) FROM Customers")
            result = cursor.fetchone()
            new_id = 1  # Mặc định là 1 nếu không có bản ghi nào
            if result[0] is not None:
                new_id = result[0] + 1

            query = """
            INSERT INTO Customers (id_cust, fullname, phone, rank, register_date)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (new_id, fullname, phone, rank, register_date))

            conn.commit()
            cursor.close()
            conn.close()

            return True
        except Exception as e:
            print(f"Error adding customer: {e}")
            raise  # Re-raise để có thể bắt lỗi ở lớp gọi

    @staticmethod
    def update_customer(customer):
        """
        Cập nhật thông tin khách hàng

        Args:
            customer: Đối tượng KhachHang cần cập nhật

        Returns:
            bool: True nếu thành công, False nếu thất bại
        """
        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = """
            UPDATE Customers
            SET fullname = ?, phone = ?, rank = ?, register_date = ?
            WHERE id_cust = ?
            """

            cursor.execute(query, (
                customer.fullname,
                customer.phone,
                customer.rank,
                customer.register_date,
                customer.id_cust
            ))

            conn.commit()
            cursor.close()
            conn.close()

            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật khách hàng: {e}")
            return False

    @staticmethod
    def update_customer_rank(customer_id):
        """
        Cập nhật rank của khách hàng dựa trên tổng tiền đã chi

        Args:
            customer_id: ID của khách hàng

        Returns:
            bool: True nếu thành công, False nếu thất bại
        """
        try:
            conn = create_connection()
            cursor = conn.cursor()

            # Tính tổng tiền đã chi
            query_total = """
            SELECT SUM(total) 
            FROM Bill 
            WHERE id_cust = ?
            """

            cursor.execute(query_total, (customer_id,))
            result = cursor.fetchone()
            total_spent = result[0] if result and result[0] is not None else 0

            # Lấy thông tin khách hàng
            query_customer = """
            SELECT register_date FROM Customers WHERE id_cust = ?
            """

            cursor.execute(query_customer, (customer_id,))
            row = cursor.fetchone()

            if not row:
                cursor.close()
                conn.close()
                return False

            register_date = row[0]

            # Xác định rank dựa trên tổng tiền
            new_rank = "Bronze"  # Mặc định

            if total_spent >= 5000000:
                new_rank = "Diamond"
            elif total_spent >= 3000000:
                new_rank = "Platinum"
            elif total_spent >= 1000000:
                new_rank = "Gold"
            elif total_spent >= 500000:
                new_rank = "Silver"

            # Cập nhật rank
            query_update = """
            UPDATE Customers
            SET rank = ?
            WHERE id_cust = ?
            """

            cursor.execute(query_update, (new_rank, customer_id))

            conn.commit()
            cursor.close()
            conn.close()

            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật rank khách hàng: {e}")
            return False

    @staticmethod
    def check_phone_exists(phone_number):
        try:
            connection = create_connection()
            cursor = connection.cursor()

            # Sửa câu lệnh SQL để sử dụng dấu hiệu tham số đúng
            query = "SELECT COUNT(*) FROM Customers WHERE phone = ?"
            cursor.execute(query, (phone_number,))

            result = cursor.fetchone()
            cursor.close()
            connection.close()

            return result[0] > 0

        except Exception as e:
            print(f"Lỗi khi kiểm tra số điện thoại: {str(e)}")
            return False

    @staticmethod
    def delete_customer(customer_id):
        """
        Xóa khách hàng từ database

        Args:
            customer_id: ID của khách hàng

        Returns:
            tuple: (success, message)
        """
        try:
            conn = create_connection()
            cursor = conn.cursor()

            # Kiểm tra xem khách hàng có hóa đơn không
            query_check = """
            SELECT COUNT(*) FROM dbo.Bill WHERE id_cust = ?
            """
            cursor.execute(query_check, (customer_id,))
            count = cursor.fetchone()[0]

            if count > 0:
                return False, "Không thể xóa khách hàng này vì đã có hóa đơn liên quan!"

            # Xóa khách hàng
            query_delete = """
            DELETE FROM Customers WHERE id_cust = ?
            """
            cursor.execute(query_delete, (customer_id,))

            conn.commit()
            cursor.close()
            conn.close()

            return True, "Xóa khách hàng thành công!"
        except Exception as e:
            return False, f"Đã xảy ra lỗi khi xóa khách hàng: {str(e)}"
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_customer_by_phone(phone, connection=None):
        """
        Lấy thông tin khách hàng dựa trên số điện thoại

        Args:
            phone (str): Số điện thoại của khách hàng
            connection: Đối tượng kết nối cơ sở dữ liệu (tùy chọn)

        Returns:
            dict: Thông tin khách hàng (id_cust, fullname, phone, rank, register_date) hoặc None nếu không tìm thấy
        """
        close_connection = False
        if connection is None:
            connection = create_connection()
            close_connection = True

        try:
            cursor = connection.cursor()
            query = "SELECT id_cust, fullname, phone, rank, register_date FROM dbo.Customers WHERE phone = ?"
            cursor.execute(query, (phone,))
            row = cursor.fetchone()
            if row:
                return {
                    'id_cust': row[0],
                    'fullname': row[1],
                    'phone': row[2],
                    'rank': row[3],
                    'register_date': row[4]
                }
            return None
        except Exception as e:
            print(f"Lỗi khi tìm khách hàng theo số điện thoại: {str(e)}")
            return None
        finally:
            if cursor:
                cursor.close()
            if close_connection and connection:
                connection.close()