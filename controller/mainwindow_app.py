from PyQt5 import QtWidgets  # type: ignore
from view.MainWindow import Ui_MainWindow
from controller.atlas_annotation_tool_app import *
from controller.download_tool_app import DownloadToolWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app: QApplication, **kwargs):
        super().__init__()
        self.app = app
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        if "style_sheet_location" in kwargs.keys():
            self.app.setStyleSheet(open(str(kwargs.get("style_sheet_location"))).read())
        self.kwargs = kwargs

        self.setListener()
        self.dialogs: List = list()
        self.show()

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
        # self.dialogs[-1]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow(app)
    app.exec_()
