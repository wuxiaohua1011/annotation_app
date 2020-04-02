import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import QtWidgets

from view.MainWindow import Ui_MainWindow

app = QApplication(sys.argv)
ex = Ui_MainWindow()
w = QtWidgets.QMainWindow()
ex.setupUi(w)
w.show()
sys.exit(app.exec_())

#
# import sys
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QAction
# # from PyQt5.QtGui import QHbox
#
#
# class menudemo(QMainWindow):
#     def __init__(self, parent=None):
#         super(menudemo, self).__init__(parent)
#
#         layout = QHBoxLayout()
#         bar = self.menuBar()
#         file = bar.addMenu("File")
#         file.addAction("New")
#
#         save = QAction("Save", self)
#         save.setShortcut("Ctrl+S")
#         file.addAction(save)
#
#         edit = file.addMenu("Edit")
#         edit.addAction("copy")
#         edit.addAction("paste")
#
#         quit = QAction("Quit", self)
#         file.addAction(quit)
#         file.triggered[QAction].connect(self.processtrigger)
#         self.setLayout(layout)
#         self.setWindowTitle("menu demo")
#
#     def processtrigger(self, q):
#         print
#         q.text() + " is triggered"
#
#
# def main():
#     app = QApplication(sys.argv)
#     ex = menudemo()
#     ex.show()
#     sys.exit(app.exec_())
#
#
# if __name__ == '__main__':
#     main()
