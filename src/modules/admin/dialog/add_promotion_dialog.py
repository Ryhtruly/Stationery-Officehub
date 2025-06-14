from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QCheckBox, QDoubleSpinBox, QHBoxLayout, QWidget
from src.database.connection import create_connection
from src.modules.admin.ui.ui_py.add_promotion import Ui_Form
from src.database.DAO.admin.CategoryDAO import CategoryDAO
from src.database.DAO.admin.PromotionDAO import KhuyenMaiDAO
from datetime import datetime
import traceback
import re

from src.database.models.promotion import Promotion

class AddPromotionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, promotion_id=None):
        try:
            print("Bắt đầu khởi tạo AddPromotionDialog")
            super(AddPromotionDialog, self).__init__(parent)
            self.ui = Ui_Form()
            print("Thiết lập UI")
            self.ui.setupUi(self)

            self.promotion_id = promotion_id

            self.setWindowTitle("Thêm khuyến mãi mới" if promotion_id is None else "Cập nhật khuyến mãi")

            if hasattr(self.ui, "them_sua_label"):
                self.ui.them_sua_label.setText("THÊM KHUYẾN MÃI MỚI" if promotion_id is None else "CẬP NHẬT KHUYẾN MÃI")

            if hasattr(self.ui, "them_btn"):
                self.ui.them_btn.setText("Thêm" if promotion_id is None else "Cập nhật")

            print("Khởi tạo DAO")
            self.category_dao = CategoryDAO()
            self.promotion_dao = KhuyenMaiDAO()

            self.category_checkboxes = {}
            self.category_discount_spinboxes = {}

            print("Tạo QTableWidget mới")
            self.create_table_widget()

            print("Thiết lập ngày tháng")
            current_date = QtCore.QDate.currentDate()
            self.ui.start_date.setDate(current_date)
            self.ui.end_date.setDate(current_date.addDays(7))

            print("Kết nối signals và slots")
            self.connect_signals()

            print("Tạo ID khuyến mãi")
            self.generate_promotion_id()

            print("Thiết lập bảng danh mục")
            self.setup_category_table()

            print("Load dữ liệu danh mục")
            self.load_categories()

            print("Khởi tạo AddPromotionDialog hoàn tất")

            if promotion_id is not None:
                self.load_promotion_data()

        except Exception as e:
            print(f"Lỗi trong __init__: {e}")
            traceback.print_exc()

    def connect_signals(self):
        try:
            self.ui.them_btn.clicked.connect(self.add_promotion)
            self.ui.huy_btn.clicked.connect(self.reject)
        except Exception as e:
            print(f"Lỗi khi kết nối signals: {e}")
            traceback.print_exc()

    def create_table_widget(self):
        try:
            self.table_widget = QtWidgets.QTableWidget()
            self.table_widget.setColumnCount(3)
            self.table_widget.setHorizontalHeaderLabels(["Chọn", "Danh mục", "Giảm giá (%)"])
            self.table_widget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            self.table_widget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            self.table_widget.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            if hasattr(self.ui, "table_widget"):
                layout = QtWidgets.QVBoxLayout(self.ui.table_widget)
                layout.addWidget(self.table_widget)
                layout.setContentsMargins(0, 0, 0, 0)
        except Exception as e:
            print(f"Lỗi khi tạo bảng: {e}")
            traceback.print_exc()

    def generate_promotion_id(self):
        try:
            new_id = self.promotion_dao.generate_next_promotion_id()
            self.ui.input_Id_khuyenmai.setText(str(new_id))
        except Exception as e:
            print(f"Lỗi khi tạo ID khuyến mãi: {e}")
            traceback.print_exc()
            self.ui.input_Id_khuyenmai.setText("1")

    def setup_category_table(self):
        try:
            self.table_widget.setRowCount(0)
            self.table_widget.setHorizontalHeaderLabels(["Chọn", "Danh mục", "Giảm giá (%)"])
            self.table_widget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            self.table_widget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            self.table_widget.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        except Exception as e:
            print(f"Lỗi khi thiết lập bảng danh mục: {e}")
            traceback.print_exc()

    def load_categories(self):
        try:
            categories = self.category_dao.get_all_categories()
            self.table_widget.setRowCount(0)
            self.category_checkboxes.clear()
            self.category_discount_spinboxes.clear()
            for category in categories:
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                checkbox = QCheckBox()
                checkbox_widget = QWidget()
                checkbox_layout = QHBoxLayout(checkbox_widget)
                checkbox_layout.addWidget(checkbox)
                checkbox_layout.setAlignment(QtCore.Qt.AlignCenter)
                checkbox_layout.setContentsMargins(0, 0, 0, 0)
                self.table_widget.setCellWidget(row_position, 0, checkbox_widget)
                self.table_widget.verticalHeader().setVisible(False)
                self.ui.input_Id_khuyenmai.setReadOnly(True)
                self.category_checkboxes[category.id_category] = checkbox
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(category.name))
                spinbox = QDoubleSpinBox()
                spinbox.setMinimum(0)
                spinbox.setMaximum(100)
                spinbox.setDecimals(2)
                spinbox.setSuffix("%")
                spinbox_widget = QWidget()
                spinbox_layout = QHBoxLayout(spinbox_widget)
                spinbox_layout.addWidget(spinbox)
                spinbox_layout.setAlignment(QtCore.Qt.AlignCenter)
                spinbox_layout.setContentsMargins(0, 0, 0, 0)
                self.table_widget.setCellWidget(row_position, 2, spinbox_widget)
                self.category_discount_spinboxes[category.id_category] = spinbox
            print(f"Đã tải {len(categories)} danh mục vào bảng")
        except Exception as e:
            print(f"Lỗi khi tải danh mục: {e}")
            traceback.print_exc()

    def load_promotion_data(self):
        try:
            print(f"Đang tải dữ liệu cho khuyến mãi ID: {self.promotion_id}")
            promotion_dao = KhuyenMaiDAO()
            promotion = promotion_dao.get_khuyen_mai_by_id(self.promotion_id)
            if promotion:
                self.ui.input_Id_khuyenmai.setText(str(promotion.id_prom))
                self.ui.input_ten_khuyenmai.setText(promotion.name)
                if isinstance(promotion.start_date, str):
                    start_date = QtCore.QDate.fromString(promotion.start_date, "yyyy-MM-dd")
                else:
                    start_date = QtCore.QDate.fromString(promotion.start_date.strftime("%Y-%m-%d"), "yyyy-MM-dd")
                if isinstance(promotion.end_date, str):
                    end_date = QtCore.QDate.fromString(promotion.end_date, "yyyy-MM-dd")
                else:
                    end_date = QtCore.QDate.fromString(promotion.end_date.strftime("%Y-%m-%d"), "yyyy-MM-dd")
                self.ui.start_date.setDate(start_date)
                self.ui.end_date.setDate(end_date)
                self.load_promotion_details(self.promotion_id)
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu khuyến mãi: {str(e)}")
            traceback.print_exc()
            QMessageBox.critical(self, "Lỗi", f"Không thể tải dữ liệu khuyến mãi: {str(e)}")

    def load_promotion_details(self, promotion_id):
        try:
            for id_category in self.category_checkboxes:
                self.category_checkboxes[id_category].setChecked(False)
                self.category_discount_spinboxes[id_category].setValue(0)
            details = self.promotion_dao.get_promotion_details(promotion_id)
            if details:
                for detail in details:
                    id_category = detail['id_category']
                    percent_discount = detail['percent_discount']
                    print(f"Loading promotion detail: id_category={id_category}, percent_discount={percent_discount}")
                    if id_category in self.category_checkboxes:
                        self.category_checkboxes[id_category].setChecked(True)
                        if percent_discount is not None:
                            try:
                                discount_value = float(percent_discount)
                                if 0 <= discount_value <= 100:
                                    self.category_discount_spinboxes[id_category].setValue(discount_value)
                                    self.category_discount_spinboxes[id_category].update()
                                else:
                                    print(f"Invalid percent_discount value for id_category {id_category}: {percent_discount}")
                                    self.category_discount_spinboxes[id_category].setValue(0)
                            except (ValueError, TypeError) as e:
                                print(f"Error converting percent_discount for id_category {id_category}: {str(e)}")
                                self.category_discount_spinboxes[id_category].setValue(0)
                        else:
                            print(f"percent_discount is None for id_category {id_category}")
                            self.category_discount_spinboxes[id_category].setValue(0)
        except Exception as e:
            print(f"Lỗi khi tải chi tiết khuyến mãi: {str(e)}")
            traceback.print_exc()

    def validate_promotion(self, id_prom, name):
        """Validate dữ liệu khuyến mãi trước khi lưu"""
        # Kiểm tra ID không âm
        try:
            id_prom = int(id_prom)
            if id_prom < 0:
                QMessageBox.warning(self, "Lỗi", "ID khuyến mãi không được âm.")
                return False
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "ID khuyến mãi phải là số nguyên.")
            return False

        if not re.match(r'^[\w\sÀ-ỹ0-9]+$', name, re.UNICODE):
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Khuyến mãi chỉ được chứa chữ, số và dấu cách.")
            return False

        # Kiểm tra tên trùng
        try:
            connection = create_connection()
            cursor = connection.cursor()
            if self.promotion_id:
                cursor.execute("SELECT COUNT(*) FROM Promotion WHERE LOWER(name) = LOWER(?) AND id_prom != ?",
                             (name, self.promotion_id))
            else:
                cursor.execute("SELECT COUNT(*) FROM Promotion WHERE LOWER(name) = LOWER(?)", (name,))
            count = cursor.fetchone()[0]
            cursor.close()
            connection.close()
            if count > 0:
                QMessageBox.warning(self, "Lỗi", f"Tên khuyến mãi '{name}' đã tồn tại.")
                return False
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi kiểm tra trùng tên khuyến mãi: {str(e)}")
            return False

        return True

    def add_promotion(self):
        try:
            id_prom_text = self.ui.input_Id_khuyenmai.text().strip()
            promotion_name = self.ui.input_ten_khuyenmai.text().strip()
            start_date = self.ui.start_date.date().toString("yyyy-MM-dd")
            end_date = self.ui.end_date.date().toString("yyyy-MM-dd")

            # Validate input
            if not id_prom_text:
                QMessageBox.warning(self, "Lỗi", "ID khuyến mãi không được để trống.")
                return
            if not promotion_name:
                QMessageBox.warning(self, "Lỗi", "Tên khuyến mãi không được để trống.")
                return
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            if end_date_obj < start_date_obj:
                QMessageBox.warning(self, "Lỗi", "Ngày kết thúc không được nhỏ hơn ngày bắt đầu!")
                return

            # Validate bổ sung
            if not self.validate_promotion(id_prom_text, promotion_name):
                return

            has_selected_category = False
            for checkbox in self.category_checkboxes.values():
                if checkbox.isChecked():
                    has_selected_category = True
                    break
            if not has_selected_category:
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn ít nhất một danh mục!")
                return

            if self.promotion_id is None:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM Promotion WHERE id_prom = ?", (id_prom_text,))
                count = cursor.fetchone()[0]
                cursor.close()
                connection.close()
                if count > 0:
                    QMessageBox.warning(self, "Lỗi", f"ID khuyến mãi {id_prom_text} đã tồn tại.")
                    return

            # Tạo đối tượng khuyến mãi
            promotion = Promotion(
                id_prom=int(id_prom_text),
                name=promotion_name,
                start_date=start_date_obj,
                end_date=end_date_obj,
            )

            # Lấy danh sách danh mục đã chọn và tỷ lệ giảm giá
            category_details = []
            for id_category, checkbox in self.category_checkboxes.items():
                if checkbox.isChecked():
                    discount_rate = self.category_discount_spinboxes[id_category].value()
                    if not 0 <= discount_rate <= 100:
                        QMessageBox.warning(self, "Lỗi", f"Phần trăm giảm giá cho danh mục {id_category} phải từ 0-100!")
                        return
                    category_details.append({
                        'id_category': id_category,
                        'percent_discount': discount_rate
                    })

            # Lưu thông tin khuyến mãi
            success = False
            if self.promotion_id is None:
                success = self.promotion_dao.add_promotion(promotion, category_details)
            else:
                success = self.promotion_dao.update_promotion(promotion, category_details)

            if success:
                QMessageBox.information(self, "Thành công",
                                        "Thêm khuyến mãi mới thành công!" if self.promotion_id is None else "Cập nhật khuyến mãi thành công!")
                self.accept()
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể lưu khuyến mãi. Vui lòng thử lại sau!")

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi xử lý: {str(e)}")
            print(f"Lỗi khi thêm/cập nhật khuyến mãi: {str(e)}")
            traceback.print_exc()