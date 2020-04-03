# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'download_tool.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_download_tool(object):
    def setupUi(self, BrowseDialog):
        BrowseDialog.setObjectName("BrowseDialog")
        BrowseDialog.resize(402, 531)
        self.io_panel = QtWidgets.QTabWidget(BrowseDialog)
        self.io_panel.setGeometry(QtCore.QRect(0, 0, 401, 531))
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

        self.retranslateUi(BrowseDialog)
        self.io_panel.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(BrowseDialog)

    def retranslateUi(self, BrowseDialog):
        _translate = QtCore.QCoreApplication.translate
        BrowseDialog.setWindowTitle(_translate("BrowseDialog", "Dialog"))
        self.download_browse_btn.setText(_translate("BrowseDialog", "Browse"))
        self.download_confirm_btn.setText(_translate("BrowseDialog", "Download"))
        self.download_cancel_btn.setText(_translate("BrowseDialog", "Cancel"))
        self.io_panel.setTabText(
            self.io_panel.indexOf(self.Download), _translate("BrowseDialog", "Download")
        )
        self.label.setText(
            _translate(
                "BrowseDialog",
                '<html><head/><body><p><span style=" font-size:18pt; font-weight:600; ">Choose a file to upload</span></p></body></html>',
            )
        )
        self.upload_browse_btn.setText(_translate("BrowseDialog", "Browse"))
        self.upload_confirm_btn.setText(_translate("BrowseDialog", "Upload"))
        self.upload_cancel_btn.setText(_translate("BrowseDialog", "Cancel"))
        self.io_panel.setTabText(
            self.io_panel.indexOf(self.Upload), _translate("BrowseDialog", "Upload")
        )
