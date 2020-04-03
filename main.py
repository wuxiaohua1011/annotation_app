from controller.atlas_annotation_tool_app import AtlasAnnotationAppWindow
from controller.mainwindow_app import MainWindow
from PyQt5.QtWidgets import QApplication
import sys

style_sheet_location = "./model/layout/MaterialDark.qss"
data_location = "./data/scene.ply"
segmentation_file_path = "./data/segment.json"

app = QApplication(sys.argv)

w = MainWindow(
    app
)
app.exec_()


# w = AtlasAnnotationAppWindow(
#     app,
#     style_sheet_location=style_sheet_location,
#     data_location=data_location,
#     segmentation_file_path=segmentation_file_location,
# )
# w.show()
# app.exec_()
