from controller.config import DEFAULT_STYLE_SHEET_LOCATION, DEFAULT_SEGMENTATION_FILE_LOCATION, \
    DEFAULT_SCENE_FILE_LOCATION
from PyQt5 import QtWidgets  # type: ignore
from PyQt5.QtWidgets import QApplication, QListWidgetItem # type: ignore
from view.planefitting_ui import Ui_planefitting_main_window
import sys
from controller.utilities.atlas_annotation_tool_util import Scene
from pathlib import Path
from typing import List
from controller.utilities.models import Segment
from controller.utilities.planefitting_utility import PlaneFittingUtil
from PyQt5 import QtCore

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
        self.scene_location: Path = kwargs.get("scene_location", DEFAULT_SCENE_FILE_LOCATION)
        self.segmentation_file_location = kwargs.get("segmentation_file_location", DEFAULT_SEGMENTATION_FILE_LOCATION)
        self.messages: List[str] = ["Program Started, UI Loaded"]  # list of strings
        self.segments: List[Segment] = []
        self.scene = Scene()

        self.plane_fitting = PlaneFittingUtil(scene_file_location=DEFAULT_SCENE_FILE_LOCATION)
        self.segments, base = self.plane_fitting.handle_json(
            segmentation_file_location=DEFAULT_SEGMENTATION_FILE_LOCATION)
        self.populateCurrSegmentDropDown()
        self.populateSegmentList()
        # demo
        self.scene.render_mesh(fname=self.scene_location.as_posix())

        self.setUpCanvas()
        self.setListener()
        self.show()

    def setUpCanvas(self):
        self.ui.data_display_window.addWidget(self.scene.native)

    def setListener(self):
        pass

    def populateCurrSegmentDropDown(self):
        self.ui.curr_segment_dropdown.clear()
        for seg in self.segments:
            self.ui.curr_segment_dropdown.addItem("ID: {} | {} ".format(seg.id, seg.segment_name))

    def populateSegmentList(self):
        self.ui.segment_list.clear()
        for seg in self.segments:
            check_box = QListWidgetItem()
            check_box.setText("ID: {} | {} ".format(seg.id, seg.segment_name))
            check_box.setFlags(check_box.flags() | QtCore.Qt.ItemIsUserCheckable)
            check_box.setCheckState(QtCore.Qt.Unchecked)
            self.ui.segment_list.addItem(check_box)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PlaneFitting(app=app)
    app.exec_()
