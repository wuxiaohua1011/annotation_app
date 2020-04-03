from ATLAS.controller.mainwindow_app import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
from ATLAS.config import ROOT, DEFAULT_DATA_LOCATION
import os

if not os.path.exists(DEFAULT_DATA_LOCATION.as_posix()):
    print("No Data folder exist, creating it at --> ", ROOT)
    os.makedirs(DEFAULT_DATA_LOCATION.as_posix())

app = QApplication(sys.argv)

w = MainWindow(
    app
)
app.exec_()
