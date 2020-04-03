import sys
import os

# Temporary fix for path
sys.path.insert(0, os.path.dirname(os.getcwd()))
import json
from controller.utilities.models import *
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


class Scene(scene.SceneCanvas):
    def __init__(self):
        scene.SceneCanvas.__init__(self, keys="interactive", size=(800, 800))
        self.unfreeze()
        self.camera_mode = "turntable"
        self.pcd = None
        self.marker = None
        self.view = self.central_widget.add_view()
        self.view.camera = self.camera_mode
        self.selected_point_ids = []
        self.point_size = 3.5
        self.additional_elements = []
        self.mesh: o3d.geometry.TriangleMesh = None
        self.pcd_fname = None

    def render_mesh(self, fname: Path = None, autoclear=False, indices_to_highlight=[]):
        if autoclear:
            self.clear()
        mesh = None
        if fname is None:
            mesh = copy.deepcopy(self.mesh)
        else:
            mesh = o3d.io.read_triangle_mesh(fname.as_posix())
            self.mesh = mesh
            self.pcd_fname = fname.as_posix()
            self.pcd = mesh_to_pointcloud(mesh)
        if len(indices_to_highlight) != 0:
            color = np.asarray(mesh.vertex_colors)
            for i in indices_to_highlight:
                color[i] = (0, 1, 0)
            mesh.vertex_colors = o3d.utility.Vector3dVector(color)
        self.render_helper(mesh)

    def render_helper(self, mesh):
        points = np.asarray(mesh.vertices)
        faces = np.asarray(
            mesh.triangles
        )  # nx3 array of ints each element is the index of point in the triangle

        # create scatter object and fill in the data
        scatter = scene.visuals.Mesh(
            vertices=points, faces=faces, vertex_colors=mesh.vertex_colors
        )
        self.view.add(scatter)

    def render_pcd(self, pcd, autoclear_view=True):
        if autoclear_view:
            self.clear()
        points = np.asarray(pcd.points)
        colors = np.asarray(pcd.colors)
        self.marker = scene.visuals.Markers()
        self.marker.set_gl_state("translucent", blend=True, depth_test=True)
        self.marker.set_data(
            points, edge_color=colors, face_color=colors, size=self.point_size
        )
        self.view.add(self.marker)

    def clear(self):
        self.central_widget.remove_widget(self.view)
        self.view = self.central_widget.add_view()
        self.additional_elements = []
        self.selected_point_ids = []
        self.view.camera = self.camera_mode

    def on_mouse_release(self, event):
        if event.button == 1 and distance_traveled(event.trail()) <= 2:
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
                    points = np.asarray(self.mesh.vertices)
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
        pcd_tree = o3d.geometry.KDTreeFlann(self.mesh)
        [k, idx, _] = pcd_tree.search_knn_vector_3d(coord, n)
        return [idx.pop() for i in range(n)]

    def findClickingCoord(self, event):
        points = np.asarray(self.mesh.vertices)
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
        self.view.add(marker)

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
        self.view.add(line)


def mesh_to_pointcloud(open3d_mesh):
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


def distance_traveled(positions):
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


def openFileNamesDialog(env):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    files, _ = QFileDialog.getOpenFileNames(
        env,
        "QFileDialog.getOpenFileNames()",
        "",
        "All Files (*);;Python Files (*.py)",
        options=options,
    )
    if files:
        return files[0]
    return None
