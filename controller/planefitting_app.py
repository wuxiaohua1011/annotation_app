from controller.config import DEFAULT_STYLE_SHEET_PATH, DEFAULT_SEGMENTATION_FILE_PATH, \
    DEFAULT_SCENE_FILE_PATH
from PyQt5 import QtWidgets  # type: ignore
from PyQt5.QtWidgets import QApplication, QListWidgetItem  # type: ignore
from view.planefitting_ui import Ui_planefitting_main_window
import sys
from controller.utilities.atlas_annotation_tool_util import Scene
from pathlib import Path
from typing import List, Tuple
from controller.utilities.models import Segment
from controller.utilities.planefitting_utility_2 import *
from PyQt5 import QtCore
import open3d as o3d


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
            self.app.setStyleSheet(open(DEFAULT_STYLE_SHEET_PATH.as_posix()).read())
        self.kwargs = kwargs
        self.scene_file_path: Path = kwargs.get("scene_file_path", DEFAULT_SCENE_FILE_PATH)
        self.segmentation_file_path = kwargs.get("segmentation_file_path", DEFAULT_SEGMENTATION_FILE_PATH)
        self.scene = Scene()
        self.plane_fitting_util = PlaneFittingUtil(pcd=DEFAULT_SCENE_FILE_PATH)
        self.segments, self.oriented_boundingbox, self.pcd = \
            self.plane_fitting_util.auto_clip_segments(segments=self.segmentation_file_path)
        self.populateCurrSegmentDropDown()
        self.populateSegmentList()

        self.setUpCanvas()
        self.setListener()

        self.show()

    def setUpCanvas(self):
        self.ui.data_display_window.addWidget(self.scene.native)
        curr_text = self.ui.curr_segment_dropdown.currentText()
        self.onCurrSegmentDropdownTextChanged(curr_text)

    def setListener(self):
        self.ui.curr_segment_dropdown.currentTextChanged.connect(self.onCurrSegmentDropdownTextChanged)

    def onCurrSegmentDropdownTextChanged(self, value):
        ID, name = parseCurrSegmentText(value)
        selected_segment = findSegment(ID, name, self.segments)
        if selected_segment is None:
            self.writeMessage("ERROR: Cannot find segment with {}".format(value))
        self.scene.render_mesh(Path(selected_segment.data_file_name))
        self.writeMessage("{} rendered".format(value))

    def populateCurrSegmentDropDown(self):
        self.ui.curr_segment_dropdown.clear()
        for seg in self.segments:
            self.ui.curr_segment_dropdown.addItem("{} | {} ".format(seg.id, seg.segment_name))

    def populateSegmentList(self):
        self.ui.segment_list.clear()
        for seg in self.segments:
            check_box = QListWidgetItem()
            check_box.setText("{} | {} ".format(seg.id, seg.segment_name))
            check_box.setFlags(check_box.flags() | QtCore.Qt.ItemIsUserCheckable)
            check_box.setCheckState(QtCore.Qt.Unchecked)
            self.ui.segment_list.addItem(check_box)

    """
    Helper functions
    """

    def writeMessage(self, message: str):
        """
        Write message in message center
        Args:
            message: a string representing the message. Automatic line breaker will be appended

        Returns:
            None

        """
        self.ui.message_center_text_edit.append("> {}\n".format(message))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PlaneFitting(app=app)
    app.exec_()
