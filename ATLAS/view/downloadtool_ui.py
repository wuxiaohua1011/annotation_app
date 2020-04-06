# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'download_tool.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore


class Ui_download_tool(object):
    def setupUi(self, download_tool):
        download_tool.setObjectName("download_tool")
        download_tool.resize(935, 681)
        self.centralwidget = QtWidgets.QWidget(download_tool)
        self.centralwidget.setObjectName("centralwidget")
        self.io_panel = QtWidgets.QTabWidget(self.centralwidget)
        self.io_panel.setGeometry(QtCore.QRect(220, 30, 401, 531))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.io_panel.sizePolicy().hasHeightForWidth())
        self.io_panel.setSizePolicy(sizePolicy)
        self.io_panel.setObjectName("io_panel")
        self.Download = QtWidgets.QWidget()
        self.Download.setObjectName("Download")
        self.fileList = QtWidgets.QListWidget(self.Download)
        self.fileList.setGeometry(QtCore.QRect(20, 0, 361, 331))
        self.fileList.setObjectName("fileList")
        self.download_browse_btn = QtWidgets.QPushButton(self.Download)
        self.download_browse_btn.setGeometry(QtCore.QRect(20, 460, 121, 32))
        self.download_browse_btn.setObjectName("download_browse_btn")
        self.download_confirm_btn = QtWidgets.QPushButton(self.Download)
        self.download_confirm_btn.setGeometry(QtCore.QRect(142, 460, 121, 32))
        self.download_confirm_btn.setObjectName("download_confirm_btn")
        self.download_cancel_btn = QtWidgets.QPushButton(self.Download)
        self.download_cancel_btn.setGeometry(QtCore.QRect(260, 460, 113, 32))
        self.download_cancel_btn.setObjectName("download_cancel_btn")
        self.download_progress = QtWidgets.QProgressBar(self.Download)
        self.download_progress.setGeometry(QtCore.QRect(20, 330, 361, 23))
        self.download_progress.setProperty("value", 24)
        self.download_progress.setObjectName("download_progress")
        self.download_msg_box = QtWidgets.QTextEdit(self.Download)
        self.download_msg_box.setGeometry(QtCore.QRect(20, 360, 361, 91))
        self.download_msg_box.setObjectName("download_msg_box")
        self.io_panel.addTab(self.Download, "")
        self.Upload = QtWidgets.QWidget()
        self.Upload.setObjectName("Upload")
        self.label = QtWidgets.QLabel(self.Upload)
        self.label.setGeometry(QtCore.QRect(20, 10, 311, 20))
        self.label.setObjectName("label")
        self.upload_progress = QtWidgets.QProgressBar(self.Upload)
        self.upload_progress.setGeometry(QtCore.QRect(20, 150, 361, 23))
        self.upload_progress.setProperty("value", 24)
        self.upload_progress.setObjectName("upload_progress")
        self.upload_url = QtWidgets.QLineEdit(self.Upload)
        self.upload_url.setGeometry(QtCore.QRect(30, 40, 341, 21))
        self.upload_url.setObjectName("upload_url")
        self.upload_browse_btn = QtWidgets.QPushButton(self.Upload)
        self.upload_browse_btn.setGeometry(QtCore.QRect(20, 70, 113, 32))
        self.upload_browse_btn.setObjectName("upload_browse_btn")
        self.upload_confirm_btn = QtWidgets.QPushButton(self.Upload)
        self.upload_confirm_btn.setGeometry(QtCore.QRect(140, 70, 113, 32))
        self.upload_confirm_btn.setObjectName("upload_confirm_btn")
        self.upload_cancel_btn = QtWidgets.QPushButton(self.Upload)
        self.upload_cancel_btn.setGeometry(QtCore.QRect(260, 70, 113, 32))
        self.upload_cancel_btn.setObjectName("upload_cancel_btn")
        self.upload_msg_box = QtWidgets.QTextEdit(self.Upload)
        self.upload_msg_box.setGeometry(QtCore.QRect(20, 180, 361, 301))
        self.upload_msg_box.setObjectName("upload_msg_box")
        self.io_panel.addTab(self.Upload, "")
        download_tool.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(download_tool)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 935, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        download_tool.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(download_tool)
        self.statusbar.setObjectName("statusbar")
        download_tool.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(download_tool)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(download_tool)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(download_tool)
        self.actionSave_As.setObjectName("actionSave_As")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(download_tool)
        self.io_panel.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(download_tool)

    def retranslateUi(self, download_tool):
        _translate = QtCore.QCoreApplication.translate
        download_tool.setWindowTitle(_translate("download_tool", "MainWindow"))
        self.download_browse_btn.setText(_translate("download_tool", "Browse"))
        self.download_confirm_btn.setText(_translate("download_tool", "Download"))
        self.download_cancel_btn.setText(_translate("download_tool", "Cancel"))
        self.io_panel.setTabText(
            self.io_panel.indexOf(self.Download),
            _translate("download_tool", "Download"),
        )
        self.label.setText(
            _translate(
                "download_tool",
                '<html><head/><body><p><span style=" font-size:18pt; font-weight:600; ">Choose a file to upload</span></p></body></html>',
            )
        )
        self.upload_browse_btn.setText(_translate("download_tool", "Browse"))
        self.upload_confirm_btn.setText(_translate("download_tool", "Upload"))
        self.upload_cancel_btn.setText(_translate("download_tool", "Cancel"))
        self.io_panel.setTabText(
            self.io_panel.indexOf(self.Upload), _translate("download_tool", "Upload")
        )
        self.menuFile.setTitle(_translate("download_tool", "File"))
        self.menuEdit.setTitle(_translate("download_tool", "Edit"))
        self.actionOpen.setText(_translate("download_tool", "Open"))
        self.actionSave.setText(_translate("download_tool", "Save"))
        self.actionSave_As.setText(_translate("download_tool", "Save As"))
