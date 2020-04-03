from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from ATLAS.config import DEFAULT_STYLE_SHEET_PATH
from pathlib import Path
from abc import abstractmethod


class BaseWindow(QtWidgets.QMainWindow):
    def __init__(self,
                 app: QApplication,
                 UI,
                 style_sheet_location: Path = DEFAULT_STYLE_SHEET_PATH,
                 show=True):
        """

        Args:
            app: QApplication
            UI: a callable that represents a class. ex: Ui_MainWindow in view/mainwindow_ui.py
            style_sheet_location: location of the style sheet
        """
        super().__init__()
        self.app = app
        self.ui = UI()
        try:
            self.ui.setupUi(self)
        except AttributeError as e:
            raise AttributeError("Given UI {} does not have setupUi function. Please see documentation".format(UI))
        self.app.setStyleSheet(open(str(style_sheet_location.as_posix())).read())

        self.setListener()
        if show:
            self.show()

    @abstractmethod
    def setListener(self):
        raise NotImplementedError
