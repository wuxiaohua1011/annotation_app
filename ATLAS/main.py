from ATLAS.controller.mainwindow_app import MainWindow
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

w = MainWindow(
    app,

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
