# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'annotation_tool.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore


class Ui_annotation_app(object):
    def setupUi(self, annotation_app):
        annotation_app.setObjectName("annotation_app")
        annotation_app.resize(1440, 855)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(annotation_app.sizePolicy().hasHeightForWidth())
        annotation_app.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(annotation_app)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.visualization_vertical_layout = QtWidgets.QVBoxLayout()
        self.visualization_vertical_layout.setObjectName(
            "visualization_vertical_layout"
        )
        self.data_display_window = QtWidgets.QVBoxLayout()
        self.data_display_window.setObjectName("data_display_window")
        self.visualization_vertical_layout.addLayout(self.data_display_window)
        self.message_center_text_edit = QtWidgets.QTextEdit(annotation_app)
        self.message_center_text_edit.setMaximumSize(QtCore.QSize(16777215, 200))
        self.message_center_text_edit.setObjectName("message_center_text_edit")
        self.visualization_vertical_layout.addWidget(self.message_center_text_edit)
        self.horizontalLayout.addLayout(self.visualization_vertical_layout)
        self.interaction_vertical_layout = QtWidgets.QVBoxLayout()
        self.interaction_vertical_layout.setObjectName("interaction_vertical_layout")
        self.system_mode = QtWidgets.QTabWidget(annotation_app)
        self.system_mode.setObjectName("system_mode")
        self.floodfill_tab_btn = QtWidgets.QWidget()
        self.floodfill_tab_btn.setObjectName("floodfill_tab_btn")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.floodfill_tab_btn)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(40, 40, 291, 501))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.floodfill_btn_vertical_layout = QtWidgets.QVBoxLayout(
            self.verticalLayoutWidget_2
        )
        self.floodfill_btn_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.floodfill_btn_vertical_layout.setObjectName(
            "floodfill_btn_vertical_layout"
        )
        self.btn_floodfill_done = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btn_floodfill_done.setObjectName("btn_floodfill_done")
        self.floodfill_btn_vertical_layout.addWidget(self.btn_floodfill_done)
        self.btn_floodfill_cancel = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btn_floodfill_cancel.setObjectName("btn_floodfill_cancel")
        self.floodfill_btn_vertical_layout.addWidget(self.btn_floodfill_cancel)
        self.system_mode.addTab(self.floodfill_tab_btn, "")
        self.boundingbox_tab_btn = QtWidgets.QWidget()
        self.boundingbox_tab_btn.setObjectName("boundingbox_tab_btn")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.boundingbox_tab_btn)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(20, 20, 711, 531))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.boundingbox_interaction_grid_layout = QtWidgets.QGridLayout()
        self.boundingbox_interaction_grid_layout.setSizeConstraint(
            QtWidgets.QLayout.SetMinAndMaxSize
        )
        self.boundingbox_interaction_grid_layout.setObjectName(
            "boundingbox_interaction_grid_layout"
        )
        self.btn_boundingbox_crop = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.btn_boundingbox_crop.setObjectName("btn_boundingbox_crop")
        self.boundingbox_interaction_grid_layout.addWidget(
            self.btn_boundingbox_crop, 12, 1, 1, 1
        )
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_2.setObjectName("label_2")
        self.boundingbox_interaction_grid_layout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label.setObjectName("label")
        self.boundingbox_interaction_grid_layout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_3.setObjectName("label_3")
        self.boundingbox_interaction_grid_layout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_12.setObjectName("label_12")
        self.boundingbox_interaction_grid_layout.addWidget(self.label_12, 11, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_9.setObjectName("label_9")
        self.boundingbox_interaction_grid_layout.addWidget(self.label_9, 8, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_6.setObjectName("label_6")
        self.boundingbox_interaction_grid_layout.addWidget(self.label_6, 5, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_4.setObjectName("label_4")
        self.boundingbox_interaction_grid_layout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_10.setObjectName("label_10")
        self.boundingbox_interaction_grid_layout.addWidget(self.label_10, 9, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_5.setObjectName("label_5")
        self.boundingbox_interaction_grid_layout.addWidget(self.label_5, 4, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_11.setObjectName("label_11")
        self.boundingbox_interaction_grid_layout.addWidget(self.label_11, 10, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_7.setObjectName("label_7")
        self.boundingbox_interaction_grid_layout.addWidget(self.label_7, 6, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_8.setObjectName("label_8")
        self.boundingbox_interaction_grid_layout.addWidget(self.label_8, 7, 0, 1, 1)
        self.btn_boundingbox_translation_reset = QtWidgets.QPushButton(
            self.verticalLayoutWidget_5
        )
        self.btn_boundingbox_translation_reset.setMinimumSize(QtCore.QSize(612, 0))
        self.btn_boundingbox_translation_reset.setObjectName(
            "btn_boundingbox_translation_reset"
        )
        self.boundingbox_interaction_grid_layout.addWidget(
            self.btn_boundingbox_translation_reset, 0, 1, 1, 1
        )
        self.btn_boundingbox_rotation_reset = QtWidgets.QPushButton(
            self.verticalLayoutWidget_5
        )
        self.btn_boundingbox_rotation_reset.setObjectName(
            "btn_boundingbox_rotation_reset"
        )
        self.boundingbox_interaction_grid_layout.addWidget(
            self.btn_boundingbox_rotation_reset, 4, 1, 1, 1
        )
        self.btn_boundingbox_rotation_xVal = QtWidgets.QSlider(
            self.verticalLayoutWidget_5
        )
        self.btn_boundingbox_rotation_xVal.setOrientation(QtCore.Qt.Horizontal)
        self.btn_boundingbox_rotation_xVal.setObjectName(
            "btn_boundingbox_rotation_xVal"
        )
        self.boundingbox_interaction_grid_layout.addWidget(
            self.btn_boundingbox_rotation_xVal, 5, 1, 1, 1
        )
        self.btn_boundingbox_translation_zVal = QtWidgets.QSlider(
            self.verticalLayoutWidget_5
        )
        self.btn_boundingbox_translation_zVal.setOrientation(QtCore.Qt.Horizontal)
        self.btn_boundingbox_translation_zVal.setObjectName(
            "btn_boundingbox_translation_zVal"
        )
        self.boundingbox_interaction_grid_layout.addWidget(
            self.btn_boundingbox_translation_zVal, 3, 1, 1, 1
        )
        self.btn_boundingbox_rotation_zVal = QtWidgets.QSlider(
            self.verticalLayoutWidget_5
        )
        self.btn_boundingbox_rotation_zVal.setOrientation(QtCore.Qt.Horizontal)
        self.btn_boundingbox_rotation_zVal.setObjectName(
            "btn_boundingbox_rotation_zVal"
        )
        self.boundingbox_interaction_grid_layout.addWidget(
            self.btn_boundingbox_rotation_zVal, 7, 1, 1, 1
        )
        self.btn_boundingbox_scaling_yVal = QtWidgets.QSlider(
            self.verticalLayoutWidget_5
        )
        self.btn_boundingbox_scaling_yVal.setOrientation(QtCore.Qt.Horizontal)
        self.btn_boundingbox_scaling_yVal.setObjectName("btn_boundingbox_scaling_yVal")
        self.boundingbox_interaction_grid_layout.addWidget(
            self.btn_boundingbox_scaling_yVal, 10, 1, 1, 1
        )
        self.btn_boundingbox_scaling_xVal = QtWidgets.QSlider(
            self.verticalLayoutWidget_5
        )
        self.btn_boundingbox_scaling_xVal.setOrientation(QtCore.Qt.Horizontal)
        self.btn_boundingbox_scaling_xVal.setObjectName("btn_boundingbox_scaling_xVal")
        self.boundingbox_interaction_grid_layout.addWidget(
            self.btn_boundingbox_scaling_xVal, 9, 1, 1, 1
        )
        self.btn_boundingbox_translation_yVal = QtWidgets.QSlider(
            self.verticalLayoutWidget_5
        )
        self.btn_boundingbox_translation_yVal.setOrientation(QtCore.Qt.Horizontal)
        self.btn_boundingbox_translation_yVal.setObjectName(
            "btn_boundingbox_translation_yVal"
        )
        self.boundingbox_interaction_grid_layout.addWidget(
            self.btn_boundingbox_translation_yVal, 2, 1, 1, 1
        )
        self.btn_boundingbox_rotation_yVal = QtWidgets.QSlider(
            self.verticalLayoutWidget_5
        )
        self.btn_boundingbox_rotation_yVal.setOrientation(QtCore.Qt.Horizontal)
        self.btn_boundingbox_rotation_yVal.setObjectName(
            "btn_boundingbox_rotation_yVal"
        )
        self.boundingbox_interaction_grid_layout.addWidget(
            self.btn_boundingbox_rotation_yVal, 6, 1, 1, 1
        )
        self.btn_boundingbox_translation_xVal = QtWidgets.QSlider(
            self.verticalLayoutWidget_5
        )
        self.btn_boundingbox_translation_xVal.setOrientation(QtCore.Qt.Horizontal)
        self.btn_boundingbox_translation_xVal.setObjectName(
            "btn_boundingbox_translation_xVal"
        )
        self.boundingbox_interaction_grid_layout.addWidget(
            self.btn_boundingbox_translation_xVal, 1, 1, 1, 1
        )
        self.btn_boundingbox_scaling_reset = QtWidgets.QPushButton(
            self.verticalLayoutWidget_5
        )
        self.btn_boundingbox_scaling_reset.setObjectName(
            "btn_boundingbox_scaling_reset"
        )
        self.boundingbox_interaction_grid_layout.addWidget(
            self.btn_boundingbox_scaling_reset, 8, 1, 1, 1
        )
        self.btn_boundingbox_scaling_zVal = QtWidgets.QSlider(
            self.verticalLayoutWidget_5
        )
        self.btn_boundingbox_scaling_zVal.setOrientation(QtCore.Qt.Horizontal)
        self.btn_boundingbox_scaling_zVal.setObjectName("btn_boundingbox_scaling_zVal")
        self.boundingbox_interaction_grid_layout.addWidget(
            self.btn_boundingbox_scaling_zVal, 11, 1, 1, 1
        )
        self.verticalLayout.addLayout(self.boundingbox_interaction_grid_layout)
        self.system_mode.addTab(self.boundingbox_tab_btn, "")
        self.interaction_vertical_layout.addWidget(self.system_mode)
        self.common_btn_horizontal_layout = QtWidgets.QHBoxLayout()
        self.common_btn_horizontal_layout.setObjectName("common_btn_horizontal_layout")
        self.common_save_btn = QtWidgets.QPushButton(annotation_app)
        self.common_save_btn.setObjectName("common_save_btn")
        self.common_btn_horizontal_layout.addWidget(self.common_save_btn)
        self.common_load_btn = QtWidgets.QPushButton(annotation_app)
        self.common_load_btn.setObjectName("common_load_btn")
        self.common_btn_horizontal_layout.addWidget(self.common_load_btn)
        self.interaction_vertical_layout.addLayout(self.common_btn_horizontal_layout)
        self.segment_list = QtWidgets.QListWidget(annotation_app)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.segment_list.sizePolicy().hasHeightForWidth())
        self.segment_list.setSizePolicy(sizePolicy)
        self.segment_list.setObjectName("segment_list")
        self.interaction_vertical_layout.addWidget(self.segment_list)
        self.horizontalLayout.addLayout(self.interaction_vertical_layout)

        self.retranslateUi(annotation_app)
        self.system_mode.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(annotation_app)

    def retranslateUi(self, annotation_app):
        _translate = QtCore.QCoreApplication.translate
        annotation_app.setWindowTitle(_translate("annotation_app", "Dialog"))
        self.btn_floodfill_done.setText(_translate("annotation_app", "Done"))
        self.btn_floodfill_cancel.setText(_translate("annotation_app", "Cancel"))
        self.system_mode.setTabText(
            self.system_mode.indexOf(self.floodfill_tab_btn),
            _translate("annotation_app", "Floodfill"),
        )
        self.btn_boundingbox_crop.setText(_translate("annotation_app", "Crop"))
        self.label_2.setText(_translate("annotation_app", "    X"))
        self.label.setText(_translate("annotation_app", "Translation"))
        self.label_3.setText(_translate("annotation_app", "    Y"))
        self.label_12.setText(_translate("annotation_app", "    Z"))
        self.label_9.setText(_translate("annotation_app", "Scaling"))
        self.label_6.setText(_translate("annotation_app", "    X"))
        self.label_4.setText(_translate("annotation_app", "    Z"))
        self.label_10.setText(_translate("annotation_app", "    X"))
        self.label_5.setText(_translate("annotation_app", "Rotation"))
        self.label_11.setText(_translate("annotation_app", "    Y"))
        self.label_7.setText(_translate("annotation_app", "    Y"))
        self.label_8.setText(_translate("annotation_app", "    Z"))
        self.btn_boundingbox_translation_reset.setText(
            _translate("annotation_app", "Reset")
        )
        self.btn_boundingbox_rotation_reset.setText(
            _translate("annotation_app", "Reset")
        )
        self.btn_boundingbox_scaling_reset.setText(
            _translate("annotation_app", "Reset")
        )
        self.system_mode.setTabText(
            self.system_mode.indexOf(self.boundingbox_tab_btn),
            _translate("annotation_app", "Bounding Box"),
        )
        self.common_save_btn.setText(_translate("annotation_app", "Save"))
        self.common_load_btn.setText(_translate("annotation_app", "Load"))
