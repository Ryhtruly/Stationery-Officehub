from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QFrame, QHBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QDate
from src.database.DAO.common.BillDAO import BillDAO
from src.database.DAO.common.BillDetailDAO import BillDetailDAO
from src.database.DAO.admin.ProductAdminDAO import ProductDAO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import subprocess
import time
import sys

class BillDetailDialog(QDialog):
    def __init__(self, bill_id, parent=None):
        super(BillDetailDialog, self).__init__(parent)
        print(f"Khởi tạo BillDetailDialog cho bill_id: {bill_id}")  # Log
        self.setWindowTitle("Chi tiết hóa đơn")
        self.setMinimumSize(600, 750)
        self.bill_id = bill_id
        self.setStyleSheet("background-color: white;")

        self.layout = QVBoxLayout(self)
        print("Đã tạo QVBoxLayout")  # Log

        self.create_header()

        self.add_separator()

        print("Khởi tạo total_label trước khi load thông tin hóa đơn")  # Log
        self.total_label = QLabel("Tổng tiền: Đang tải...")
        self.total_label.setStyleSheet("""
            font-family: 'Times New Roman';
            font-size: 14px;
            font-weight: bold;
            color: #FF0000;
            padding: 5px;
        """)
        self.load_bill_info()

        self.add_separator()

        # Bảng chi tiết hóa đơn
        print("Bắt đầu khởi tạo QTableWidget")  # Log
        self.detail_table = QTableWidget()
        print("Đã khởi tạo QTableWidget")  # Log
        self.detail_table.setColumnCount(5)
        print("Đã đặt số cột cho QTableWidget: 5")  # Log
        self.detail_table.setHorizontalHeaderLabels(["Tên sản phẩm", "Số lượng", "Giá", "Giảm giá (%)", "Thành tiền"])
        print("Đã đặt tiêu đề cột cho QTableWidget")  # Log
        self.detail_table.setColumnWidth(0, 200)  # Tên sản phẩm
        self.detail_table.setColumnWidth(1, 80)   # Số lượng
        self.detail_table.setColumnWidth(2, 80)   # Giá
        self.detail_table.setColumnWidth(3, 80)   # Giảm giá
        self.detail_table.setColumnWidth(4, 100)  # Thành tiền
        print("Đã đặt kích thước cột thủ công cho QTableWidget")  # Log
        self.detail_table.horizontalHeader().setStretchLastSection(True)
        self.detail_table.verticalHeader().setVisible(False)
        self.detail_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #000000;
                font-family: 'Times New Roman';
                font-size: 11px;
            }
            QTableWidget::item {
                padding: 3px;
            }
            QHeaderView::section {
                background-color: #E0E0E0;
                font-weight: bold;
                font-size: 12px;
                padding: 5px;
                border: 1px solid #000000;
            }
            QTableWidget::item {
                border: 1px solid #D3D3D3;
            }
        """)
        self.layout.addWidget(self.detail_table)
        print("Đã thêm QTableWidget vào layout")
        self.load_bill_details()
        self.add_separator()
        print("Hiển thị total_label sau bảng chi tiết hóa đơn")  # Log
        self.layout.addWidget(self.total_label, alignment=Qt.AlignRight)
        self.add_separator()

        thank_you_label = QLabel("Cảm ơn quý khách đã mua hàng tại OFFICEHUB - Hẹn gặp lại!")
        thank_you_label.setStyleSheet("""
            font-family: 'Times New Roman';
            font-size: 12px;
            color: #333333;
            padding: 10px;
        """)
        thank_you_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(thank_you_label)
        print("Đã thêm dòng 'Cảm ơn quý khách đã mua hàng'")  # Log

        button_layout = QHBoxLayout()

        # Nút "Đóng"
        print("Bắt đầu khởi tạo nút Đóng")  # Log
        self.close_button = QPushButton("Đóng")
        print("Đã khởi tạo nút Đóng")  # Log
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.close_button.clicked.connect(self.accept)
        print("Đã kết nối sự kiện clicked cho nút Đóng")  # Log
        button_layout.addWidget(self.close_button)

        # Nút "Xuất hóa đơn"
        print("Bắt đầu khởi tạo nút Xuất hóa đơn")  # Log
        self.export_button = QPushButton("Xuất hóa đơn")
        print("Đã khởi tạo nút Xuất hóa đơn")  # Log
        self.export_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.export_button.clicked.connect(self.export_to_pdf)
        print("Đã kết nối sự kiện clicked cho nút Xuất hóa đơn")  # Log
        button_layout.addWidget(self.export_button)

        self.layout.addLayout(button_layout)
        print("Đã thêm layout nút vào layout chính")  # Log

    def create_header(self):
        """Tạo tiêu đề hóa đơn"""
        header_label = QLabel("OFFICEHUB - HÓA ĐƠN BÁN HÀNG")
        header_label.setStyleSheet("""
            font-family: 'Arial';
            font-size: 20px;
            font-weight: bold;
            color: #000000;
            padding: 10px;
        """)
        header_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(header_label)
        print("Đã tạo tiêu đề hóa đơn")  # Log

    def add_separator(self):
        """Thêm đường kẻ phân cách"""
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("""
            QFrame {
                border: none;
                border-top: 1px dashed #D3D3D3;
            }
        """)
        self.layout.addWidget(separator)
        print("Đã thêm đường kẻ phân cách")  # Log

    def safe_str(self, value):
        """Chuyển đổi giá trị thành chuỗi an toàn để hiển thị"""
        if value is None:
            return ""
        try:
            str_value = str(value)
            return str_value.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"Lỗi xử lý chuỗi: {value}, lỗi: {str(e)}")
            return str(value)

    def format_currency(self, value):
        """Định dạng tiền tệ với dấu phẩy ngăn cách hàng nghìn"""
        try:
            return f"{float(value):,.0f} VNĐ"
        except (ValueError, TypeError) as e:
            print(f"Lỗi định dạng tiền tệ: {value}, lỗi: {str(e)}")
            return "0 VNĐ"

    def load_bill_info(self):
        """Hiển thị thông tin hóa đơn"""
        print(f"Loading bill info for bill_id: {self.bill_id}")  # Log
        bill_dao = BillDAO()
        bill = bill_dao.get_bill_by_id(self.bill_id)

        self.bill_info = bill

        if bill:
            print(f"Bill info loaded: {bill}")  # Log
            try:
                print("Hiển thị ID Hóa đơn")  # Log
                id_label = QLabel(f"ID Hóa đơn: {self.safe_str(bill['id_bill'])}")
                id_label.setStyleSheet("""
                    font-family: 'Times New Roman';
                    font-size: 12px;
                    color: #333333;
                    margin: 2px 0;
                """)
                self.layout.addWidget(id_label)

                print("Hiển thị Ngày")  # Log
                date_label = QLabel(f"Ngày: {bill['date'].strftime('%Y-%m-%d %H:%M:%S') if bill['date'] else ''}")
                date_label.setStyleSheet("""
                    font-family: 'Times New Roman';
                    font-size: 12px;
                    color: #333333;
                    margin: 2px 0;
                """)
                self.layout.addWidget(date_label)

                print("Hiển thị Nhân viên")  # Log
                emp_label = QLabel(f"Nhân viên: {self.safe_str(bill['employee_name'])}")
                emp_label.setStyleSheet("""
                    font-family: 'Times New Roman';
                    font-size: 12px;
                    color: #333333;
                    margin: 2px 0;
                """)
                self.layout.addWidget(emp_label)

                print("Hiển thị Khách hàng")  # Log
                cust_label = QLabel(f"Khách hàng: {self.safe_str(bill['customer_name'])}")
                cust_label.setStyleSheet("""
                    font-family: 'Times New Roman';
                    font-size: 12px;
                    color: #333333;
                    margin: 2px 0;
                """)
                self.layout.addWidget(cust_label)

                print("Hiển thị Tổng tiền")
                total = bill.get('total', 0)
                print(f"Tổng tiền từ cơ sở dữ liệu: {total}")
                self.total_label.setText(f"Tổng tiền: {self.format_currency(total)}")
                print("Hoàn tất hiển thị thông tin hóa đơn")
            except Exception as e:
                print(f"Lỗi khi hiển thị thông tin hóa đơn: {str(e)}")
                error_label = QLabel("Lỗi khi hiển thị thông tin hóa đơn.")
                error_label.setStyleSheet("""
                    font-family: 'Times New Roman';
                    font-size: 12px;
                    color: #FF0000;
                    margin: 2px 0;
                """)
                self.layout.addWidget(error_label)
                self.total_label.setText("Tổng tiền: 0 VNĐ")  # Đặt giá trị mặc định nếu lỗi
        else:
            print(f"Không tìm thấy hóa đơn với id_bill: {self.bill_id}")  # Log
            error_label = QLabel("Không tìm thấy thông tin hóa đơn.")
            error_label.setStyleSheet("""
                font-family: 'Times New Roman';
                font-size: 12px;
                color: #FF0000;
                margin: 2px 0;
            """)
            self.layout.addWidget(error_label)
            self.total_label.setText("Tổng tiền: 0 VNĐ")

    def load_bill_details(self):
        """Hiển thị chi tiết hóa đơn"""
        print(f"Loading bill details for bill_id: {self.bill_id}")  # Log
        bill_detail_dao = BillDetailDAO()
        product_dao = ProductDAO()

        # Load chi tiết hóa đơn
        try:
            print("Bắt đầu lấy chi tiết hóa đơn")  # Log
            details = bill_detail_dao.get_bill_details(self.bill_id)
            print(f"Chi tiết hóa đơn trả về: {details}")  # Log chi tiết
            if details is None or not isinstance(details, list) or not details:
                print(f"Không tìm thấy chi tiết hóa đơn cho bill_id: {self.bill_id}")
                self.detail_table.setRowCount(0)
                no_data_label = QLabel("Không có chi tiết hóa đơn.")
                no_data_label.setStyleSheet("""
                    font-family: 'Times New Roman';
                    font-size: 12px;
                    color: #FF0000;
                    margin: 2px 0;
                """)
                self.layout.addWidget(no_data_label)
                return
            print(f"Số lượng chi tiết hóa đơn: {len(details)}")  # Log số lượng
        except Exception as e:
            print(f"Lỗi khi lấy chi tiết hóa đơn: {str(e)}")
            self.detail_table.setRowCount(0)
            error_label = QLabel("Lỗi khi lấy chi tiết hóa đơn.")
            error_label.setStyleSheet("""
                font-family: 'Times New Roman';
                font-size: 12px;
                color: #FF0000;
                margin: 2px 0;
            """)
            self.layout.addWidget(error_label)
            return

        # Lưu chi tiết hóa đơn để sử dụng khi xuất PDF
        self.bill_details = details

        # Xóa các dòng cũ trong bảng trước khi thêm mới
        print("Bắt đầu xóa các dòng cũ trong QTableWidget")  # Log
        self.detail_table.setRowCount(0)
        print("Đã xóa các dòng cũ trong QTableWidget")  # Log

        # Thêm các dòng chi tiết hóa đơn vào bảng
        for detail in details:
            print(f"Processing detail: {detail}")
            try:
                # Kiểm tra dữ liệu chi tiết
                if not isinstance(detail, dict):
                    print(f"Dữ liệu chi tiết không hợp lệ: {detail}")
                    continue

                # Kiểm tra các trường cần thiết
                required_fields = ['id_prod', 'quantity', 'price', 'discount']
                if not all(field in detail for field in required_fields):
                    print(f"Thiếu trường cần thiết trong detail: {detail}")
                    continue

                # Lấy tên sản phẩm trực tiếp từ ProductDAO
                print(f"Bắt đầu lấy tên sản phẩm cho id_prod: {detail['id_prod']}")  # Log
                product_name = product_dao.get_product_name_by_id(detail['id_prod'])
                print(f"Tên sản phẩm với id_prod {detail['id_prod']}: {product_name}")  # Log

                quantity = detail['quantity']
                price = detail['price']
                print(f"Giá sản phẩm từ Bill_detail (id_prod: {detail['id_prod']}): {price}")  # Log giá sản phẩm
                if price == 0:
                    print(f"Cảnh báo: Giá sản phẩm cho id_prod {detail['id_prod']} là 0. Kiểm tra dữ liệu trong bảng Products hoặc Bill_detail.")
                discount = detail['discount'] if detail['discount'] is not None else 0
                discount_percent = discount * 100  # Chuyển đổi từ phần trăm
                subtotal = quantity * price * (1 - discount)

                print(f"Thêm dòng mới vào QTableWidget, row_position: {self.detail_table.rowCount()}")  # Log
                row_position = self.detail_table.rowCount()
                self.detail_table.insertRow(row_position)
                print(f"Đã thêm dòng mới vào QTableWidget tại row_position: {row_position}")  # Log

                # Hiển thị dữ liệu vào bảng
                print(f"Hiển thị Tên sản phẩm: {product_name}")  # Log
                safe_product_name = self.safe_str(product_name)
                self.detail_table.setItem(row_position, 0, QTableWidgetItem(safe_product_name))
                print(f"Hiển thị Số lượng: {quantity}")  # Log
                self.detail_table.setItem(row_position, 1, QTableWidgetItem(str(quantity)))
                print(f"Hiển thị Giá: {self.format_currency(price)}")  # Log
                self.detail_table.setItem(row_position, 2, QTableWidgetItem(self.format_currency(price)))
                print(f"Hiển thị Giảm giá: {discount_percent}%")  # Log
                self.detail_table.setItem(row_position, 3, QTableWidgetItem(f"{discount_percent:.0f}%"))
                print(f"Hiển thị Thành tiền: {self.format_currency(subtotal)}")  # Log
                self.detail_table.setItem(row_position, 4, QTableWidgetItem(self.format_currency(subtotal)))
                print(f"Hoàn tất hiển thị chi tiết hóa đơn tại row_position: {row_position}")  # Log
            except Exception as e:
                print(f"Lỗi khi hiển thị chi tiết hóa đơn tại row_position {row_position}: {str(e)}")
                self.detail_table.setItem(row_position, 0, QTableWidgetItem("Lỗi hiển thị"))

    def export_to_pdf(self):
        """Xuất hóa đơn ra file PDF"""
        # Mở hộp thoại để chọn nơi lưu file PDF
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Lưu hóa đơn", "", "PDF Files (*.pdf);;All Files (*)"
        )
        if not file_name:
            return  # Người dùng hủy thao tác

        if not file_name.endswith('.pdf'):
            file_name += '.pdf'

        # Kiểm tra quyền ghi file
        try:
            with open(file_name, 'wb') as f:
                pass  # Chỉ kiểm tra quyền ghi
            os.remove(file_name)  # Xóa file kiểm tra để tránh xung đột
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể ghi file PDF: {e}")
            return

        # Sử dụng reportlab để tạo PDF
        try:
            # Đăng ký font hỗ trợ tiếng Việt
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

        # --- Vẽ tiêu đề hóa đơn ---
        c.setFont(font_family, 20)
        c.setFillColorRGB(0, 0, 0)  # Màu đen
        c.drawCentredString(width / 2, y, "OFFICEHUB - HÓA ĐƠN BÁN HÀNG")
        y -= 30 * mm  # Khoảng cách lớn hơn sau tiêu đề

        # --- Vẽ đường kẻ ngang phân cách ---
        c.setLineWidth(0.5 * mm)
        c.setStrokeColorRGB(0.82, 0.82, 0.82)  # Màu xám nhạt
        c.line(margin, y, width - margin, y)
        y -= section_spacing

        # --- Vẽ thông tin hóa đơn ---
        c.setFont(font_family, 12)
        c.setFillColorRGB(0.2, 0.2, 0.2)  # Màu xám đậm
        bill_info = self.bill_info
        if bill_info:
            c.drawString(margin, y, f"ID Hóa đơn: {self.safe_str(bill_info['id_bill'])}")
            y -= line_spacing
            c.drawString(margin, y, f"Ngày: {bill_info['date'].strftime('%Y-%m-%d %H:%M:%S') if bill_info['date'] else ''}")
            y -= line_spacing
            c.drawString(margin, y, f"Nhân viên: {self.safe_str(bill_info['employee_name'])}")
            y -= line_spacing
            c.drawString(margin, y, f"Khách hàng: {self.safe_str(bill_info['customer_name'])}")
            y -= 20 * mm  # Khoảng cách sau thông tin hóa đơn
        else:
            c.drawString(margin, y, "Không tìm thấy thông tin hóa đơn.")
            y -= 20 * mm

        # --- Vẽ đường kẻ ngang phân cách ---
        c.setLineWidth(0.5 * mm)
        c.line(margin, y, width - margin, y)
        y -= section_spacing

        # --- Vẽ bảng chi tiết hóa đơn ---
        c.setFont(font_family, 16)
        c.setFillColorRGB(0, 0.2, 0.4)  # Màu xanh đậm
        c.drawCentredString(width / 2, y, "Chi tiết hóa đơn")
        y -= 15 * mm

        # Chuẩn bị dữ liệu bảng
        headers = ["Tên sản phẩm", "Số lượng", "Giá", "Giảm giá (%)", "Thành tiền"]
        data = [headers]

        # Tính toán tổng tiền từ chi tiết hóa đơn
        calculated_total = 0
        for detail in self.bill_details:
            product_dao = ProductDAO()
            product_name = product_dao.get_product_name_by_id(detail['id_prod'])
            quantity = detail['quantity']
            price = detail['price']
            print(f"Giá sản phẩm từ Bill_detail (id_prod: {detail['id_prod']}): {price}")  # Log giá sản phẩm
            if price == 0:
                print(f"Cảnh báo: Giá sản phẩm cho id_prod {detail['id_prod']} là 0. Kiểm tra dữ liệu trong bảng Products hoặc Bill_detail.")
            discount = detail['discount'] if detail['discount'] is not None else 0
            discount_percent = discount * 100  # Chuyển đổi từ phần trăm
            subtotal = quantity * price * (1 - discount)
            calculated_total += subtotal
            data.append([
                self.safe_str(product_name),
                str(quantity),
                self.format_currency(price),
                f"{discount_percent:.0f}%",
                self.format_currency(subtotal)
            ])

        # So sánh tổng tiền tính toán với tổng tiền từ cơ sở dữ liệu
        bill_total = self.bill_info.get('total', 0) if self.bill_info else 0
        print(f"Tổng tiền từ cơ sở dữ liệu (bill['total']): {bill_total}")  # Log tổng tiền từ cơ sở dữ liệu
        print(f"Tổng tiền tính toán từ chi tiết: {calculated_total}")  # Log tổng tiền tính toán
        if bill_total == 0 and calculated_total == 0:
            QMessageBox.warning(
                self, "Cảnh báo",
                "Tổng tiền từ hóa đơn và chi tiết đều là 0. Vui lòng kiểm tra dữ liệu trong bảng Bill và Bill_detail."
            )
            total_to_display = 0
        elif bill_total == 0 and calculated_total > 0:
            print("Tổng tiền từ cơ sở dữ liệu là 0, sử dụng tổng tiền tính toán từ chi tiết.")
            total_to_display = calculated_total
        else:
            total_to_display = bill_total  # Sử dụng tổng tiền từ hóa đơn
            if abs(calculated_total - bill_total) > 0.01:  # Cho phép sai số nhỏ
                QMessageBox.warning(
                    self, "Cảnh báo",
                    f"Tổng tiền tính toán từ chi tiết ({self.format_currency(calculated_total)}) không khớp với tổng tiền trong hóa đơn ({self.format_currency(bill_total)}). Sẽ sử dụng tổng tiền từ hóa đơn."
                )

        # Vẽ bảng
        col_widths = [50 * mm, 20 * mm, 30 * mm, 20 * mm, 30 * mm]  # Chiều rộng cột
        table_height = (len(data) * 10 * mm)  # Ước tính chiều cao bảng
        if y - table_height < 50 * mm:  # Kiểm tra nếu bảng vượt quá trang
            c.showPage()
            y = height - margin
            c.setFont(font_family, 16)
            c.setFillColorRGB(0, 0.2, 0.4)
            c.drawCentredString(width / 2, y, "Chi tiết hóa đơn")
            y -= 15 * mm

        # Vẽ header của bảng
        c.setFont(font_family, 12)
        c.setFillColorRGB(0, 0, 0)
        x_pos = margin
        for col, (header, width) in enumerate(zip(headers, col_widths)):
            c.setFillColorRGB(0.88, 0.88, 0.88)  # Màu nền header
            c.rect(x_pos, y - 10 * mm, width, 10 * mm, fill=1)
            c.setFillColorRGB(0, 0, 0)  # Màu đen cho chữ
            c.drawString(x_pos + 2 * mm, y - 8 * mm, header)
            x_pos += width

        y -= 10 * mm

        # Vẽ dữ liệu bảng
        for row in range(len(self.bill_details)):
            x_pos = margin
            for col, width in enumerate(col_widths):
                text = data[row + 1][col]  # +1 để bỏ qua header
                c.setFillColorRGB(1, 1, 1)  # Màu nền trắng
                c.rect(x_pos, y - 10 * mm, width, 10 * mm, fill=1, stroke=1)
                c.setFillColorRGB(0, 0, 0)  # Màu đen cho chữ
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
                    c.setFillColorRGB(0.88, 0.88, 0.88)
                    c.rect(x_pos, y - 10 * mm, width, 10 * mm, fill=1)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(x_pos + 2 * mm, y - 8 * mm, header)
                    x_pos += width
                y -= 10 * mm

        y -= section_spacing

        # --- Vẽ đường kẻ ngang phân cách ---
        c.setLineWidth(0.5 * mm)
        c.line(margin, y, width - margin, y)
        y -= section_spacing

        # --- Vẽ tổng tiền ---
        c.setFont(font_family, 14)
        c.setFillColorRGB(1, 0, 0)
        total_text = f"Tổng tiền: {self.format_currency(total_to_display)}"
        print(f"Hiển thị tổng tiền trong PDF: {total_text}")
        text_width = c.stringWidth(total_text, font_family, 14)
        padding_left = -120 * mm
        x_position = width - margin - text_width - padding_left
        c.drawString(x_position, y, total_text)
        y -= 20 * mm

        # --- Vẽ đường kẻ ngang phân cách ---
        c.setLineWidth(0.5 * mm)
        c.line(margin, y, width - margin, y)
        y -= section_spacing

        # --- Vẽ dòng "Cảm ơn quý khách" ---
        c.setFont(font_family, 12)
        c.setFillColorRGB(0.2, 0.2, 0.2)
        padding_left = -90 * mm  # Thêm khoảng đệm 5mm để không sát lề phải
        x_position = width - margin - text_width - padding_left  # Điều chỉnh vị trí
        c.drawString(x_position, y, "Cảm ơn quý khách đã mua hàng tại OFFICEHUB - Hẹn gặp lại!")
        y -= 20 * mm

        # --- Vẽ số trang ---
        c.setFont(font_family, 10)
        c.setFillColorRGB(0.39, 0.39, 0.39)  # Màu xám
        page_number = "Trang 1"
        c.drawRightString(width - margin, 30 * mm, page_number)

        # Hoàn tất PDF
        c.showPage()
        c.save()

        # Kiểm tra file PDF đã được tạo thành công
        if not os.path.exists(file_name) or os.path.getsize(file_name) == 0:
            QMessageBox.critical(self, "Lỗi", f"File PDF không được tạo hoặc bị hỏng: {file_name}")
            return

        # Mở file PDF
        try:
            time.sleep(0.5)  # Đợi để đảm bảo file được ghi hoàn tất
            if os.path.exists(file_name):
                if os.name == 'nt':  # Windows
                    os.startfile(file_name)
                else:
                    QMessageBox.warning(self, "Cảnh báo", "Hệ điều hành không phải Windows, không thể mở file PDF bằng os.startfile.")
                QMessageBox.information(self, "Thành công", f"Hóa đơn đã được xuất và mở tại: {file_name}")
            else:
                QMessageBox.critical(self, "Lỗi", f"File PDF không tồn tại tại: {file_name}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể mở file PDF: {e}")