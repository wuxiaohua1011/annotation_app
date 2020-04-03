from PyQt5.QtWidgets import QApplication  # type: ignore
from ATLAS.view.annotation_tool_ui import Ui_annotation_app
from ATLAS.controller.utilities.atlas_annotation_tool_util import *
from ATLAS.controller.utilities.floodfill_utility import floodfill, crop_reserve
from ATLAS.controller.utilities.boundingbox_utility import BBOX, Line
from ATLAS.controller.utilities.models import Segment
import vispy  # type: ignore
from ATLAS.config import DEFAULT_STYLE_SHEET_PATH, DEFAULT_DATA_LOCATION, DEFAULT_SCENE_FILE_PATH, \
    DEFAULT_SEGMENTATION_FILE_PATH
from ATLAS.controller.utilities.utility import BaseWindow
from vispy import scene
import warnings
warnings.filterwarnings(action="ignore", category=FutureWarning)


class AtlasAnnotationAppWindow(BaseWindow):
    """
    Class controlling the behavior of the Annotation App.

    Responsible for
    1. Listening to user actions on the GUI and invoke the respective backend functions
    2. Maintain interaction with other screens(going back to Main menu, etc)
    3. Must have consistent MenuBar behavior as other windows
    """
    def __init__(self,
                 app: QApplication,
                 segmentation_file_path: Path = DEFAULT_SEGMENTATION_FILE_PATH,
                 style_sheet_path: Path = DEFAULT_STYLE_SHEET_PATH,
                 scene_file_path: Path = DEFAULT_SCENE_FILE_PATH,
                 show: bool = True
                 ):
        super().__init__(app=app,
                         UI=Ui_annotation_app,
                         style_sheet_location=style_sheet_path,
                         show=show)

        self.segmentation_file_path = segmentation_file_path
        self.messages = ["Program Started, UI Loaded"]  # list of strings
        self.segments: List[Segment] = []  # list of Segment objects
        self.current_cropped_data: List = []
        self.upperScene = AnnotationScene()
        self.lowerScene = AnnotationScene()
        self.currentSystemMode = -1
        self.system_mode_clicked()

        self.populateSegmentList()
        self.setupCanvas()

        # demo
        self.upperScene.readMesh(DEFAULT_SCENE_FILE_PATH, render=True)
        print(self.upperScene.current_main_file_path)

    def setListener(self):
        self.ui.btn_floodfill_done.clicked.connect(self.btn_floodfill_done_clicked)
        self.ui.btn_floodfill_cancel.clicked.connect(self.btn_floodfill_cancel_clicked)
        self.ui.common_load_btn.clicked.connect(self.btn_common_load_clicked)
        self.ui.common_save_btn.clicked.connect(self.btn_save_clicked)
        self.ui.segment_list.itemDoubleClicked.connect(
            self.segmentation_list_item_double_clicked
        )

        self.ui.btn_boundingbox_crop.clicked.connect(self.btn_boundingbox_cropped)
        self.ui.system_mode.currentChanged.connect(self.system_mode_clicked)
        self.ui.btn_boundingbox_translation_xVal.valueChanged.connect(
            self.bbox_update_translate
        )
        self.ui.btn_boundingbox_translation_yVal.valueChanged.connect(
            self.bbox_update_translate
        )
        self.ui.btn_boundingbox_translation_zVal.valueChanged.connect(
            self.bbox_update_translate
        )
        self.ui.btn_boundingbox_translation_reset.clicked.connect(
            self.bbox_reset_translate
        )
        self.ui.btn_boundingbox_rotation_xVal.valueChanged.connect(
            self.bbox_update_rot_x
        )
        self.ui.btn_boundingbox_rotation_yVal.valueChanged.connect(
            self.bbox_update_rot_y
        )
        self.ui.btn_boundingbox_rotation_zVal.valueChanged.connect(
            self.bbox_update_rot_z
        )
        self.ui.btn_boundingbox_rotation_reset.clicked.connect(self.bbox_reset_rotation)
        self.ui.btn_boundingbox_scaling_xVal.valueChanged.connect(
            self.bbox_update_scale
        )
        self.ui.btn_boundingbox_scaling_yVal.valueChanged.connect(
            self.bbox_update_scale
        )
        self.ui.btn_boundingbox_scaling_zVal.valueChanged.connect(
            self.bbox_update_scale
        )
        self.ui.btn_boundingbox_scaling_reset.clicked.connect(self.bbox_reset_scaling)

    def system_mode_clicked(self):
        """
        Listener for on system click event

        System modes supported:
            1. floodfill
            2. boundingbox
        Returns:
            None
        """
        try:
            self.currentSystemMode = system_modes[self.ui.system_mode.currentIndex()]
        except KeyError as err:
            self.writeMessage("Cannot understand current system mode")
            print(err)
            exit(1)
        if self.currentSystemMode == "UNKNOWN":
            print("ERR, system mode = -1 ")
        elif self.currentSystemMode == "boundingbox":
            if not self.upperScene.main_mesh.is_empty():
                self.start_bbox()
        else:
            self.destroy_bbox()

    def setupCanvas(self):
        """
        Set up canvas for displaying scene
        Returns:

        """
        self.ui.data_display_window.addWidget(self.upperScene.native)
        self.ui.data_display_window.addWidget(self.lowerScene.native)

    """
    Event Listener
    """

    def btn_floodfill_done_clicked(self):
        """
        Listner for on btn_floodfill_done_clicked
        1. If there's one point, execute floodfill
        2. if there's two points, tell user that this is an invalid action, hit cancel to re-select
        3. if there's three points, execute floodfill
        4. if there's more than three points, tell user that this is an invalid action, hit cancel to re-select
        Returns:
            None
        """
        if len(self.upperScene.selected_point_ids) == 1:
            print("One points detected, floodfilling")
            pcd = meshToPointcloud(self.upperScene.main_mesh)
            surface_to_crop = floodfill(self.upperScene.selected_point_ids, pcd)
            self.current_cropped_data = surface_to_crop
            new_pcd = crop_reserve(pcd, surface_to_crop)
            self.lowerScene.renderPCD(new_pcd)
        elif len(self.upperScene.selected_point_ids) == 2:
            self.writeMessage(
                "Two Points <{}> selected so far, instruction is unclear, abort".format(
                    self.upperScene.selected_point_ids
                )
            )
        elif len(self.upperScene.selected_point_ids) == 3:
            print("three points detected, floodfilling")
            pcd = meshToPointcloud(self.upperScene.main_mesh)
            surface_to_crop = floodfill(self.upperScene.selected_point_ids, pcd)
            self.current_cropped_data = surface_to_crop
            new_pcd = crop_reserve(pcd, surface_to_crop)
            self.lowerScene.renderPCD(new_pcd)
        else:
            self.writeMessage(
                "More than 3 points chosen, not implemented this functionality yet, please hit cancel to re-select"
            )

    def btn_floodfill_cancel_clicked(self):
        """
        listener for on btn_floodfill is clicked.

        clear the mesh and the selected points field
        clear current cropped data

        Returns:
            None
        """
        mesh = self.upperScene.main_mesh
        self.upperScene.clear()
        self.upperScene.renderMesh(mesh)
        self.current_cropped_data = []


    def btn_common_load_clicked(self):
        """
        Invoke select file window
        Returns:
            None
        """
        filename = openFileNamesDialog(self)
        # do filetype checking here
        if filename:
            import os

            dirpath = os.getcwd()
            relative_path = filename.replace(dirpath, ".")
            # self.current_data_file_name = relative_path  # TODO this might cause issue later on
            self.writeMessage("Opening file <{}>".format(filename))
            self.upperScene.clear()
            self.upperScene.readMesh(fpath=Path(filename), render=True)
            self.current_cropped_data = []

    def btn_save_clicked(self):
        response = prompt_saving()

        if response.get("seg_name", "") == "":
            self.writeMessage("Please provide a segmentation name")
        else:
            # assume that the state of the program should have existing segments all read in from file
            # from initializing the program.
            if (
                    len(self.upperScene.selected_point_ids) == 0
                    and self.currentSystemMode == 0
            ):
                self.writeMessage("There are no points to save")
            else:
                new_seg = Segment(
                    id=len(self.segments),
                    data_file_name=self.upperScene.current_main_file_path.as_posix(),  # TODO broken here
                    segment_name=response.get("seg_name"),
                    indices=self.current_cropped_data,
                    type_class=(response.get("type_class", "Unknown Class"), 1),
                )
                self.segments.append(new_seg)
                self.ui.segment_list.addItem(
                    "{} | {} | {}".format(
                        new_seg.id, new_seg.segment_name, new_seg.type_class
                    )
                )

                self.writeSegments()
                # can we just remove the bbox and floodfill markings instead and leave the rest
                if self.currentSystemMode == 0:
                    self.lowerScene.clear()
                    mesh = self.upperScene.main_mesh
                    self.upperScene.renderMesh(mesh=mesh, autoclear=True)
                self.writeMessage("Data Saved")
                self.current_cropped_data = []

    def segmentation_list_item_double_clicked(self):
        current_item_text = self.ui.segment_list.currentItem().text()
        try:
            current_item_index = int(current_item_text.split(" | ")[0])
            selected_segment = self.segments[current_item_index]
            self.upperScene.renderMesh(
                mesh=highlightIndices(
                    self.upperScene.readMesh(fpath=Path(selected_segment.data_file_name),
                                             render=False,
                                             autoclear=False),
                    indices_to_highlight=selected_segment.indices),
                autoclear=False)

        except ValueError as e:
            self.writeMessage(
                "ERR: Index is not an int --> {}".format(
                    current_item_text.split(" | ")[0]
                )
            )

    """
    Helper functions
    """

    def writeMessage(self, message):
        self.messages.append(message)
        self.ui.message_center_text_edit.append("> {}\n".format(message))

    def populateSegmentList(self):
        self.segments.clear()
        self.ui.segment_list.clear()
        try:
            new_segs = readSegmentation(self.segmentation_file_path)
            for new_seg in new_segs:
                self.segments.append(new_seg)
                self.ui.segment_list.addItem(
                    "{} | {} | {}".format(
                        new_seg.id, new_seg.segment_name, new_seg.type_class
                    )
                )
        except FileNotFoundError:
            self.writeMessage("No segments read")

    def writeSegments(self):
        with open(self.segmentation_file_path.as_posix(), mode="w") as f:
            json.dump(
                [json.loads(segment.json()) for segment in self.segments], f, indent=4
            )

    def start_bbox(self):
        self.children_before_bbox = len(self.upperScene.view.children[0].children)

        try:
            self.bbox
        except:
            self.bbox = BBOX()
        self.bbox_outlines = [
            Line(
                pos=np.array(outline),
                color="r",
                width=5,
                connect="strip",
                method="gl",
                antialias=True,
            )
            for outline in self.bbox.get_outline()
        ]
        # self.view.add adds a reference
        [self.upperScene.view.add(outline) for outline in self.bbox_outlines]

    def destroy_bbox(self):
        for child in self.upperScene.view.children[0].children:
            if type(child) != vispy.scene.visuals.Mesh and not isinstance(child, scene.BaseCamera):
                child.parent = None

    def vis_bbox(self):
        new_outline = self.bbox.get_outline()
        for i in range(len(new_outline)):
            convert_array = np.array(
                [ind_array.tolist() for ind_array in new_outline[i]]
            )
            self.bbox_outlines[i].set_data(convert_array)
            self.bbox_outlines[i].update_markers(convert_array)

    def bbox_update_translate(self):
        self.bbox.set_translate(
            self.ui.btn_boundingbox_translation_xVal.value(),
            self.ui.btn_boundingbox_translation_yVal.value(),
            self.ui.btn_boundingbox_translation_zVal.value(),
        )
        self.vis_bbox()

    def bbox_update_rot_x(self):
        self.bbox.set_x_rot(self.ui.btn_boundingbox_rotation_xVal.value())
        self.vis_bbox()

    def bbox_update_rot_y(self):
        self.bbox.set_y_rot(self.ui.btn_boundingbox_rotation_yVal.value())
        self.vis_bbox()

    def bbox_update_rot_z(self):
        self.bbox.set_z_rot(self.ui.btn_boundingbox_rotation_zVal.value())
        self.vis_bbox()

    def bbox_update_scale(self):
        self.bbox.set_scale(
            self.ui.btn_boundingbox_scaling_xVal.value(),
            self.ui.btn_boundingbox_scaling_yVal.value(),
            self.ui.btn_boundingbox_scaling_zVal.value(),
        )
        self.vis_bbox()

    def bbox_reset_translate(self):
        self.ui.btn_boundingbox_translation_xVal.setValue(0)
        self.ui.btn_boundingbox_translation_yVal.setValue(0)
        self.ui.btn_boundingbox_translation_zVal.setValue(0)

    def bbox_reset_rotation(self):
        self.ui.btn_boundingbox_rotation_xVal.setValue(0)
        self.ui.btn_boundingbox_rotation_yVal.setValue(0)
        self.ui.btn_boundingbox_rotation_zVal.setValue(0)

    def bbox_reset_scaling(self):
        self.ui.btn_boundingbox_scaling_xVal.setValue(1)
        self.ui.btn_boundingbox_scaling_yVal.setValue(1)
        self.ui.btn_boundingbox_scaling_zVal.setValue(1)

    def btn_boundingbox_cropped(self):
        try:
            tmp_pointcloud = o3d.geometry.PointCloud()
            tmp_pointcloud.points = self.upperScene.main_mesh.vertices
            tmp_pointcloud.colors = self.upperScene.main_mesh.vertex_colors
            bb_to_crop = self.bbox.crop_idx(tmp_pointcloud)
            new_pcd = crop_reserve(tmp_pointcloud, bb_to_crop[0].tolist())
            self.lowerScene.renderPCD(new_pcd)
            self.current_cropped_data = bb_to_crop[0].tolist()
        except Exception as e:
            print("error")
            print(e)
            self.writeMessage(str(e))
        self.writeMessage("Selected Points is cleared")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = AtlasAnnotationAppWindow(app=app)
    app.exec_()
