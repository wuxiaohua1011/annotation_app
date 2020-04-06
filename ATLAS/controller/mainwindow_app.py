from PyQt5 import QtWidgets  # type: ignore
from PyQt5.QtWidgets import QApplication
from ATLAS.view.mainwindow_ui import Ui_MainWindow
from ATLAS.controller.atlas_annotation_tool_app import AtlasAnnotationAppWindow
from ATLAS.controller.download_tool_app import DownloadToolWindow
from ATLAS.config import DEFAULT_STYLE_SHEET_PATH
from ATLAS.controller.utilities.utility import BaseWindow
from typing import List
from pathlib import Path


class MainWindow(BaseWindow):
    def __init__(
        self,
        app: QApplication,
        style_sheet_location: Path = DEFAULT_STYLE_SHEET_PATH,
        **kwargs
    ):
        super().__init__(
            app=app, UI=Ui_MainWindow, style_sheet_location=style_sheet_location
        )
        self.dialogs: List = list()
        self.kwargs = kwargs

    def setListener(self):
        self.ui.btn_annotate.clicked.connect(self.btn_annotate_clicked)
        self.ui.btn_download_data.clicked.connect(self.btn_download_data_clicked)

    def btn_annotate_clicked(self):
        annotation_app = AtlasAnnotationAppWindow(self.app, **self.kwargs)
        self.dialogs.append(annotation_app)
        self.hide()
        annotation_app.show()
        annotation_app.closeEvent = self.app_close_event

    def btn_download_data_clicked(self):
        download_app = DownloadToolWindow(self.app)
        self.dialogs.append(download_app)
        self.hide()
        download_app.show()
        download_app.closeEvent = self.app_close_event

    # rewires annotation_app's closing event
    def app_close_event(self, close_event):
        self.show()
