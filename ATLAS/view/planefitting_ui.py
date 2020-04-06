# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'planefitting.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_planefitting_main_window(object):
    def setupUi(self, planefitting_main_window):
        planefitting_main_window.setObjectName("planefitting_main_window")
        planefitting_main_window.resize(732, 647)
        self.centralwidget = QtWidgets.QWidget(planefitting_main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_undo = QtWidgets.QPushButton(self.centralwidget)
        self.btn_undo.setObjectName("btn_undo")
        self.horizontalLayout_2.addWidget(self.btn_undo)
        self.btn_clip = QtWidgets.QPushButton(self.centralwidget)
        self.btn_clip.setObjectName("btn_clip")
        self.horizontalLayout_2.addWidget(self.btn_clip)
        self.btn_done = QtWidgets.QPushButton(self.centralwidget)
        self.btn_done.setObjectName("btn_done")
        self.horizontalLayout_2.addWidget(self.btn_done)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.curr_segment_dropdown = QtWidgets.QComboBox(self.centralwidget)
        self.curr_segment_dropdown.setMinimumSize(QtCore.QSize(200, 0))
        self.curr_segment_dropdown.setObjectName("curr_segment_dropdown")
        self.horizontalLayout.addWidget(self.curr_segment_dropdown)
        self.segment_list = QtWidgets.QListWidget(self.centralwidget)
        self.segment_list.setMinimumSize(QtCore.QSize(200, 0))
        self.segment_list.setMaximumSize(QtCore.QSize(300, 16777215))
        self.segment_list.setObjectName("segment_list")
        self.horizontalLayout.addWidget(self.segment_list)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.data_display_window = QtWidgets.QVBoxLayout()
        self.data_display_window.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.data_display_window.setObjectName("data_display_window")
        self.gridLayout.addLayout(self.data_display_window, 0, 0, 1, 1)
        self.message_center_text_edit = QtWidgets.QTextEdit(self.centralwidget)
        self.message_center_text_edit.setObjectName("message_center_text_edit")
        self.gridLayout.addWidget(self.message_center_text_edit, 1, 0, 1, 1)
        planefitting_main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(planefitting_main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 732, 22))
        self.menubar.setObjectName("menubar")
        planefitting_main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(planefitting_main_window)
        self.statusbar.setObjectName("statusbar")
        planefitting_main_window.setStatusBar(self.statusbar)

        self.retranslateUi(planefitting_main_window)
        QtCore.QMetaObject.connectSlotsByName(planefitting_main_window)

    def retranslateUi(self, planefitting_main_window):
        _translate = QtCore.QCoreApplication.translate
        planefitting_main_window.setWindowTitle(
            _translate("planefitting_main_window", "MainWindow")
        )
        self.btn_undo.setText(_translate("planefitting_main_window", "Undo"))
        self.btn_clip.setText(_translate("planefitting_main_window", "Clip"))
        self.btn_done.setText(_translate("planefitting_main_window", "Done"))
