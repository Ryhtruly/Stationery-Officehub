from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QGridLayout, QScrollArea, QFrame,
                             QSizePolicy, QSpacerItem)
from src.modules.employee.dialog.product_info_dialog import ProductInfoDialog
from src.modules.employee.data.cart_data import CartData
import os

cart_data = CartData()

class ProductItemView(QFrame):
    def __init__(self, product_id, name, price, description, image_path=None):
        super(ProductItemView, self).__init__()
        self.product_id = product_id
        self.product_data = {
            'id': product_id,
            'name': name or "Không có tên",
            'price': float(price) if price is not None else 0.0,
            'description': description or "",
            'image_path': image_path or ""
        }
        self.setup_ui(self.product_data['name'], self.product_data['price'],
                      self.product_data['description'], self.product_data['image_path'])

    def show_product_info(self):
        try:
            info_dialog = ProductInfoDialog(self.product_data, parent=self)
            info_dialog.add_to_cart_signal.connect(self.add_to_cart)
            info_dialog.exec_()
        except Exception as e:
            print(f"Lỗi khi hiển thị thông tin sản phẩm: {str(e)}")

    def add_to_cart(self):
        print(f"Đã thêm sản phẩm {self.product_data['name']} vào giỏ hàng")
        cart_data.add_item(
            self.product_data['id'],
            self.product_data['name'],
            self.product_data['price'],
            1
        )

    def setup_ui(self, name, price, description, image_path):
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.3);
                border-radius: 10px;
                border: 1px solid rgba(60, 60, 60, 0.8);
            }
            QFrame > * {
                background-color: transparent;
                border: none;
                border-radius: 0px;
            }
            QFrame QLabel {
                color: #333333;
                background: transparent;
            }
            QFrame QPushButton {
                background-color: rgba(255, 87, 34, 0.8);
                border: 1px solid rgba(255, 87, 34, 1);
                border-radius: 16px;
            }
            QFrame QPushButton[objectName="info_btn"] {
                background-color: rgba(33, 150, 243, 0.8);
                border: 1px solid rgba(33, 150, 243, 1);
                border-radius: 16px;
            }
        """)
        self.setMinimumSize(200, 280)
        self.setMaximumSize(220, 300)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        cart_icon_path = os.path.join(base_dir, "employee", "ui", "ui_design", "icon", "cart-59-xl.png")
        info_icon_path = os.path.join(base_dir, "employee", "ui", "ui_design", "icon", "info-2-xxl.png")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        # Hình ảnh sản phẩm
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setMinimumHeight(120)
        image_label.setMaximumHeight(140)
        pixmap = None
        if image_path and image_path.strip():
            try:
                if image_path.startswith(('http://', 'https://')):
                    self.manager = QNetworkAccessManager()
                    self.manager.finished.connect(lambda reply: self.handle_image_response(reply, image_label))
                    request = QNetworkRequest(QUrl(image_path))
                    self.manager.get(request)
                    placeholder_path = "./static/images/loading.png"
                    if os.path.exists(placeholder_path):
                        pixmap = QPixmap(placeholder_path)
                    else:
                        pixmap = None
                else:
                    pixmap = QPixmap(image_path)
                    if pixmap.isNull():
                        pixmap = None
            except Exception as e:
                print(f"Lỗi khi tải hình ảnh: {str(e)}")
                pixmap = None

        if pixmap is None or pixmap.isNull():
            self.set_default_placeholder(image_label)
        else:
            pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
            image_label.setStyleSheet("")
        main_layout.addWidget(image_label)

        # Tên sản phẩm
        name_label = QLabel(name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setWordWrap(True)
        name_label.setStyleSheet("font-weight: bold; font-size: 14px; color: white")
        main_layout.addWidget(name_label)

        # Giá sản phẩm
        price_label = QLabel(f"{price:,.0f} đ")
        price_label.setAlignment(Qt.AlignCenter)
        price_label.setStyleSheet("color: #FF5555; font-weight: bold; font-size: 14px;")
        main_layout.addWidget(price_label)

        # Mô tả sản phẩm
        if description:
            desc_label = QLabel(description)
            desc_label.setAlignment(Qt.AlignCenter)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("color: white; font-size: 12px;")
            desc_label.setMaximumHeight(40)
            main_layout.addWidget(desc_label)

        spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.cart_btn = QPushButton()
        self.cart_btn.setIcon(QIcon(cart_icon_path))
        self.cart_btn.setIconSize(QSize(20, 20))
        self.cart_btn.setFixedSize(32, 32)
        self.cart_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 87, 34, 0.8);
                border: 1px solid rgba(255, 87, 34, 1);
                border-radius: 16px;
            }
            QPushButton:hover {
                background-color: rgba(255, 87, 34, 1);
            }
            QPushButton:pressed {
                background-color: rgba(255, 87, 34, 0.9);
            }
        """)
        self.cart_btn.setCursor(Qt.PointingHandCursor)
        self.cart_btn.clicked.connect(self.add_to_cart)
        buttons_layout.addWidget(self.cart_btn)

        self.info_btn = QPushButton()
        self.info_btn.setIcon(QIcon(info_icon_path))
        self.info_btn.setIconSize(QSize(20, 20))
        self.info_btn.setFixedSize(32, 32)
        self.info_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(33, 150, 243, 0.8);
                border: 1px solid rgba(33, 150, 243, 1);
                border-radius: 16px;
            }
            QPushButton:hover {
                background-color: rgba(33, 150, 243, 1);
            }
            QPushButton:pressed {
                background-color: rgba(33, 150, 243, 0.9);
            }
        """)
        self.info_btn.setCursor(Qt.PointingHandCursor)
        self.info_btn.clicked.connect(self.show_product_info)
        buttons_layout.addWidget(self.info_btn)

        buttons_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        main_layout.addLayout(buttons_layout)

    def handle_image_response(self, reply, image_label):
        try:
            if reply.error() == QNetworkReply.NoError:
                data = reply.readAll()
                pixmap = QPixmap()
                if pixmap.loadFromData(data) and not pixmap.isNull():
                    pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    image_label.setPixmap(pixmap)
                    image_label.setStyleSheet("")
                    print(f"Tải thành công hình ảnh từ {reply.url().toString()}")
                else:
                    print(f"Dữ liệu hình ảnh không hợp lệ từ {reply.url().toString()}")
                    self.set_default_placeholder(image_label)
            else:
                print(f"Lỗi tải hình ảnh từ {reply.url().toString()}: {reply.errorString()}")
                self.set_default_placeholder(image_label)
        except Exception as e:
            print(f"Lỗi xử lý phản hồi hình ảnh: {str(e)}")
            self.set_default_placeholder(image_label)
        finally:
            reply.deleteLater()

    def set_default_placeholder(self, image_label):
        pixmap = QPixmap(120, 120)
        pixmap.fill(Qt.transparent)
        image_label.setPixmap(pixmap)
        image_label.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            color: #B0BEC5;
            font-size: 12px;
            text-align: center;
        """)
        image_label.setText("Không có hình ảnh")

class ProductGridView(QWidget):
    def __init__(self):
        super(ProductGridView, self).__init__()
        self.setup_ui()
        self.current_row = 0
        self.current_col = 0
        self.max_cols = 3

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(20)
        self.grid_widget = QWidget()
        self.grid_widget.setLayout(self.grid_layout)
        self.grid_widget.setStyleSheet("background-color: transparent;")
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background-color: rgba(255, 255, 255, 0.1);
                width: 8px;
                margin: 0px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: rgba(255, 255, 255, 0.4);
                min-height: 30px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: rgba(255, 255, 255, 0.6);
            }
            QScrollBar::handle:vertical:pressed {
                background-color: rgba(255, 255, 255, 0.8);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        self.scroll_area.setWidget(self.grid_widget)
        self.main_layout.addWidget(self.scroll_area)

    def add_product_item(self, product_id, name, price, description, image_path=None):
        product_item = ProductItemView(product_id, name, price, description, image_path)
        self.grid_layout.addWidget(product_item, self.current_row, self.current_col)
        self.current_col += 1
        if self.current_col >= self.max_cols:
            self.current_col = 0
            self.current_row += 1

    def clear_products(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.current_row = 0
        self.current_col = 0

class ProductManagementView(QWidget):
    def __init__(self):
        super(ProductManagementView, self).__init__()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.product_grid = ProductGridView()
        main_layout.addWidget(self.product_grid)

    def add_product_item(self, product_id, name, price, description, image_path=None):
        self.product_grid.add_product_item(product_id, name, price, description, image_path)

    def clear_products(self):
        self.product_grid.clear_products()