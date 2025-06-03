import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from src.modules.login.view.login_window import LoginWindow
from src.modules.admin.views.admin_window import AdminWindow
from src.modules.employee.view.employee_window import EmployeeWindow
from src.modules.login.ui.ui_py import resource_rc
from src.modules.employee.ui.ui_py import resource_rc
from src.modules.admin.ui.ui_py import resource_rc
from src.modules.login.data.login_data import LoginData
from src.database.connection import test_connection, create_connection
from src.database.triggers.trigger_manager import setup_all_triggers
import locale
locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')
global_app = None
current_windows = {}

def load_stylesheet(role):
    # Xây dựng đường dẫn đến file style.qss trong src/modules/{role}/styles/
    base_path = os.path.abspath(os.path.dirname(__file__))
    style_path = os.path.join(base_path, "modules", role, "styles", "style.qss")
    try:
        with open(style_path, "r", encoding="utf-8") as style_file:
            return style_file.read()
    except FileNotFoundError:
        print(f"Không tìm thấy {style_path}, tiếp tục mà không áp dụng style.")
        return ""
    except Exception as e:
        print(f"Lỗi khi load {style_path}: {e}")
        return ""

def open_window(account_id, username, role, login_window=None):
    global current_windows
    try:
        stylesheet = load_stylesheet(role)

        if role.lower() == "admin":
            window = AdminWindow(account_id=account_id)
        elif role.lower() == "employee" or role.lower() == "user":
            window = EmployeeWindow(account_id=account_id)  # Truyền account_id
        else:
            QMessageBox.warning(None, "Lỗi", f"Vai trò không hợp lệ: {role}")
            return None

        if stylesheet:
            window.setStyleSheet(stylesheet)

        if hasattr(window, 'logout_btn'):
            window.logout_btn.clicked.connect(lambda: handle_logout(window))
        elif hasattr(window, 'ui') and hasattr(window.ui, 'logout_btn'):
            window.ui.logout_btn.clicked.connect(lambda: handle_logout(window))

        current_windows['main_window'] = window
        window.show()

        if login_window:
            login_window.hide()

        return window
    except Exception as e:
        QMessageBox.critical(None, "Lỗi", f"Lỗi khi mở cửa sổ: {str(e)}")
        return None

def handle_logout(current_window):
    global current_windows
    try:
        if current_window:
            current_window.hide()
            current_window.deleteLater()

        login_window = create_login_window()
        current_windows['login_window'] = login_window
    except Exception as e:
        QMessageBox.critical(None, "Lỗi", f"Lỗi khi đăng xuất: {str(e)}")

def create_login_window():
    global current_windows
    try:
        login_window = LoginWindow(authenticate_callback=on_authenticated)
        current_windows['login_window'] = login_window

        def on_login_clicked():
            try:
                username = login_window.ui.username_line.text().strip()
                password = login_window.ui.password_line.text().strip()

                success, message, user_info = LoginData.validate_login(username, password)
                if success and user_info:
                    account_id = user_info.get('account_id', 0)
                    role = user_info.get('role', 'user')
                    open_window(account_id, username, role, login_window)
                else:
                    QMessageBox.warning(login_window, "Lỗi đăng nhập", message)
            except Exception as e:
                QMessageBox.critical(login_window, "Lỗi", f"Lỗi khi đăng nhập: {str(e)}")

        try:
            login_window.ui.login_btn.clicked.disconnect()
        except TypeError:
            pass

        login_window.ui.login_btn.clicked.connect(on_login_clicked)
        login_window.show()
        return login_window
    except Exception as e:
        QMessageBox.critical(None, "Lỗi", f"Lỗi khi tạo cửa sổ đăng nhập: {str(e)}")
        return None

def on_authenticated(account_id, username, role):
    try:
        open_window(account_id, username, role)
    except Exception as e:
        QMessageBox.critical(None, "Lỗi", f"Lỗi khi xử lý xác thực: {str(e)}")

def main():
    global global_app
    try:
        global_app = QApplication(sys.argv)

        if not test_connection():
            QMessageBox.critical(None, "Lỗi kết nối", "Không thể kết nối đến database. Ứng dụng sẽ thoát.")
            return 1

        try:
            conn = create_connection()
            cursor = conn.cursor()
            setup_all_triggers(cursor)
            conn.commit()
            print("Đã thiết lập trigger thành công")
        except Exception as e:
            QMessageBox.warning(None, "Cảnh báo", f"Có lỗi khi thiết lập trigger: {str(e)}\nỨng dụng vẫn tiếp tục.")

        create_login_window()
        return global_app.exec_()
    except Exception as e:
        QMessageBox.critical(None, "Lỗi", f"Lỗi khởi động ứng dụng: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())