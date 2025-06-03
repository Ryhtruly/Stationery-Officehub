
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime
from src.database.models.import_product import NhapHang
from src.database.models.import_detail import ChiTietNhapHang
from src.modules.admin.data.import_detail_data import load_import_data, them_phieu_nhap


def setup_import_events(admin_window):
    """
    Thiết lập các sự kiện cho chức năng nhập hàng
    """
    if hasattr(admin_window.ui, 'refresh_import_btn'):
        admin_window.ui.refresh_import_btn.clicked.connect(lambda: refresh_import_table(admin_window))

    if hasattr(admin_window.ui, 'add_import_btn'):
        admin_window.ui.add_import_btn.clicked.connect(lambda: show_add_import_dialog(admin_window))


def refresh_import_table(admin_window):
    """
    Làm mới bảng nhập hàng
    """
    try:
        if hasattr(admin_window.ui, 'table_nhap'):
            load_import_data(admin_window.ui.table_nhap, admin_window)
    except Exception as e:
        QMessageBox.critical(
            admin_window,
            "Lỗi",
            f"Không thể làm mới bảng nhập hàng: {str(e)}",
            QMessageBox.Ok
        )


def show_add_import_dialog(admin_window):
    """
    Hiển thị dialog thêm phiếu nhập mới
    """
    try:
        # Tạo phiếu nhập mới (giả sử dữ liệu đã được nhập từ form)
        nhap_hang = NhapHang(
            id_imp=generate_import_id(),
            id_emp=admin_window.current_user.id_emp if hasattr(admin_window, 'current_user') else "EMP001",
            # Giả sử có thông tin người dùng hiện tại
            date=datetime.now()
        )

        # Tạo danh sách chi tiết phiếu nhập (giả sử dữ liệu đã được nhập từ form)
        chi_tiet_list = []
        # chi_tiet_list.append(ChiTietNhapHang(id_imp=nhap_hang.id_imp, id_prod=1, quantity=10, price=100000))
        # chi_tiet_list.append(ChiTietNhapHang(id_imp=nhap_hang.id_imp, id_prod=2, quantity=5, price=200000))

        # Thêm phiếu nhập vào database
        if them_phieu_nhap(nhap_hang, chi_tiet_list):
            QMessageBox.information(
                admin_window,
                "Thông báo",
                "Thêm phiếu nhập thành công!",
                QMessageBox.Ok
            )

            # Làm mới bảng nhập hàng
            refresh_import_table(admin_window)
        else:
            QMessageBox.warning(
                admin_window,
                "Cảnh báo",
                "Thêm phiếu nhập không thành công!",
                QMessageBox.Ok
            )
    except Exception as e:
        QMessageBox.critical(
            admin_window,
            "Lỗi",
            f"Không thể thêm phiếu nhập: {str(e)}",
            QMessageBox.Ok
        )


def generate_import_id():
    """
    Tạo ID mới cho phiếu nhập
    Format: IMP + YYMMDD + 3 số ngẫu nhiên
    """
    from datetime import datetime
    import random

    now = datetime.now()
    date_part = now.strftime("%y%m%d")
    random_part = str(random.randint(100, 999))

    return f"IMP{date_part}{random_part}"
