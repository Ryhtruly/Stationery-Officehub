import os

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTextEdit, QWidget, QSizePolicy)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QPixmap, QCursor


class AppInfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Thông tin ứng dụng")
        self.setMinimumSize(1000, 680)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.setAttribute(Qt.WA_TranslucentBackground, False)  # Tắt nền trong suốt
        self.setStyleSheet("""
            QDialog {
                background: #F5F7FA;  /* Trắng ngà sáng */
                border: 1px solid #D0D4D8;  /* Viền xám nhạt */
                border-radius: 10px;  /* Bo góc */
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);  /* Bóng đổ nhẹ */
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        header_layout = QHBoxLayout()

        logo_label = QLabel()
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        logo_path = os.path.join(base_dir, "employee", "ui", "ui_design", "icon", "SnapBG.ai_1747709355469.png")
        logo_pixmap = QPixmap(logo_path)
        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
        else:
            logo_label.setText("LOGO")
            logo_label.setStyleSheet("""
                font-size: 24px;
                font-weight: bold;
                color: #333333;  /* Đen xám đậm */
                background: #FFFFFF;  /* Nền trắng */
                border: 1px solid #E0E0E0;  /* Viền xám nhạt */
                border-radius: 8px;  /* Bo góc */
                box-shadow: 0 1px 5px rgba(0, 0, 0, 0.05);  /* Bóng đổ nhẹ */
            """)

        logo_label.setFixedSize(80, 80)
        logo_label.setAlignment(Qt.AlignCenter)
        if not logo_pixmap.isNull():
            logo_label.setStyleSheet("""
                background: #FFFFFF;  /* Nền trắng */
                border: 1px solid #E0E0E0;  /* Viền xám nhạt */
                border-radius: 8px;  /* Bo góc */
                box-shadow: 0 1px 5px rgba(0, 0, 0, 0.05);  /* Bóng đổ nhẹ */
            """)
        header_layout.addWidget(logo_label)

        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(20, 0, 0, 0)

        app_title = QLabel("OFFICEHUB")
        app_title.setFont(QFont('Arial', 18, QFont.Bold))
        app_title.setStyleSheet("""
            color: #333333;  /* Đen xám đậm */
            background: #FFFFFF;  /* Nền trắng */
            border: 1px solid #E0E0E0;  /* Viền xám nhạt */
            border-radius: 5px;  /* Bo góc */
            padding: 5px 10px;
            box-shadow: 0 1px 5px rgba(0, 0, 0, 0.05);  /* Bóng đổ nhẹ */
        """)

        app_subtitle = QLabel("CỬA HÀNG VĂN PHÒNG PHẨM THÔNG MINH - MỞ CỬA THÀNH CÔNG TỪ NHỮNG ĐIỀU NHỎ NHẤT")
        app_subtitle.setFont(QFont('Arial', 12))
        app_subtitle.setStyleSheet("""
            color: #555555;  /* Xám đậm nhẹ */
            background: #FFFFFF;  /* Nền trắng */
            border: 1px solid #E0E0E0;  /* Viền xám nhạt */
            border-radius: 5px;  /* Bo góc */
            padding: 5px 10px;
            box-shadow: 0 1px 5px rgba(0, 0, 0, 0.05);  /* Bóng đổ nhẹ */
        """)

        title_layout.addWidget(app_title)
        title_layout.addWidget(app_subtitle)

        header_layout.addWidget(title_container)
        header_layout.addStretch(1)

        main_layout.addLayout(header_layout)

        content_text = QTextEdit()
        content_text.setReadOnly(True)
        content_text.setStyleSheet("""
            QTextEdit {
                background: #FFFFFF;  /* Nền trắng */
                border: 1px solid #D0D4D8;  /* Viền xám nhạt */
                border-radius: 8px;  /* Bo góc */
                padding: 15px;
                font-size: 11pt;
                line-height: 1.5;
                color: #333333;  /* Đen xám đậm */
                box-shadow: 0 1px 5px rgba(0, 0, 0, 0.05);  /* Bóng đổ nhẹ */
            }
            QTextEdit QScrollBar:vertical {
                background: #F0F2F5;  /* Nền thanh cuộn xám nhạt */
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }
            QTextEdit QScrollBar::handle:vertical {
                background: #A0A4A8;  /* Xám đậm cho tay cầm */
                border-radius: 5px;
            }
            QTextEdit QScrollBar::handle:vertical:hover {
                background: #808488;  /* Xám đậm hơn khi hover */
            }
        """)

        content_text.setHtml("""
        <h2 style="color: #333333;">Chào mừng bạn đến với OfficeHub!</h2>

        <p style="text-align: justify;">Trong kỷ nguyên số hóa 4.0 hiện nay, khi mọi hoạt động đều được chuyển từ sổ sách sang các nền tảng kỹ thuật số, 
        OfficeHub ra đời với sứ mệnh mang đến giải pháp quản lý toàn diện cho cửa hàng văn phòng phẩm của bạn. 
        Chúng tôi hiểu rằng việc quản lý một cửa hàng văn phòng phẩm đòi hỏi sự tỉ mỉ, chính xác và hiệu quả, 
        đặc biệt là trong các thời điểm cao điểm như mùa tựu trường hay đầu năm học mới.</p>

        <p style="text-align: justify;">OfficeHub được thiết kế với giao diện thân thiện, dễ sử dụng, giúp bạn tiết kiệm thời gian và công sức 
        trong việc quản lý hàng hóa, theo dõi doanh thu và chăm sóc khách hàng. Không còn những rắc rối với sổ sách 
        giấy tờ hay lo lắng về việc tính toán sai sót, OfficeHub sẽ là người trợ lý đắc lực giúp bạn vận hành 
        cửa hàng một cách suôn sẻ và hiệu quả.</p>

        <h3>Tính năng nổi bật</h3>
        <ul>
            <li>  Quản lý sản phẩm thông minh:</b> Dễ dàng thêm, sửa, xóa và tìm kiếm sản phẩm</li>
            <li>  Theo dõi tồn kho thời gian thực:</b> Luôn nắm bắt chính xác số lượng hàng hóa</li>
            <li>  Xử lý đơn hàng nhanh chóng:</b> Tạo hóa đơn và thanh toán chỉ trong vài thao tác đơn giản</li>
            <li>  Chăm sóc khách hàng:</b> Lưu trữ thông tin khách hàng, tích điểm và áp dụng chương trình khuyến mãi</li>
            <li>  Báo cáo trực quan:</b> Xem báo cáo doanh thu </li>
            <li>  Xuất báo cáo:</b> Xuất báo cáo thống kê và hóa đơn dạng PDF </li>
            <li>  Quản lý nhân viên:</b> Phân quyền quản lí thông tin nhân viên</li>
        </ul>

        <h3>Danh mục sản phẩm</h3>
        <ul>
            <li>  Đồ dùng học tập:</b> Bút các loại, vở, tập, thước kẻ, compa, hộp bút, balo, cặp sách...</li>
            <li>  Văn phòng phẩm:</b> Giấy in, giấy photo, kẹp giấy, bìa hồ sơ, băng keo, bút dạ quang...</li>
            <li>  Thiết bị văn phòng:</b> Máy tính, máy in, máy scan, máy photocopy, máy hủy tài liệu...</li>
            <li>  Dụng cụ mỹ thuật:</b> Màu vẽ, cọ, giấy vẽ, tập tô màu, đất nặn, kéo nghệ thuật...</li>
        </ul>

        <h3>Cam kết của chúng tôi</h3>
        <p style="text-align: justify;">OfficeHub cam kết đồng hành cùng bạn trên hành trình phát triển kinh doanh. Chúng tôi liên tục cập nhật 
        và cải tiến ứng dụng để đáp ứng nhu cầu ngày càng cao của thị trường. Với OfficeHub, việc quản lý 
        cửa hàng văn phòng phẩm chưa bao giờ dễ dàng đến thế!</p>

        <p style="margin-top: 20px;"><b>Phiên bản:</b> 2.1.0</p>
        <p><b>Phát triển bởi:</b> Lê Hữu Trí, Nguyễn Minh Tú, Đỗ Xuân Trí</p>
        <p><b>© 2025</b> - Bản quyền thuộc về OfficeHub</p>
        <p>Học viện Công nghệ Bưu chính Viễn thông</p>
        """)

        main_layout.addWidget(content_text)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)

        close_btn = QPushButton("Đóng")
        close_btn.setIcon(QIcon("ui_design/icon/cancel-xxl.png"))
        close_btn.setIconSize(QSize(24, 24))
        close_btn.setFixedSize(100, 40)
        close_btn.setStyleSheet("""
            QPushButton {
                background: #FFFFFF;  /* Nền trắng */
                color: #333333;  /* Chữ đen xám */
                border: 1px solid #D0D4D8;  /* Viền xám nhạt */
                border-radius: 8px;  /* Bo góc */
                padding: 5px 15px;
                font-weight: bold;
                box-shadow: 0 1px 5px rgba(0, 0, 0, 0.05);  /* Bóng đổ nhẹ */
            }
            QPushButton:hover {
                background: #E6ECEF;  /* Xám nhạt khi hover */
                border: 1px solid #A0A4A8;  /* Viền đậm hơn */
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);  /* Bóng đổ rõ hơn */
            }
            QPushButton:pressed {
                background: #D0D4D8;  /* Xám nhạt hơn khi nhấn */
                border: 1px solid #808488;  /* Viền đậm */
                box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);  /* Hiệu ứng nhấn */
            }
        """)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.close)

        button_layout.addWidget(close_btn)
        main_layout.addLayout(button_layout)