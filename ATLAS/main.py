from ATLAS.controller.mainwindow_app import MainWindow
from PyQt5.QtWidgets import QApplication  # type: ignore
import sys
from ATLAS.config import ROOT, DEFAULT_DATA_LOCATION

if not DEFAULT_DATA_LOCATION.exists():
    print("No Data folder exist, creating it at --> ", ROOT)
    DEFAULT_DATA_LOCATION.mkdir(parents=True, exist_ok=True)

app = QApplication(sys.argv)

w = MainWindow(app)
app.exec_()
