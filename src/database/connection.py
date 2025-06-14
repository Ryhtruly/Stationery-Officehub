import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def create_connection():
    """
    Tạo và trả về kết nối đến SQL Server

    Returns:
        pyodbc.Connection: Đối tượng kết nối đến database
    """
    try:
        # Thông tin kết nối từ biến môi trường
        server = os.getenv('DB_SERVER')
        database = os.getenv('DB_NAME')
        username = os.getenv('DB_USERNAME')
        password = os.getenv('DB_PASSWORD')

        # Tạo chuỗi kết nối
        conn_str = (
            f'DRIVER={{SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
        )

        # Thêm thông tin xác thực
        if username and password:
            conn_str += f'UID={username};PWD={password}'
        else:
            conn_str += 'Trusted_Connection=yes;'  # Windows Authentication

        # Kết nối đến database
        connection = pyodbc.connect(conn_str)
        return connection

    except Exception as e:
        print(f"Lỗi kết nối database: {str(e)}")
        raise

def test_connection():
    """
    Kiểm tra kết nối đến database
    """
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT @@version")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        print(f"Kết nối thành công!\nPhiên bản SQL Server: {version}")
        return True
    except Exception as e:
        print(f"Lỗi kết nối: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection()
