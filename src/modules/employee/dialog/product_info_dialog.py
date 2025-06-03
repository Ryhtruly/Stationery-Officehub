import requests
from io import BytesIO
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QScrollArea, QWidget, QSizePolicy, QSpacerItem)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QFont
import os

class ProductInfoDialog(QDialog):
    add_to_cart_signal = pyqtSignal()

    def __init__(self, product_data, parent=None):
        super().__init__(parent)
        self.product_data = product_data
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Thông tin sản phẩm")
        self.setMinimumSize(600, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setStyleSheet("background-color: #F5F5F5;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        content_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(20, 0, 0, 0)

        image_container = QWidget()
        image_container_layout = QHBoxLayout(image_container)
        image_container_layout.setContentsMargins(0, 0, 0, 0)

        image_label = QLabel()
        image_label.setFixedSize(200, 200)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setStyleSheet("background-color: transparent; border: none;")

        print("Dữ liệu sản phẩm:", self.product_data)

        possible_image_keys = ['hinh_anh', 'image_path', 'image', 'anh', 'hinhanh', 'img', 'url_image']
        image_path = None

        for key in possible_image_keys:
            if key in self.product_data and self.product_data[key]:
                image_path = self.product_data[key]
                print(f"Tìm thấy đường dẫn hình ảnh trong trường '{key}': {image_path}")
                break

        if image_path:
            print(f"Đang thử tải hình ảnh từ: {image_path}")

            # Kiểm tra nếu đường dẫn là URL
            if image_path.startswith('http'):
                try:
                    # Tải hình ảnh từ URL
                    response = requests.get(image_path, timeout=5)
                    if response.status_code == 200:
                        # Chuyển dữ liệu hình ảnh thành pixmap
                        img_data = BytesIO(response.content)
                        pixmap = QPixmap()
                        pixmap.loadFromData(img_data.read())

                        if not pixmap.isNull():
                            print("Tải hình ảnh từ URL thành công!")
                            pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                            image_label.setPixmap(pixmap)
                        else:
                            print("Không thể chuyển đổi dữ liệu thành hình ảnh")
                            image_label.setText("Lỗi hình ảnh")
                    else:
                        print(f"Không thể tải hình ảnh, mã lỗi: {response.status_code}")
                        image_label.setText("Lỗi tải ảnh")
                except Exception as e:
                    print(f"Lỗi khi tải hình ảnh từ URL: {e}")
                    image_label.setText("Lỗi kết nối")
            else:
                # Nếu là đường dẫn cục bộ
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    print("Tải hình ảnh cục bộ thành công!")
                    pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    image_label.setPixmap(pixmap)
                else:
                    print(f"Không thể tải hình ảnh từ đường dẫn cục bộ: {image_path}")
                    image_label.setText("Không tìm thấy ảnh")
        else:
            print("Không tìm thấy trường hình ảnh trong dữ liệu sản phẩm")
            image_label.setText("Không có ảnh")

        image_container_layout.addWidget(image_label)
        image_container_layout.addStretch()

        left_layout.addWidget(image_container)
        left_layout.addSpacing(30)

        # Tên sản phẩm (đặt dưới hình ảnh và căn lề trái)
        name_container = QWidget()
        name_layout = QHBoxLayout(name_container)
        name_layout.setContentsMargins(0, 0, 0, 0)

        product_name = QLabel(self.product_data.get('name', 'Tên sản phẩm'))
        product_name.setFont(QFont('Arial', 14, QFont.Bold))
        product_name.setStyleSheet("color: #333333; background-color: transparent; border: none;")  # Đảm bảo không có khung
        product_name.setWordWrap(True)
        product_name.setAlignment(Qt.AlignLeft)

        name_layout.addWidget(product_name)
        name_layout.addStretch()  # Thêm khoảng trống bên phải để căn lề trái

        left_layout.addWidget(name_container)

        # Thêm layout bên trái vào content_layout
        content_layout.addLayout(left_layout)

        # Thông tin sản phẩm (bên phải)
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(0, 0, 140, 0)

        # Giá
        price = self.product_data.get('price', 0)
        price_label = QLabel(f"Giá: {price:,.0f} đ")
        price_label.setFont(QFont('Arial', 14))
        price_label.setStyleSheet("color: #FF4500; font-weight: bold; background-color: transparent; border: none;")  # Đảm bảo không có khung
        price_label.setAlignment(Qt.AlignLeft)
        info_layout.addWidget(price_label)

        # Mô tả
        description = self.product_data.get('description', 'Không có mô tả')
        description_label = QLabel("Mô tả sản phẩm:")
        description_label.setFont(QFont('Arial', 12, QFont.Bold))
        description_label.setStyleSheet("color: #333333; background-color: transparent; border: none;")  # Đảm bảo không có khung
        description_label.setAlignment(Qt.AlignLeft)
        info_layout.addWidget(description_label)

        description_text = QLabel(description)
        description_text.setWordWrap(True)
        description_text.setFont(QFont('Arial', 11))
        description_text.setStyleSheet("background-color: transparent; color: #555555; border: none;")  # Bỏ khung: không nền, không bo góc
        description_text.setAlignment(Qt.AlignLeft)
        info_layout.addWidget(description_text)

        # Thêm các layout vào content_layout và main_layout
        content_layout.addLayout(info_layout)
        main_layout.addLayout(content_layout)

        # Thêm thông tin khác nếu có
        if 'category' in self.product_data:
            category_label = QLabel(f"Danh mục: {self.product_data['category']}")
            category_label.setFont(QFont('Arial', 11))
            category_label.setStyleSheet("color: #555555; background-color: transparent; border: none;")  # Đảm bảo không có khung
            info_layout.addWidget(category_label)

        if 'brand' in self.product_data:
            brand_label = QLabel(f"Thương hiệu: {self.product_data['brand']}")
            brand_label.setFont(QFont('Arial', 11))
            brand_label.setStyleSheet("color: #555555; background-color: transparent; border: none;")  # Đảm bảo không có khung
            info_layout.addWidget(brand_label)

        # Thêm khoảng trống co giãn
        info_layout.addStretch(1)

        content_layout.addLayout(info_layout)
        main_layout.addLayout(content_layout)

        # Nút thao tác
        button_layout = QHBoxLayout()

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        cart_icon_path = os.path.join(base_dir, "employee", "ui", "ui_design", "icon", "cart-59-xl.png")
        cancel_icon_path = os.path.join(base_dir, "employee", "ui", "ui_design", "icon", "cancel-xxl.png")

        # Nút thêm vào giỏ hàng
        add_to_cart_btn = QPushButton()
        add_to_cart_btn.setIcon(QIcon(cart_icon_path))
        add_to_cart_btn.setIconSize(QSize(24, 24))  # Tăng kích thước icon
        add_to_cart_btn.setFixedSize(40, 40)
        add_to_cart_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF5722;  /* Màu cam đậm */
                border: none;  /* Không viền */
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            QPushButton:hover {
                background-color: #FF7043;  /* Cam nhạt hơn khi hover */
            }
            QPushButton:pressed {
                background-color: #E64A19;  /* Cam đậm hơn khi nhấn */
            }
        """)
        add_to_cart_btn.setCursor(Qt.PointingHandCursor)
        add_to_cart_btn.clicked.connect(self.on_add_to_cart)

        # Nút đóng
        close_btn = QPushButton()
        close_btn.setIcon(QIcon(cancel_icon_path))
        close_btn.setIconSize(QSize(24, 24))
        close_btn.setFixedSize(40, 40)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #D3D3D3;  /* Xám nhạt */
                border: none;  /* Không viền */
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            QPushButton:hover {
                background-color: #C0C0C0;  /* Xám đậm hơn một chút khi hover */
            }
            QPushButton:pressed {
                background-color: #A9A9A9;  /* Xám đậm hơn khi nhấn */
            }
        """)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        spacer = QSpacerItem(20, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)  # 20px khoảng trống
        button_layout.addSpacerItem(spacer)
        button_layout.addWidget(add_to_cart_btn)
        button_layout.addWidget(close_btn)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

    def on_add_to_cart(self):
        # Phát tín hiệu để thêm sản phẩm vào giỏ hàng
        self.add_to_cart_signal.emit()
        self.close()