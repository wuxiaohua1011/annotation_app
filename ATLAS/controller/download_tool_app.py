import sys
import os

from ATLAS.view.downloadtool_ui import Ui_download_tool
from ATLAS.controller.utilities.endpoints import Atlas_api_fetcher
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtWidgets import QApplication


class DownloadToolWindow(QDialog):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.ui = Ui_download_tool()
        self.ui.setupUi(self)
        self.files = []
        self.message = []
        self.file_to_upload = ""
        self.fetcher = Atlas_api_fetcher()
        # set data location
        self.dataLoc = "/".join([os.getcwd(), "data"])
        # prepare for message box
        self.write_message("Current download directory: " + self.dataLoc)
        self.ui.download_progress.setValue(0)
        self.ui.upload_progress.setValue(0)
        self.setListener()
        self.populateFileList()
        self.show()

    def populateFileList(self):
        self.files.clear()
        self.ui.fileList.clear()
        all_files = self.fetcher.get_file_list()
        for file in all_files:
            self.files.append(file)
            self.ui.fileList.addItem(file)

    def setListener(self):
        self.ui.download_cancel_btn.clicked.connect(self.download_btn_cancel_clicked)
        self.ui.download_confirm_btn.clicked.connect(self.download_btn_confirm_clicked)
        self.ui.download_browse_btn.clicked.connect(self.download_btn_browse_clicked)
        self.ui.upload_cancel_btn.clicked.connect(self.upload_btn_cancel_clicked)
        self.ui.upload_confirm_btn.clicked.connect(self.upload_btn_confirm_clicked)
        self.ui.upload_browse_btn.clicked.connect(self.upload_btn_browse_clicked)

    def download_btn_cancel_clicked(self):
        pass

    def download_btn_confirm_clicked(self):
        item = self.ui.fileList.currentItem().text()
        self.fetcher.get_file(item, self.ui.download_progress, self.dataLoc)
        self.ui.download_progress.setValue(0)
        self.write_message("File downloaded: " + item)

    def download_btn_browse_clicked(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)

        if dialog.exec_():
            folder = dialog.selectedFiles()[0]

        self.dataLoc = folder
        self.write_message("Current download directory:" + folder)

    def upload_btn_cancel_clicked(self):
        self.change_update_file("")

    def upload_btn_confirm_clicked(self):
        if self.file_to_upload == "":
            self.write_message("No file is selected to be uploaded")
            return

        self.fetcher.upload_file(self.file_to_upload)
        suffix = self.file_to_upload.split("/")[-1]
        self.write_message("{} uploaded successfully".format(suffix))

    def upload_btn_browse_clicked(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)

        if dialog.exec_():
            filename = dialog.selectedFiles()[0]
            if filename != None:
                self.change_update_file(filename)

    def write_message(self, message):
        self.message.append(message)
        format_msg = "> {}\n".format(message)
        self.ui.download_msg_box.append(format_msg)
        self.ui.upload_msg_box.append(format_msg)

    def change_update_file(self, filename):
        self.file_to_upload = filename
        self.ui.upload_url.setText(filename)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = DownloadToolWindow(app)
    app.exec_()
