# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_design/inventory_adjust.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(655, 392)
        Form.setStyleSheet("#Form {\n"
"background: #F5F5F5;\n"
"border-bottom-radius : 10px;\n"
"border : 2px solid white ;\n"
"}")
        self.cbb_ten_san_pham = QtWidgets.QComboBox(Form)
        self.cbb_ten_san_pham.setGeometry(QtCore.QRect(40, 140, 261, 41))
        self.cbb_ten_san_pham.setMinimumSize(QtCore.QSize(261, 31))
        self.cbb_ten_san_pham.setMaximumSize(QtCore.QSize(261, 41))
        self.cbb_ten_san_pham.setStyleSheet("QComboBox {\n"
"    color: black;\n"
"    font-family: \"Segoe UI\", \"Montserrat\", sans-serif;\n"
"    font-size: 16px;\n"
"    padding: 6px 12px;\n"
"    border: 3px solid gray;\n"
"    border-radius: 10px;\n"
"    background-color: rgba(255, 255, 255, 0.05);\n"
"    backdrop-filter: blur(10px);\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: rgba(255, 255, 255, 0.1);\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 30px;\n"
"    border-left: 1px solid rgba(255, 255, 255, 0.2);\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/icons/down_arrow_white.png); /* thay bằng icon phù hợp */\n"
"    width: 12px;\n"
"    height: 12px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: rgba(255, 255, 255, 0.08);\n"
"    border: 1px solid rgba(255, 255, 255, 0.2);\n"
"    border-radius: 8px;\n"
"    selection-background-color: rgba(255, 255, 255, 0.2);\n"
"    color: rgba(255, 255, 255, 0.95);\n"
"}\n"
"")
        self.cbb_ten_san_pham.setObjectName("cbb_ten_san_pham")
        self.label_15 = QtWidgets.QLabel(Form)
        self.label_15.setGeometry(QtCore.QRect(30, 80, 172, 45))
        self.label_15.setMaximumSize(QtCore.QSize(172, 45))
        self.label_15.setStyleSheet("QLabel {\n"
"    color: rgba(50, 50, 50, 0.85); /* Màu chữ đậm nhưng hơi trong suốt */\n"
"    font-family: \"Segoe UI\", \"Roboto\", sans-serif; /* Font hiện đại */\n"
"    font-weight: 500; /* Độ đậm vừa phải */\n"
"    font-size: 18px; /* Kích thước phù hợp */\n"
"    padding: 10px;\n"
"    letter-spacing: 0.3px; /* Tăng khoảng cách chữ nhẹ */\n"
"    \n"
"    text-align: center;\n"
"    background-color: rgba(255, 255, 255, 0.1); /* Nền trắng trong suốt */\n"
"    border-radius: 6px; /* Bo góc */\n"
"    backdrop-filter: blur(5px); /* Hiệu ứng blur đặc trưng của glassmorphism */\n"
"    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.07); /* Đổ bóng tinh tế */\n"
"\n"
"}\n"
"")
        self.label_15.setObjectName("label_15")
        self.line_so_luong = QtWidgets.QLineEdit(Form)
        self.line_so_luong.setGeometry(QtCore.QRect(340, 140, 287, 36))
        self.line_so_luong.setMinimumSize(QtCore.QSize(131, 31))
        self.line_so_luong.setStyleSheet("QLineEdit {\n"
"    background-color: rgba(255, 255, 255, 0.15); /* Nền trắng trong suốt */\n"
"    color: rgba(50, 50, 50, 0.9); /* Màu chữ đậm nhưng hơi trong suốt */\n"
"    border: 2px solid rgba(255, 255, 255, 0.9); /* Viền trắng trong suốt */\n"
"    border-radius: 17px; /* Bo góc lớn hơn cho hiệu ứng hiện đại */\n"
"    padding: 7px 6px; /* Thêm padding để trông thoáng hơn */\n"
"    backdrop-filter: blur(10px); /* Hiệu ứng blur đặc trưng của glassmorphism */\n"
"    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05); /* Đổ bóng tinh tế */\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 1px solid rgba(200, 200, 255, 0.5); /* Viền sáng hơn khi hover */\n"
"    background-color: rgba(255, 255, 255, 0.25); /* Nền sáng hơn khi hover */\n"
"    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08); /* Đổ bóng rõ hơn khi hover */\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1.5px solid rgba(120, 170, 255, 0.6); /* Viền xanh nhạt khi focus */\n"
"    background-color: rgba(255, 255, 255, 0.3); /* Nền sáng hơn khi focus */\n"
"    box-shadow: 0 4px 20px rgba(100, 150, 255, 0.15); /* Đổ bóng xanh nhạt khi focus */\n"
"}\n"
"")
        self.line_so_luong.setObjectName("line_so_luong")
        self.them_sua_label = QtWidgets.QLabel(Form)
        self.them_sua_label.setGeometry(QtCore.QRect(0, 0, 661, 45))
        self.them_sua_label.setMinimumSize(QtCore.QSize(0, 0))
        self.them_sua_label.setStyleSheet("QLabel {\n"
"    background-color:  rgba(40, 40, 40, 180); /* Nền xanh trong suốt */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    font-size: 12px;\n"
" font-family: \"Segoe UI\", \"Roboto\", sans-serif;\n"
"\n"
"    padding: 8px 16px;\n"
"    \n"
"    /* Viền sáng */\n"
"    border: 1.5px solid rgba(255, 255, 255, 0.4);\n"
"    \n"
"    /* Đổ bóng - QSS hỗ trợ giới hạn */\n"
"    border-style: outset;\n"
"    border-width: 1px;\n"
"    \n"
"    /* Gradient xanh */\n"
"}\n"
"\n"
"")
        self.them_sua_label.setObjectName("them_sua_label")
        self.them_btn = QtWidgets.QPushButton(Form)
        self.them_btn.setGeometry(QtCore.QRect(420, 270, 80, 40))
        self.them_btn.setMinimumSize(QtCore.QSize(80, 40))
        self.them_btn.setStyleSheet("QPushButton {\n"
"    background-color:  rgba(30, 170, 255, 0.7); /* Nền xanh trong suốt */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    border-radius: 16px;\n"
"    padding: 8px 16px;\n"
"    \n"
"    /* Viền sáng */\n"
"    border: 1.5px solid rgba(255, 255, 255, 0.4);\n"
"    \n"
"    /* Đổ bóng - QSS hỗ trợ giới hạn */\n"
"    border-style: outset;\n"
"    border-width: 1px;\n"
"    \n"
"    /* Gradient xanh */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(30, 170, 255, 0.5); /* Xanh sáng hơn khi hover */\n"
"    border: 1.5px solid rgba(255, 255, 255, 0.6);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(0, 120, 200, 0.4);\n"
"    border: 1.5px solid rgba(255, 255, 255, 0.3);\n"
"    padding-top: 9px; /* Tạo hiệu ứng nhấn xuống */\n"
"    padding-left: 17px;\n"
"}\n"
"")
        self.them_btn.setObjectName("them_btn")
        self.huy_btn = QtWidgets.QPushButton(Form)
        self.huy_btn.setGeometry(QtCore.QRect(530, 270, 80, 40))
        self.huy_btn.setMinimumSize(QtCore.QSize(80, 40))
        self.huy_btn.setStyleSheet("#huy_btn {\n"
"    background-color: white;\n"
"    color: black;\n"
"    border: 1px solid #d9d9d9;\n"
"    font-family: Arial, sans-serif;\n"
"    font-size: 12px;\n"
"    border-radius: 10px;\n"
"    padding: 5px 15px; /* Khoảng cách trong nút */\n"
"}\n"
"\n"
"/* Hover effect */\n"
"#huy_btn:hover {\n"
"    background-color: #f5f5f5;  /* Nhẹ hơn để tạo hiệu ứng phản hồi */\n"
"    border: 1px solid #a0a0a0;  /* Viền đậm hơn một chút khi hover */\n"
"    color: black;\n"
"}\n"
"")
        self.huy_btn.setObjectName("huy_btn")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_15.setText(_translate("Form", "Chọn sản phẩm : "))
        self.line_so_luong.setPlaceholderText(_translate("Form", "Số lượng.."))
        self.them_sua_label.setText(_translate("Form", " CHỈNH SỬA SỐ LƯỢNG TỒN KHO"))
        self.them_btn.setText(_translate("Form", "Lưu "))
        self.huy_btn.setText(_translate("Form", "Hủy"))
