#####
# Please read how to test with pytestQt
# https://pytest-qt.readthedocs.io/en/latest/
#####
from PyQt5.QtWidgets import QApplication
import sys
from ATLAS.controller.atlas_annotation_tool_app import AtlasAnnotationAppWindow
import os
import pathlib

path = pathlib.Path(os.getcwd())
proj_root = path.parent.parent
style_sheet_location = (proj_root / "model/layout/MaterialDark.qss").as_posix()
data_location = (proj_root / "data/scene.ply").as_posix()
segmentation_file_location = (proj_root / "data/segment.json").as_posix()


def test_window_initial_semantics(qtbot):
    app = QApplication(sys.argv)
    w = AtlasAnnotationAppWindow(
        app,
        style_sheet_path=style_sheet_location,
        scene_file_path=data_location,
        segmentation_file_path=segmentation_file_location,
    )
    qtbot.addWidget(w)

    assert w.ui.common_save_btn.text() == "Save"
    assert w.ui.common_load_btn.text() == "Load"
    assert w.currentSystemMode == "floodfill"

    assert w.ui.btn_floodfill_done.text() == "Done"
    assert w.ui.btn_floodfill_cancel.text() == "Cancel"

    assert w.ui.btn_boundingbox_translation_reset.text() == "Reset"
    assert w.ui.btn_boundingbox_rotation_reset.text() == "Reset"
    assert w.ui.btn_boundingbox_scaling_reset.text() == "Reset"
