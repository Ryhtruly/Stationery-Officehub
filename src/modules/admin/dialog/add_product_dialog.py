from src.modules.admin.ui.ui_py.add_product import Ui_Form
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from src.database.DAO.admin.CategoryDAO import CategoryDAO
from src.database.DAO.admin.ProductAdminDAO import ProductDAO
from src.database.connection import create_connection

class AddProductDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, product_id=None):
        super(AddProductDialog, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.product_id = product_id

        self.setWindowTitle("Thêm sản phẩm mới" if product_id is None else "Cập nhật sản phẩm")

        if hasattr(self.ui, "them_sua_label"):
            self.ui.them_sua_label.setText("THÊM SẢN PHẨM MỚI" if product_id is None else "CẬP NHẬT SẢN PHẨM")

        if hasattr(self.ui, "huy_btn"):
            self.ui.huy_btn.clicked.connect(self.close)
        if hasattr(self.ui, "them_btn"):
            self.ui.them_btn.clicked.connect(self.save_product)
            self.ui.them_btn.setText("Thêm" if product_id is None else "Cập nhật")

        if product_id is not None:
            if hasattr(self.ui, "line_id"):
                self.ui.line_id.setReadOnly(True)
                self.ui.line_id.setEnabled(False)

        self.load_categories()

        if product_id is not None:
            self.load_product_data()
        else:
            self.generate_new_id()

    def load_categories(self):
        """
        Nạp danh sách danh mục vào combo box và tự động chọn danh mục hiện tại của sản phẩm nếu đang ở chế độ sửa
        """
        print("Bắt đầu nạp danh mục...")
        try:
            if hasattr(self.ui, "combo_box_danhmuc"):
                print("Tìm thấy combo box danh mục: combo_box_danhmuc")
                categories = CategoryDAO.get_all_categories()
                print(f"Đã lấy được {len(categories)} danh mục từ database")
                self.ui.combo_box_danhmuc.clear()
                self.ui.combo_box_danhmuc.addItem("Thêm danh mục", -1)
                for category in categories:
                    print(f"Thêm danh mục: {category.name} (ID: {category.id_category})")
                    self.ui.combo_box_danhmuc.addItem(category.name, category.id_category)

                if self.product_id is not None:
                    print(f"Đang sửa sản phẩm có ID: {self.product_id}")
                    product = ProductDAO.get_product_by_id(self.product_id)
                    if product:
                        category_id = getattr(product, "id_category", None)
                        print(f"Sản phẩm thuộc danh mục ID: {category_id}")
                        if category_id is not None:
                            index = self.ui.combo_box_danhmuc.findData(category_id)
                            print(f"Index của danh mục trong combo box: {index}")
                            if index >= 0:
                                self.ui.combo_box_danhmuc.setCurrentIndex(index)
                                print(f"Đã chọn danh mục: {self.ui.combo_box_danhmuc.currentText()} (ID: {category_id})")
                            else:
                                print(f"Không tìm thấy danh mục có ID: {category_id} trong combo box")
                    else:
                        print(f"Không tìm thấy sản phẩm có ID: {self.product_id}")
                try:
                    self.ui.combo_box_danhmuc.currentIndexChanged.disconnect()
                except:
                    pass
                self.ui.combo_box_danhmuc.currentIndexChanged.connect(self.on_category_changed)
                print("Hoàn thành nạp danh mục vào combo box")
            else:
                print("Không tìm thấy combo box danh mục trong UI!")
        except Exception as e:
            print(f"Lỗi khi nạp danh sách danh mục: {e}")
            import traceback
            traceback.print_exc()

    def generate_new_id(self):
        """
        Tạo ID mới cho sản phẩm bằng cách lấy ID lớn nhất từ bảng Products và tăng thêm 1
        """
        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT MAX(id_prod) FROM Products")
            max_id = cursor.fetchone()[0]
            if max_id is None:
                new_id = 1
            else:
                new_id = max_id + 1
            self.ui.line_id.setText(str(new_id))
            cursor.close()
            connection.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Không thể tạo ID mới: {str(e)}")

    def on_category_changed(self, index):
        """
        Xử lý khi người dùng chọn một mục trong combo box danh mục
        """
        try:
            if index == 0:
                self.show_add_category_dialog()
        except Exception as e:
            print(f"Lỗi khi xử lý sự kiện chọn danh mục: {e}")
            import traceback
            traceback.print_exc()

    def show_add_category_dialog(self):
        """
        Hiển thị dialog thêm danh mục mới
        """
        try:
            category_name, ok = QtWidgets.QInputDialog.getText(
                self,
                "Thêm danh mục mới",
                "Nhập tên danh mục mới:"
            )
            if ok and category_name:
                new_category_id = CategoryDAO.add_category(category_name)
                if new_category_id:
                    print(f"Đã thêm danh mục mới: {category_name} (ID: {new_category_id})")
                    self.ui.combo_box_danhmuc.addItem(category_name, new_category_id)
                    index = self.ui.combo_box_danhmuc.findData(new_category_id)
                    if index >= 0:
                        self.ui.combo_box_danhmuc.currentIndexChanged.disconnect(self.on_category_changed)
                        self.ui.combo_box_danhmuc.setCurrentIndex(index)
                        self.ui.combo_box_danhmuc.currentIndexChanged.connect(self.on_category_changed)
                else:
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Lỗi",
                        "Không thể thêm danh mục mới. Vui lòng thử lại!"
                    )
                    if self.ui.combo_box_danhmuc.count() > 1:
                        self.ui.combo_box_danhmuc.currentIndexChanged.disconnect(self.on_category_changed)
                        self.ui.combo_box_danhmuc.setCurrentIndex(1)
                        self.ui.combo_box_danhmuc.currentIndexChanged.connect(self.on_category_changed)
            else:
                if self.ui.combo_box_danhmuc.count() > 1:
                    self.ui.combo_box_danhmuc.currentIndexChanged.disconnect(self.on_category_changed)
                    self.ui.combo_box_danhmuc.setCurrentIndex(1)
                    self.ui.combo_box_danhmuc.currentIndexChanged.connect(self.on_category_changed)
        except Exception as e:
            print(f"Lỗi khi hiển thị dialog thêm danh mục: {e}")
            import traceback
            traceback.print_exc()
            if hasattr(self.ui, "combo_box_danhmuc") and self.ui.combo_box_danhmuc.count() > 1:
                self.ui.combo_box_danhmuc.currentIndexChanged.disconnect(self.on_category_changed)
                self.ui.combo_box_danhmuc.setCurrentIndex(1)
                self.ui.combo_box_danhmuc.currentIndexChanged.connect(self.on_category_changed)

    def save_product(self):
        try:
            id_text = self.ui.line_id.text().strip() if hasattr(self.ui, "line_id") else ""
            name = self.ui.line_name.text().strip() if hasattr(self.ui, "line_name") else ""
            unit = self.ui.line_unit.text().strip() if hasattr(self.ui, "line_unit") else ""
            price_str = self.ui.line_gia_ban.text().strip() if hasattr(self.ui, "line_gia_ban") else ""
            description = self.ui.line_ghiChu.text().strip() if hasattr(self.ui, "line_ghiChu") else ""
            image_url = self.ui.line_link_hinhanh.text().strip() if hasattr(self.ui, "line_link_hinhanh") else ""

            if not id_text:
                QMessageBox.warning(self, "Lỗi", "ID sản phẩm không được để trống.")
                return
            try:
                id_prod = int(id_text)
            except ValueError:
                QMessageBox.warning(self, "Lỗi", "ID sản phẩm phải là số nguyên.")
                return
            if not name:
                QMessageBox.warning(self, "Lỗi", "Tên sản phẩm không được để trống.")
                return
            if not unit:
                QMessageBox.warning(self, "Lỗi", "Đơn vị sản phẩm không được để trống.")
                return
            try:
                price = float(price_str) if price_str else 0
                if price < 0:
                    QMessageBox.warning(self, "Lỗi", "Giá bán không được âm.")
                    return
            except ValueError:
                QMessageBox.warning(self, "Lỗi", "Giá bán phải là một số hợp lệ.")
                return
            category_id = -1
            if hasattr(self.ui, "combo_box_danhmuc") and self.ui.combo_box_danhmuc.currentIndex() > 0:
                category_id = self.ui.combo_box_danhmuc.currentData()
            if category_id == -1:
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn danh mục sản phẩm.")
                return

            if self.product_id is None:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM Products WHERE id_prod = ?", (id_prod,))
                count = cursor.fetchone()[0]
                cursor.close()
                connection.close()
                if count > 0:
                    QMessageBox.warning(self, "Lỗi", f"ID sản phẩm {id_prod} đã tồn tại.")
                    return

            product_data = {
                "name": name,
                "unit": unit,
                "price": price,
                "description": description,
                "id_category": category_id,
                "image_url": image_url
            }

            if self.product_id is None:
                success = ProductDAO.add_product(product_data)
                if success:
                    QMessageBox.information(self, "Thành công", "Thêm sản phẩm mới thành công!")
                    self.accept()
                else:
                    QMessageBox.critical(self, "Lỗi", "Không thể thêm sản phẩm. Vui lòng thử lại sau.")
            else:
                product_data["id_prod"] = self.product_id
                success = ProductDAO.update_product(product_data)
                if success:
                    QMessageBox.information(self, "Thành công", "Cập nhật sản phẩm thành công!")
                    self.accept()
                else:
                    QMessageBox.critical(self, "Lỗi", "Không thể cập nhật sản phẩm. Vui lòng thử lại sau.")

        except Exception as e:
            import traceback
            print(f"Lỗi khi lưu sản phẩm: {str(e)}")
            print(traceback.format_exc())
            QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def load_product_data(self):
        try:
            print(f"Đang nạp thông tin sản phẩm có ID: {self.product_id}")
            product = ProductDAO.get_product_by_id(self.product_id)
            if not product:
                QMessageBox.warning(self, "Lỗi", f"Không tìm thấy sản phẩm có ID: {self.product_id}")
                return
            print(f"Đã tìm thấy sản phẩm: {product.name}")
            if hasattr(self.ui, "line_id"):
                self.ui.line_id.setText(str(product.id_prod))
            if hasattr(self.ui, "line_name"):
                self.ui.line_name.setText(product.name)
            if hasattr(self.ui, "line_unit"):
                self.ui.line_unit.setText(product.unit)
            if hasattr(self.ui, "line_gia_ban"):
                self.ui.line_gia_ban.setText(str(product.price))
            if hasattr(self.ui, "line_ghiChu"):
                self.ui.line_ghiChu.setText(product.description)
            if hasattr(self.ui, "line_link_hinhanh"):
                self.ui.line_link_hinhanh.setText(product.image_url)
            if hasattr(self.ui, "combo_box_danhmuc"):
                index = self.ui.combo_box_danhmuc.findData(product.id_category)
                if index >= 0:
                    self.ui.combo_box_danhmuc.setCurrentIndex(index)
        except Exception as e:
            import traceback
            print(f"Lỗi khi nạp thông tin sản phẩm: {str(e)}")
            print(traceback.format_exc())
            QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi khi nạp thông tin sản phẩm: {str(e)}")