# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_design/add_product_to_import.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        Form.setStyleSheet("#Form {\n"
"background: #F5F5F5;\n"
"border-bottom-radius : 10px;\n"
"border : 2px solid white ;\n"
"}")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 0, 801, 601))
        self.frame.setObjectName("frame")
        self.them_sua_label = QtWidgets.QLabel(self.frame)
        self.them_sua_label.setGeometry(QtCore.QRect(0, 0, 811, 61))
        self.them_sua_label.setMinimumSize(QtCore.QSize(811, 61))
        self.them_sua_label.setMaximumSize(QtCore.QSize(811, 61))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.them_sua_label.setFont(font)
        self.them_sua_label.setStyleSheet("QLabel {\n"
"    background-color:  rgba(40, 40, 40, 180); /* Nền xanh trong suốt */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
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
        self.them_sua_label.setText("")
        self.them_sua_label.setObjectName("them_sua_label")
        self.layoutWidget = QtWidgets.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(51, 91, 688, 479))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(66)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(101, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.line_id = QtWidgets.QLineEdit(self.layoutWidget)
        self.line_id.setMinimumSize(QtCore.QSize(271, 35))
        self.line_id.setStyleSheet("QLineEdit {\n"
"    background-color: #ffffff; /* Màu nền trắng */\n"
"    border: 1px solid #cccccc; /* Viền xám nhạt */\n"
"    border-radius: 15px; /* Bo góc */\n"
"    padding: 5px; /* Khoảng cách bên trong */\n"
"    font-size: 14px;\n"
"    color: #333333;\n"
"}\n"
"\n"
"/* Hiệu ứng khi ô nhập liệu được chọn */\n"
"QLineEdit:focus {\n"
"    border: 1px solid #4a90e2; /* Viền xanh khi focus */\n"
"    background-color: #e6f0fa; /* Nền xanh nhạt khi focus */\n"
"}")
        self.line_id.setObjectName("line_id")
        self.verticalLayout.addWidget(self.line_id)
        self.horizontalLayout_7.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(48, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setMinimumSize(QtCore.QSize(101, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_4.addWidget(self.label_5)
        self.line_unit = QtWidgets.QLineEdit(self.layoutWidget)
        self.line_unit.setMinimumSize(QtCore.QSize(120, 35))
        self.line_unit.setMaximumSize(QtCore.QSize(20000, 16777215))
        self.line_unit.setStyleSheet("QLineEdit {\n"
"    background-color: #ffffff; /* Màu nền trắng */\n"
"    border: 1px solid #cccccc; /* Viền xám nhạt */\n"
"    border-radius: 15px; /* Bo góc */\n"
"    padding: 5px; /* Khoảng cách bên trong */\n"
"    font-size: 14px;\n"
"    color: #333333;\n"
"}\n"
"\n"
"/* Hiệu ứng khi ô nhập liệu được chọn */\n"
"QLineEdit:focus {\n"
"    border: 1px solid #4a90e2; /* Viền xanh khi focus */\n"
"    background-color: #e6f0fa; /* Nền xanh nhạt khi focus */\n"
"}")
        self.line_unit.setObjectName("line_unit")
        self.verticalLayout_4.addWidget(self.line_unit)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        spacerItem1 = QtWidgets.QSpacerItem(48, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.label_6.setMinimumSize(QtCore.QSize(101, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_5.addWidget(self.label_6)
        self.line_soLuong = QtWidgets.QLineEdit(self.layoutWidget)
        self.line_soLuong.setMinimumSize(QtCore.QSize(120, 35))
        self.line_soLuong.setMaximumSize(QtCore.QSize(20000, 16777215))
        self.line_soLuong.setStyleSheet("QLineEdit {\n"
"    background-color: #ffffff; /* Màu nền trắng */\n"
"    border: 1px solid #cccccc; /* Viền xám nhạt */\n"
"    border-radius: 15px; /* Bo góc */\n"
"    padding: 5px; /* Khoảng cách bên trong */\n"
"    font-size: 14px;\n"
"    color: #333333;\n"
"}\n"
"\n"
"/* Hiệu ứng khi ô nhập liệu được chọn */\n"
"QLineEdit:focus {\n"
"    border: 1px solid #4a90e2; /* Viền xanh khi focus */\n"
"    background-color: #e6f0fa; /* Nền xanh nhạt khi focus */\n"
"}")
        self.line_soLuong.setObjectName("line_soLuong")
        self.verticalLayout_5.addWidget(self.line_soLuong)
        self.horizontalLayout_4.addLayout(self.verticalLayout_5)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_4)
        self.gridLayout.addLayout(self.horizontalLayout_7, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 38, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 6, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 18, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setMinimumSize(QtCore.QSize(101, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.line_name = QtWidgets.QLineEdit(self.layoutWidget)
        self.line_name.setMinimumSize(QtCore.QSize(271, 35))
        self.line_name.setStyleSheet("QLineEdit {\n"
"    background-color: #ffffff; /* Màu nền trắng */\n"
"    border: 1px solid #cccccc; /* Viền xám nhạt */\n"
"    border-radius: 15px; /* Bo góc */\n"
"    padding: 5px; /* Khoảng cách bên trong */\n"
"    font-size: 14px;\n"
"    color: #333333;\n"
"}\n"
"\n"
"/* Hiệu ứng khi ô nhập liệu được chọn */\n"
"QLineEdit:focus {\n"
"    border: 1px solid #4a90e2; /* Viền xanh khi focus */\n"
"    background-color: #e6f0fa; /* Nền xanh nhạt khi focus */\n"
"}")
        self.line_name.setObjectName("line_name")
        self.verticalLayout_2.addWidget(self.line_name)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        spacerItem4 = QtWidgets.QSpacerItem(108, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setMinimumSize(QtCore.QSize(131, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.combo_box_danhmuc = QtWidgets.QComboBox(self.layoutWidget)
        self.combo_box_danhmuc.setMinimumSize(QtCore.QSize(281, 35))
        self.combo_box_danhmuc.setStyleSheet("QComboBox {\n"
"    background-color: #ffffff; /* Màu nền trắng */\n"
"    border: 1px solid #cccccc; /* Viền xám nhạt */\n"
"    border-radius: 15px; /* Bo góc */\n"
"    padding: 5px; /* Khoảng cách bên trong */\n"
"    font-size: 14px;\n"
"    color: #333333;\n"
"}\n"
"\n"
"/* Hiệu ứng khi ô nhập liệu được chọn */\n"
"QComboBox:focus {\n"
"    border: 1px solid #4a90e2; /* Viền xanh khi focus */\n"
"    background-color: #e6f0fa; /* Nền xanh nhạt khi focus */\n"
"}")
        self.combo_box_danhmuc.setObjectName("combo_box_danhmuc")
        self.verticalLayout_3.addWidget(self.combo_box_danhmuc)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.them_btn = QtWidgets.QPushButton(self.layoutWidget)
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
        self.them_btn.setText("")
        self.them_btn.setObjectName("them_btn")
        self.horizontalLayout_2.addWidget(self.them_btn)
        self.huy_btn = QtWidgets.QPushButton(self.layoutWidget)
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
        self.horizontalLayout_2.addWidget(self.huy_btn)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_2)
        spacerItem5 = QtWidgets.QSpacerItem(508, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem5)
        self.gridLayout.addLayout(self.horizontalLayout_6, 7, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_8 = QtWidgets.QLabel(self.layoutWidget)
        self.label_8.setMinimumSize(QtCore.QSize(81, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_7.addWidget(self.label_8)
        self.line_gia_nhap = QtWidgets.QLineEdit(self.layoutWidget)
        self.line_gia_nhap.setMinimumSize(QtCore.QSize(271, 35))
        self.line_gia_nhap.setMaximumSize(QtCore.QSize(271, 16777215))
        self.line_gia_nhap.setStyleSheet("QLineEdit {\n"
"    background-color: #ffffff; /* Màu nền trắng */\n"
"    border: 1px solid #cccccc; /* Viền xám nhạt */\n"
"    border-radius: 15px; /* Bo góc */\n"
"    padding: 5px; /* Khoảng cách bên trong */\n"
"    font-size: 14px;\n"
"    color: #333333;\n"
"}\n"
"\n"
"/* Hiệu ứng khi ô nhập liệu được chọn */\n"
"QLineEdit:focus {\n"
"    border: 1px solid #4a90e2; /* Viền xanh khi focus */\n"
"    background-color: #e6f0fa; /* Nền xanh nhạt khi focus */\n"
"}")
        self.line_gia_nhap.setObjectName("line_gia_nhap")
        self.verticalLayout_7.addWidget(self.line_gia_nhap)
        self.horizontalLayout_5.addLayout(self.verticalLayout_7)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem6)
        self.gridLayout.addLayout(self.horizontalLayout_5, 5, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 18, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem7, 4, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "ID sản phẩm : "))
        self.line_id.setPlaceholderText(_translate("Form", "  ID Sản phẩm..."))
        self.label_5.setText(_translate("Form", "Đơn vị : "))
        self.line_unit.setPlaceholderText(_translate("Form", "Đơn vị..."))
        self.label_6.setText(_translate("Form", "Số lượng : "))
        self.line_soLuong.setPlaceholderText(_translate("Form", "Đơn vị..."))
        self.label_3.setText(_translate("Form", "Tên sản phẩm : "))
        self.line_name.setPlaceholderText(_translate("Form", "  Tên sản phẩm..."))
        self.label_4.setText(_translate("Form", "Danh mục sản phẩm : "))
        self.huy_btn.setText(_translate("Form", "Hủy"))
        self.label_8.setText(_translate("Form", "Giá nhập : "))
        self.line_gia_nhap.setPlaceholderText(_translate("Form", "  Đơn giá..."))
