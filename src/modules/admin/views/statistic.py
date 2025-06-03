from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QDateEdit, QSizePolicy, QHeaderView,
    QScrollArea, QFrame, QComboBox, QGridLayout, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QFontDatabase
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import subprocess
import time
import sys
from src.modules.admin.events.event_handlers import update_statistics_event, export_report_event, update_chart, statistic_data_loader

class StatisticWindow(QWidget):
    """Cửa sổ thống kê doanh thu"""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        main_layout = QVBoxLayout(content_widget)

        scroll_area.setWidget(content_widget)

        base_layout = QVBoxLayout(self)

        self.setStyleSheet("""
            /* Nền tổng thể trong suốt */
            QWidget {
                background: transparent;
                border-radius: 10px;
            }

            /* ScrollArea */
            QScrollArea {
                background: transparent;
                border: none;
            }

            /* Label (Tiêu đề, nhãn) */
            QLabel {
                color: #333333; /* Xám đen đậm để nổi bật */
                font-family: "Arial";
                background: transparent;
                border: none;
                margin: 10px;
            }
            QLabel#title {
                font-size: 24px; /* Tăng kích thước chữ từ 20px lên 24px */
                font-weight: bold;
                color: #ffffff; /* Đổi màu thành trắng để nổi bật */
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); /* Thêm bóng chữ để nổi bật hơn */
            }
            QLabel#chartTitle, QLabel#tableLabel, QLabel#totalsTitle {
                font-size: 12px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            QLabel#totalQuantityLabel, QLabel#totalRevenueLabel, QLabel#totalCostLabel, QLabel#totalProfitLabel {
                padding: 5px;
            }

            /* QDateEdit */
            QDateEdit {
                background-color: rgba(40, 40, 40, 180);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                color: #ffffff;
            }
            QDateEdit::drop-down {
                border: none;
            }

            /* QComboBox */
            QComboBox {
                background-color: rgba(40, 40, 40, 180);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                color: #ffffff;
            }
            QComboBox::drop-down {
                border: none;
                color: #ffffff;
            }

            /* QFrame (Khung chứa biểu đồ và bảng) */
            QFrame {
                background: transparent;
                border: none;
                border-radius: 5px;
                margin: 10px 0;
            }

            /* Bo góc và nền cho QFrame bọc biểu đồ */
            QFrame#chartFrame {
                background-color: rgba(255, 255, 255, 0.9); /* Nền trắng nhẹ */
                border: 1px solid rgba(255, 255, 255, 0.2); /* Viền nhẹ */
                border-radius: 10px; /* Bo góc */
            }

            /* Tổng thể bảng với phong cách Glassmorphism */
            QTableWidget {
                background-color: rgba(40, 40, 40, 180); /* Nền đen mờ, tăng độ trong suốt */
                border: 1px solid rgba(255, 255, 255, 0.2); /* Viền trắng mờ nhẹ */
                border-radius: 10px; /* Bo góc mềm mại */
                color: #ffffff; /* Chữ trắng để nổi bật */
                font-family: "Arial", sans-serif;
                font-size: 14px;
                gridline-color: transparent;
            }

            /* Tiêu đề cột (header) */
            QHeaderView::section {
                background-color: rgba(30, 30, 30, 180); /* Nền header đen mờ hơn một chút */
                color: #ffffff;
                border: none;
                border-bottom: 1px solid rgba(255, 255, 255, 0.2);
                font-weight: bold;
                padding: 20px;
                min-height: 50px;
            }

            /* Hiệu ứng hover cho tiêu đề */
            QHeaderView::section:hover {
                background-color: rgba(0, 0, 0, 0.6); /* Sáng nhẹ khi hover */
                transition: background-color 0.3s ease; /* Hiệu ứng chuyển màu mượt */
            }

            /* Các ô trong bảng */
            QTableWidget::item {
                padding: 10px; /* Tăng padding để chữ không bị cắt */
                min-height: 40px; /* Đảm bảo chiều cao tối thiểu để hiển thị chữ */
                border: none;
                background-color: transparent;
                word-wrap: break-word; /* Nội dung dài sẽ tự động xuống dòng */
            }

            /* Hiệu ứng khi chọn ô */
            QTableWidget::item:selected {
                background-color: rgba(66, 165, 245, 0.4); /* Màu xanh dương mờ khi chọn */
                color: #ffffff;
            }

            /* Hiệu ứng hover cho ô */
            QTableWidget::item:hover {
                background-color: rgba(255, 255, 255, 0.1); /* Sáng nhẹ khi rê chuột */
                transition: background-color 0.3s ease; /* Chuyển màu mượt mà */
            }

            /* Thanh cuộn dọc */
            QScrollBar:vertical {
                background: rgba(0, 0, 0, 0.3); /* Nền đen mờ hơn */
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }

            QScrollBar::handle:vertical {
                background: linear-gradient(to bottom, rgba(66, 165, 245, 0.6), rgba(30, 136, 229, 0.6)); /* Gradient xanh dương mờ */
                border-radius: 5px;
            }

            QScrollBar::handle:vertical:hover {
                background: linear-gradient(to bottom, rgba(100, 181, 246, 0.7), rgba(66, 165, 245, 0.7)); /* Sáng hơn khi hover */
                transition: background 0.3s ease;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                background: none;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }

            /* Thanh cuộn ngang */
            QScrollBar:horizontal {
                background: rgba(0, 0, 0, 0.3); /* Nền đen mờ hơn */
                height: 10px;
                margin: 0px;
                border-radius: 5px;
            }

            QScrollBar::handle:horizontal {
                background: linear-gradient(to right, rgba(66, 165, 245, 0.6), rgba(30, 136, 229, 0.6)); /* Gradient xanh dương mờ */
                border-radius: 5px;
            }

            QScrollBar::handle:horizontal:hover {
                background: linear-gradient(to right, rgba(100, 181, 246, 0.7), rgba(66, 165, 245, 0.7)); /* Sáng hơn khi hover */
                transition: background 0.3s ease;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                background: none;
            }

            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {
                background: none;
            }

            /* Nút (QPushButton) */
            QPushButton {
                background-color: #4a90e2;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 14px;
                font-family: "Arial";
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)

        base_layout.addWidget(scroll_area)
        base_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("THỐNG KẾ", self)
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(title)

        date_layout = QHBoxLayout()

        # Chọn từ ngày
        from_date_label = QLabel("Từ ngày:", self)
        self.from_date = QDateEdit(self)
        self.from_date.setCalendarPopup(True)
        self.from_date.setDate(QDate.currentDate().addDays(-30))
        self.from_date.setDisplayFormat("dd-MM-yyyy")

        # Chọn đến ngày
        to_date_label = QLabel("Đến ngày:", self)
        self.to_date = QDateEdit(self)
        self.to_date.setCalendarPopup(True)
        self.to_date.setDate(QDate.currentDate())
        self.to_date.setDisplayFormat("dd-MM-yyyy")

        # Nút cập nhật
        update_btn = QPushButton("Cập nhật", self)
        update_btn.clicked.connect(lambda: update_statistics_event(self))

        date_layout.addWidget(from_date_label)
        date_layout.addWidget(self.from_date)
        date_layout.addWidget(to_date_label)
        date_layout.addWidget(self.to_date)
        date_layout.addWidget(update_btn)
        date_layout.addStretch()

        main_layout.addLayout(date_layout)

        chart_type_layout = QHBoxLayout()
        chart_type_label = QLabel("Loại biểu đồ:", self)
        self.chart_type_combo = QComboBox(self)
        self.chart_type_combo.addItems(["Cột", "Đường", "Vùng"])
        self.chart_type_combo.setCurrentIndex(0)
        self.chart_type_combo.currentIndexChanged.connect(lambda: update_statistics_event(self))

        chart_type_layout.addWidget(chart_type_label)
        chart_type_layout.addWidget(self.chart_type_combo)
        chart_type_layout.addStretch()
        main_layout.addLayout(chart_type_layout)

        self.figure = Figure(figsize=(10, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.setMinimumHeight(500)

        chart_container = QFrame()
        chart_container.setFrameShape(QFrame.StyledPanel)
        chart_container.setObjectName("chartFrame")

        chart_title = QLabel("BIỂU ĐỒ DOANH THU THEO NGÀY", self)
        chart_title.setObjectName("chartTitle")
        chart_title.setAlignment(Qt.AlignCenter)
        chart_title.setFont(QFont("Arial", 12, QFont.Bold))

        self.chart_layout = QVBoxLayout(chart_container)
        self.chart_layout.addWidget(chart_title)
        self.chart_layout.addWidget(self.canvas)

        main_layout.addWidget(chart_container)

        table_container = QFrame()
        table_container.setFrameShape(QFrame.StyledPanel)
        table_layout = QVBoxLayout(table_container)

        table_label = QLabel("CHI TIẾT SẢN PHẨM", self)
        table_label.setObjectName("tableLabel")
        table_label.setFont(QFont("Arial", 12, QFont.Bold))
        table_label.setAlignment(Qt.AlignCenter)
        table_layout.addWidget(table_label)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Tên sản phẩm", "Số lượng", "Tổng thu nhập", "Tổng vốn", "Lợi nhuận"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(False)

        self.table.setMinimumHeight(300)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.table.horizontalHeader().setMinimumHeight(60)

        table_layout.addWidget(self.table)
        main_layout.addWidget(table_container)

        totals_frame = QFrame()
        totals_frame.setFrameShape(QFrame.StyledPanel)
        totals_layout = QVBoxLayout(totals_frame)

        totals_title = QLabel("TỔNG KẾT", self)
        totals_title.setObjectName("totalsTitle")
        totals_title.setFont(QFont("Arial", 12, QFont.Bold))
        totals_title.setAlignment(Qt.AlignCenter)
        totals_layout.addWidget(totals_title)

        totals_info_layout = QGridLayout()

        self.total_quantity_label = QLabel("Tổng số lượng: 0")
        self.total_quantity_label.setObjectName("totalQuantityLabel")
        self.total_revenue_label = QLabel("Tổng doanh thu: 0 VNĐ")
        self.total_revenue_label.setObjectName("totalRevenueLabel")
        self.total_cost_label = QLabel("Tổng vốn: 0 VNĐ")
        self.total_cost_label.setObjectName("totalCostLabel")
        self.total_profit_label = QLabel("Tổng lợi nhuận: 0 VNĐ")
        self.total_profit_label.setObjectName("totalProfitLabel")

        for label in [self.total_quantity_label, self.total_revenue_label, self.total_cost_label,
                      self.total_profit_label]:
            label.setFont(QFont("Arial", 10, QFont.Bold))
            label.setAlignment(Qt.AlignLeft)

        totals_info_layout.addWidget(self.total_quantity_label, 0, 0)
        totals_info_layout.addWidget(self.total_revenue_label, 0, 1)
        totals_info_layout.addWidget(self.total_cost_label, 1, 0)
        totals_info_layout.addWidget(self.total_profit_label, 1, 1)

        totals_layout.addLayout(totals_info_layout)
        main_layout.addWidget(totals_frame)

        export_btn = QPushButton("Xuất báo cáo", self)
        export_btn.clicked.connect(lambda: self.export_report_event())
        export_btn.setMinimumWidth(150)

        export_layout = QHBoxLayout()
        export_layout.addStretch()
        export_layout.addWidget(export_btn)
        main_layout.addLayout(export_layout)

        main_layout.addStretch()

        from_date_str = self.from_date.date().toString("dd-MM-yyyy")
        to_date_str = self.to_date.date().toString("dd-MM-yyyy")
        update_chart(self, from_date_str, to_date_str)
        statistic_data_loader.load_data_to_statistic_table(self.table, from_date_str, to_date_str)

    def update_statistics(self):
        """Cập nhật dữ liệu thống kê"""
        update_statistics_event(self)

    def export_report_event(self):
        """Xuất báo cáo thống kê dưới dạng PDF với định dạng đẹp và kiểm tra lỗi"""
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Lưu báo cáo", "", "PDF Files (*.pdf);;All Files (*)"
        )
        if not file_name:
            return

        if not file_name.endswith('.pdf'):
            file_name += '.pdf'

        try:
            with open(file_name, 'wb') as f:
                pass
            os.remove(file_name)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể ghi file PDF: {e}")
            return

        temp_chart_file = "temp_chart.png"
        try:
            self.figure.savefig(temp_chart_file, dpi=300, bbox_inches='tight', format='png')
            if not os.path.exists(temp_chart_file) or os.path.getsize(temp_chart_file) == 0:
                QMessageBox.critical(self, "Lỗi", "Không thể tạo file biểu đồ tạm thời hoặc file rỗng.")
                return
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi lưu biểu đồ: {e}")
            return

        if self.table.rowCount() == 0:
            QMessageBox.critical(self, "Lỗi", "Không có dữ liệu trong bảng.")
            return

        try:
            pdfmetrics.registerFont(TTFont('TimesNewRoman', 'C:/Windows/Fonts/times.ttf'))
        except Exception as e:
            QMessageBox.warning(self, "Cảnh báo", f"Không thể tải font Times New Roman: {e}. Sử dụng font mặc định.")
            font_family = "Helvetica"
        else:
            font_family = "TimesNewRoman"

        # Tạo PDF bằng reportlab
        c = canvas.Canvas(file_name, pagesize=A4)
        width, height = A4  # Kích thước trang A4 (mm)

        # Định nghĩa khoảng cách và tọa độ
        margin = 20 * mm
        section_spacing = 10 * mm
        line_spacing = 5 * mm
        y = height - margin  # Bắt đầu từ trên cùng của trang

        # --- Vẽ tiêu đề báo cáo ---
        c.setFont(font_family, 24)
        c.setFillColorRGB(0, 0.2, 0.4)  # Màu xanh đậm
        c.drawCentredString(width / 2, y, "BÁO CÁO THỐNG KẾ DOANH THU")
        y -= 30 * mm  # Khoảng cách lớn hơn sau tiêu đề

        # --- Vẽ đường kẻ ngang phân cách ---
        c.setLineWidth(0.5 * mm)
        c.setStrokeColorRGB(0.8, 0.8, 0.8)  # Màu xám nhạt
        c.line(margin, y, width - margin, y)
        y -= section_spacing

        # --- Vẽ khoảng thời gian ---
        c.setFont(font_family, 12)
        c.setFillColorRGB(0, 0, 0)  # Màu đen
        from_date_str = self.from_date.date().toString("dd-MM-yyyy")
        to_date_str = self.to_date.date().toString("dd-MM-yyyy")
        time_range = f"Từ ngày: {from_date_str} - Đến ngày: {to_date_str}"
        c.drawString(margin, y, time_range)
        y -= 20 * mm  # Khoảng cách sau thời gian

        # --- Vẽ biểu đồ ---
        c.setFont(font_family, 16)
        c.setFillColorRGB(0, 0.2, 0.4)
        c.drawCentredString(width / 2, y, "Biểu đồ doanh thu theo ngày")
        y -= 15 * mm

        try:
            chart_width = (width - 2 * margin)  # Chiều rộng biểu đồ
            chart_height = 80 * mm  # Chiều cao biểu đồ
            c.drawImage(temp_chart_file, margin, y - chart_height, width=chart_width, height=chart_height)
            y -= chart_height + section_spacing
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi vẽ biểu đồ vào PDF: {e}")
            if os.path.exists(temp_chart_file):
                os.remove(temp_chart_file)
            return

        # --- Vẽ đường kẻ ngang phân cách trước bảng ---
        c.setLineWidth(0.5 * mm)
        c.line(margin, y, width - margin, y)
        y -= section_spacing

        # --- Vẽ bảng dữ liệu ---
        c.setFont(font_family, 16)
        c.setFillColorRGB(0, 0.2, 0.4)
        c.drawCentredString(width / 2, y, "Chi tiết sản phẩm")
        y -= 15 * mm

        # Chuẩn bị dữ liệu bảng
        headers = ["ID", "Tên sản phẩm", "Số lượng", "Tổng thu nhập", "Tổng vốn", "Lợi nhuận"]
        data = [headers]
        row_count = self.table.rowCount()
        for row in range(row_count):
            row_data = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                text = item.text() if item else ""
                row_data.append(text)
            data.append(row_data)

        # Vẽ bảng
        col_widths = [20 * mm, 50 * mm, 30 * mm, 30 * mm, 30 * mm, 30 * mm]  # Chiều rộng cột
        table_height = (len(data) * 10 * mm)  # Ước tính chiều cao bảng
        if y - table_height < 50 * mm:  # Kiểm tra nếu bảng vượt quá trang
            c.showPage()
            y = height - margin
            c.setFont(font_family, 16)
            c.setFillColorRGB(0, 0.2, 0.4)
            c.drawCentredString(width / 2, y, "Chi tiết sản phẩm")
            y -= 15 * mm

        # Vẽ header của bảng
        c.setFont(font_family, 12)
        c.setFillColorRGB(0, 0, 0)
        x_pos = margin
        for col, (header, width) in enumerate(zip(headers, col_widths)):
            c.rect(x_pos, y - 10 * mm, width, 10 * mm, fill=1)
            c.setFillColorRGB(1, 1, 1)  # Màu trắng cho chữ trong header
            c.drawString(x_pos + 2 * mm, y - 8 * mm, header)
            c.setFillColorRGB(0, 0, 0)  # Đặt lại màu đen cho các phần sau
            x_pos += width

        y -= 10 * mm

        # Vẽ dữ liệu bảng
        for row in range(row_count):
            x_pos = margin
            for col, width in enumerate(col_widths):
                text = data[row + 1][col]  # +1 để bỏ qua header
                c.rect(x_pos, y - 10 * mm, width, 10 * mm, fill=0)
                c.drawString(x_pos + 2 * mm, y - 8 * mm, text)
                x_pos += width
            y -= 10 * mm

            # Kiểm tra nếu vượt trang
            if y < 50 * mm:
                c.showPage()
                y = height - margin
                # Vẽ lại header trên trang mới
                x_pos = margin
                c.setFont(font_family, 12)
                c.setFillColorRGB(0, 0, 0)
                for col, (header, width) in enumerate(zip(headers, col_widths)):
                    c.rect(x_pos, y - 10 * mm, width, 10 * mm, fill=1)
                    c.setFillColorRGB(1, 1, 1)
                    c.drawString(x_pos + 2 * mm, y - 8 * mm, header)
                    c.setFillColorRGB(0, 0, 0)
                    x_pos += width
                y -= 10 * mm

        y -= section_spacing

        # --- Vẽ đường kẻ ngang phân cách trước phần tổng kết ---
        c.setLineWidth(0.5 * mm)
        c.line(margin, y, width - margin, y)
        y -= section_spacing

        # --- Vẽ thông tin tổng kết ---
        c.setFont(font_family, 16)
        c.setFillColorRGB(0, 0.2, 0.4)
        c.drawCentredString(width / 2, y, "Tổng kết")
        y -= 15 * mm

        # Vẽ khung tổng kết
        totals_height = 40 * mm
        if y - totals_height < 50 * mm:
            c.showPage()
            y = height - margin

        c.setLineWidth(0.2 * mm)
        c.setFillColorRGB(0.94, 0.96, 1.0)  # Màu nền khung tổng kết
        c.rect(margin, y - totals_height, width - 2 * margin, totals_height, fill=1, stroke=1)
        c.setFillColorRGB(0, 0, 0)

        # Vẽ nội dung tổng kết
        c.setFont(font_family, 12)
        y_totals = y - 5 * mm
        for text in [
            self.total_quantity_label.text(),
            self.total_revenue_label.text(),
            self.total_cost_label.text(),
            self.total_profit_label.text()
        ]:
            c.drawString(margin + 5 * mm, y_totals - 5 * mm, text)
            y_totals -= line_spacing

        y -= totals_height + section_spacing

        # --- Vẽ đường kẻ ngang phân cách trước footer ---
        c.setLineWidth(0.5 * mm)
        c.line(margin, y, width - margin, y)

        # --- Thêm footer ---
        c.setFont(font_family, 10)
        c.setFillColorRGB(0.39, 0.39, 0.39)  # Màu xám
        footer_text = f"Báo cáo được tạo vào {QDate.currentDate().toString('dd-MM-yyyy')}"
        c.drawString(margin, 30 * mm, footer_text)
        page_number = f"Trang 1"
        c.drawRightString(width - margin, 30 * mm, page_number)

        # Hoàn tất PDF
        c.showPage()
        c.save()

        # Xóa file PNG tạm thời
        if os.path.exists(temp_chart_file):
            try:
                os.remove(temp_chart_file)
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi khi xóa file tạm: {e}")

        # Kiểm tra file PDF đã được tạo thành công
        if not os.path.exists(file_name) or os.path.getsize(file_name) == 0:
            QMessageBox.critical(self, "Lỗi", f"File PDF không được tạo hoặc bị hỏng: {file_name}")
            return

        # Mở file PDF (đặc biệt tối ưu cho Windows)
        try:
            time.sleep(0.5)  # Đợi để đảm bảo file được ghi hoàn tất
            if os.path.exists(file_name):
                if os.name == 'nt':  # Windows
                    os.startfile(file_name)
                else:
                    QMessageBox.warning(self, "Cảnh báo", "Hệ điều hành không phải Windows, không thể mở file PDF bằng os.startfile.")
                QMessageBox.information(self, "Thành công", f"Báo cáo đã được xuất và mở tại: {file_name}")
            else:
                QMessageBox.critical(self, "Lỗi", f"File PDF không tồn tại tại: {file_name}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể mở file PDF: {e}")

    def resizeEvent(self, event):
        """Xử lý sự kiện thay đổi kích thước cửa sổ"""
        super().resizeEvent(event)
        # Cập nhật lại biểu đồ khi thay đổi kích thước
        from_date = self.from_date.date().toString("dd-MM-yyyy")
        to_date = self.to_date.date().toString("dd-MM-yyyy")
        update_chart(self, from_date, to_date)