from controller.config import DEFAULT_STYLE_SHEET_LOCATION, DEFAULT_SEGMENTATION_FILE_LOCATION, DEFAULT_SCENE_LOCATION
from PyQt5 import QtWidgets  # type: ignore
from PyQt5.QtWidgets import QApplication  # type: ignore
from view.planefitting_ui import Ui_planefitting_main_window
import sys
from controller.utilities.atlas_annotation_tool_util import Scene
from pathlib import Path


class PlaneFitting(QtWidgets.QMainWindow):
    def __init__(self,
                 app: QApplication, **kwargs):
        super().__init__()
        self.app = app
        self.ui = Ui_planefitting_main_window()
        self.ui.setupUi(self)
        if "style_sheet_location" in kwargs.keys():
            self.app.setStyleSheet(open(str(kwargs.get("style_sheet_location"))).read())
        else:
            self.app.setStyleSheet(open(DEFAULT_STYLE_SHEET_LOCATION.as_posix()).read())

        self.kwargs = kwargs
        self.scene_location: Path = kwargs.get("scene_location", DEFAULT_SCENE_LOCATION)

        self.scene = Scene()
        # demo
        self.scene.render_mesh(fname=self.scene_location.as_posix())


        self.setUpCanvas()
        self.setListener()
        self.show()

    def setUpCanvas(self):
        self.ui.data_display_window.addWidget(self.scene.native)

    def setListener(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PlaneFitting(app=app)
    app.exec_()