import json
from ATLAS.controller.utilities.models import *
from vispy import scene  # type: ignore
import vispy  # type: ignore
import copy
import open3d as o3d  # type: ignore
import numpy as np  # type: ignore
from PyQt5.QtWidgets import (  # type: ignore
    QDialog,
    QFormLayout,
    QComboBox,
    QDialogButtonBox,
    QLineEdit,
    QLabel,
    QFileDialog,
)  # type: ignore
from pathlib import Path
from ATLAS.controller.utilities.utility import BaseScene
from typing import Union
from ATLAS.config import DEFAULT_DATA_LOCATION

system_modes = {0: "floodfill", 1: "boundingbox"}


def readSegmentation(filePath: Path) -> List[Segment]:
    """
    Read Segmentation from filePath
    :param filePath:
    :return: list of segments
    """
    try:
        result = []
        with open(filePath.as_posix(), "r") as f:
            segmentations = json.load(f)
        for segment in segmentations:
            seg = Segment.parse_obj(segment)
            result.append(seg)
        return result
    except FileNotFoundError as e:
        raise FileNotFoundError(
            "Given [{}] is not read in successfully.".format(filePath)
        )
    except UnicodeDecodeError as e:
        print("File [{}] cannot be read succesfully")
        raise e


def highlightIndices(
    mesh: o3d.geometry.TriangleMesh, indices_to_highlight: List[int]
) -> o3d.geometry.TriangleMesh:
    """
    Given a list of indicies, render the mesh with those indices to highlight
    Args:
        mesh: mesh that will be highlighted
        indices_to_highlight: indices to highlight

    Returns:
        a mesh whose indices is highlighted
    """
    color = np.asarray(mesh.vertex_colors)
    for i in indices_to_highlight:
        color[i] = (0, 1, 0)
    mesh.vertex_colors = o3d.utility.Vector3dVector(color)
    return mesh


class AnnotationScene(BaseScene):
    """
    Scene designed for AnnotationTool
    1. Can keep track of the main mesh, which is defined to be the first mesh that this scene renders
    2. keep track of selected_point_ids
    3. renders points with indices to highlight
    4. also keep track of the main data file ( aka where is the main mesh coming from)
    """

    def __init__(self, keys="interactive", size=(800, 800), point_size: float = 3.5):
        super().__init__(keys=keys, size=size, point_size=point_size)
        self.selected_point_ids: List[int] = []
        self.main_mesh: o3d.geometry.TriangleMesh = o3d.geometry.TriangleMesh()
        self.current_main_file_path: Union[Path, None] = None

    def readMesh(
        self, fpath: Path, render=False, autoclear=False
    ) -> o3d.geometry.TriangleMesh:
        if self.main_mesh.is_empty():
            self.current_main_file_path = fpath
        return super(AnnotationScene, self).readMesh(
            fpath=fpath, render=render, autoclear=autoclear
        )

    def renderMesh(self, mesh: o3d.geometry.TriangleMesh, autoclear: bool = False):
        if self.main_mesh.is_empty():
            self.main_mesh = mesh
        super().renderMesh(mesh=mesh, autoclear=autoclear)

    def clear(self):
        super().clear()
        self.selected_point_ids.clear()
        self.main_mesh = o3d.geometry.TriangleMesh()

    def on_mouse_release(self, event):
        if event.button == 1 and distanceTraveled(event.trail()) <= 2:
            try:
                selected_point_coord = self.findClickingCoord(event)
                if len(selected_point_coord) > 0:
                    selected_point_id = self.findPointIDFromClick(
                        selected_point_coord, 1
                    )[
                        0
                    ]  # select only one point at a time
                    self.selected_point_ids.append(selected_point_id)
                if len(self.selected_point_ids) == 2:
                    points = np.asarray(self.main_mesh.vertices)
                    pt1 = points[self.selected_point_ids[0]]
                    pt2 = points[self.selected_point_ids[1]]
                    self.draw_line(pt1, pt2)
            except Exception as e:
                print(e)
                pass

    def findPointIDFromClick(self, coord, n):
        """
        :param coord: centering coordinate
        :param n: number of closest point to coord
        :return: return n closest point to coord
        """
        pcd_tree = o3d.geometry.KDTreeFlann(self.main_mesh)
        [k, idx, _] = pcd_tree.search_knn_vector_3d(coord, n)
        return [idx.pop() for i in range(n)]

    def findClickingCoord(self, event):
        points = np.asarray(self.main_mesh.vertices)
        # colors = np.asarray(pcd.colors)
        # axis = scene.visuals.XYZAxis(parent=self.upper.scene)

        # prepare list of unique colors needed for picking
        ids = np.arange(1, len(points) + 1, dtype=np.uint32).view(np.uint8)
        ids = ids.reshape(-1, 4)
        ids = np.divide(ids, 255, dtype=np.float32)
        screen_pos = self.view.scene.transform.map(points)
        screen_pos = screen_pos[:, 0:2]

        # tmp = screen_pos - event.pos
        # all in marker coordinates
        # create point on line of clicked point but offset by in z direction
        # create direction of line as difference between clicked point and offset point
        # unit normalize direction
        # project candidate points to line
        # pick best candidate based on distance on line
        clicked_point = self.view.scene.transform.imap(event.pos)
        offset_point = np.asarray([event.pos[0], event.pos[1], 0.000001, 1])
        offset_point = self.view.scene.transform.imap(offset_point)
        direction = clicked_point - offset_point
        direction = direction[0:3]
        direction = direction / np.linalg.norm(direction)

        diff = np.linalg.norm(screen_pos - event.pos, axis=1)
        # print("min of diff =", min(diff))
        good_idxs = np.where(diff <= min(diff))[0]  # @Dapo
        # good_idxs = np.where(diff < 2)[0]
        candidate_points = points[good_idxs]
        centered_points = candidate_points - clicked_point[0:3]
        distances = np.matmul(centered_points, direction.reshape((3, 1)))
        good_idx = np.argmax(distances)

        tmp_point = candidate_points[good_idx, 0:3]
        tmp_point = tmp_point[
            np.newaxis, :
        ]  # reshape it to fit it into marker.set_data

        marker = scene.visuals.Markers()
        marker.set_gl_state("opaque", blend=False, depth_test=False)
        marker.set_data(tmp_point, edge_color="red", face_color="red", size=5.0)
        self.addViewChild(marker)

        return tmp_point[0]  # since we are only selecting 1 point at a time

    def draw_line(self, pt1, pt2):
        line = vispy.scene.visuals.Line(
            pos=np.asarray([pt1, pt2]),
            color="red",
            width=10,
            connect="strip",
            method="gl",
            antialias=False,
        )
        line.set_gl_state("opaque", blend=False, depth_test=False)
        self.addViewChild(line)


def meshToPointcloud(open3d_mesh):
    """
    converting an open3d mesh to open3d pointcloud by
    taking all the verticies and colors and put them into an PointCloud structure
    :param open3d_mesh:
    :return: o3d.geometry.PointCloud
    """
    points = np.asarray(open3d_mesh.vertices)
    colors = np.asarray(open3d_mesh.vertex_colors)

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    return pcd


def distanceTraveled(positions):
    """
    Return the total amount of pixels traveled in a sequence of pixel
    `positions`, using Manhattan distances for simplicity.
    """
    return np.sum(np.abs(np.diff(positions, axis=0)))


def prompt_saving():
    dialog = QDialog()
    form = QFormLayout(dialog)
    combo_box = QComboBox()
    combo_box.addItems(["Wall", "Floor", "Ceiling", "Other"])
    q_dialog_buttonbox = QDialogButtonBox()
    btn_ok = q_dialog_buttonbox.addButton(QDialogButtonBox.Ok)
    btn_cancel = q_dialog_buttonbox.addButton(QDialogButtonBox.Cancel)
    line_edit = QLineEdit()
    form.addRow(QLabel("Segment Name:"), line_edit)
    form.addRow(QLabel("Segmentation type:"), combo_box)
    form.addRow(q_dialog_buttonbox)

    def btn_ok_clicked():
        dialog.close()

    def btn_cancel_clicked():
        dialog.close()

    btn_ok.clicked.connect(btn_ok_clicked)

    btn_cancel.clicked.connect(btn_cancel_clicked)
    dialog.exec_()
    return {"type_class": combo_box.currentText(), "seg_name": line_edit.text()}


def openFileNamesDialog(env, default_data_location: Path = DEFAULT_DATA_LOCATION):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    files, _ = QFileDialog.getOpenFileNames(
        env,
        "QFileDialog.getOpenFileNames()",
        "",
        "All Files (*);;Python Files (*.py)",
        options=options,
        directory=default_data_location.as_posix(),
    )
    if files:
        return files[0]
    return None
