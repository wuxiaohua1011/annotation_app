from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from ATLAS.config import DEFAULT_STYLE_SHEET_PATH
from pathlib import Path
from abc import abstractmethod
from vispy import scene
import open3d as o3d
import numpy as np
from typing import Dict, Any


class BaseWindow(QtWidgets.QMainWindow):
    def __init__(self,
                 app: QApplication,
                 UI,
                 style_sheet_location: Path = DEFAULT_STYLE_SHEET_PATH,
                 show=True):
        """

        Args:
            app: QApplication
            UI: a callable that represents a class. ex: Ui_MainWindow in view/mainwindow_ui.py
            style_sheet_location: location of the style sheet
        """
        super().__init__()
        self.app = app
        self.ui = UI()
        try:
            self.ui.setupUi(self)
        except AttributeError as e:
            raise AttributeError("Given UI {} does not have setupUi function. Please see documentation".format(UI))
        self.app.setStyleSheet(open(str(style_sheet_location.as_posix())).read())

        self.setListener()
        if show:
            self.show()

    @abstractmethod
    def setListener(self):
        raise NotImplementedError


class BaseScene(scene.SceneCanvas):
    """
    Responsible for all events happing inside a scene
    1. Handle mouse point click
    2. handle rendering of the scene
    3. keep track of all objects that are currently being rendered
    4. able to remove/add another object to be rendered
    5. can read in a ply file and renders it
    """

    def __init__(self, keys="interactive", size=(800, 800), point_size: float = 3.5):
        scene.SceneCanvas.__init__(self, keys=keys, size=size)
        self.unfreeze()
        self.camera_mode = "turntable"
        self.view: scene.widgets.viewbox.ViewBox = self.initView()
        self.view_children_tracker: Dict[int, Any] = dict()  # dictionary mapping ID to a children in view
        self.last_children_id: int = -1  # possible to have integer overflow issue, but not likely
        self.point_size = point_size

    def renderMesh(self, mesh: o3d.geometry.TriangleMesh, autoclear: bool = False):
        """
        Given a mesh, renders it.
        If autoclear set to true, clear the scene before graphing
        Args:
            mesh: open3d's Triangle Mesh
            autoclear: if true, clear the scene, otherwise, leave it alone

        Returns:
            None
        """
        if autoclear:
            self.clear()
        vis_mesh = scene.visuals.Mesh(vertices=np.asarray(mesh.vertices),
                                      faces=np.asarray(mesh.triangles),
                                      vertex_colors=mesh.vertex_colors)
        self.addViewChild(vis_mesh)

    def initView(self) -> scene.widgets.viewbox.ViewBox:
        """
        Initialize view
        Returns:
            the new view object
        """
        view = self.central_widget.add_view()
        view.camera = self.camera_mode
        return view

    def addViewChild(self, child: Any):
        """
        Add Child to self.view_children_tracker
        Automatically increment last_children_id
        Add Child to self.view
        Args:
            child: an object that is rendered on self.view

        Returns:
            None
        """
        self.view_children_tracker[self.last_children_id + 1] = child
        self.last_children_id += 1
        self.view.add(child)

    def removeViewChild(self, child: Any = None, ID: int = -1):
        """
        remove child from view
        remove child from tracker

        Note: this function does NOT decrement last_children_id
        Args:
            child:
            ID:

        Returns:

        """

        assert not (child is None and ID == -1), "Cannot remove child is None and ID==-1"

        # print("child = {}, id = ".format(child, ID))
        if ID != -1:
            child_in_memory = self.view_children_tracker[ID]
            assert child is not None and child == child_in_memory, \
                "The provided child and the child in memory refer to different things"
            del self.view_children_tracker[ID]
            child.parent = None  # this function might error
        else:
            for k, c in self.view_children_tracker.items():
                if c == child:
                    ID = k
            assert ID != -1, "ID not found in self.view_children_tracker.items()"

            child.parent = None  # this function might error
            del self.view_children_tracker[ID]



    def clear(self):
        """
        clears the scene, including the objects in memory
        Returns:
            None
        """
        for ID, child in self.view_children_tracker.items():
            print("Removing child id {}, child {}".format(ID, child))
            self.removeViewChild(child=child, ID=ID)
        self.central_widget.remove_widget(self.view)
        self.view = self.initView()

    def renderPCD(self, pcd: o3d.geometry.PointCloud, autoclear=False):
        """
        Given a pcd, renders it
        If autoclear is set to true, clear the scene before graphing
        Args:
            pcd: open3d PCD object
            autoclear: if true, clear the scene, otherwise, leave it alone

        Returns:
            None
        """
        if autoclear:
            self.clear()
        points = np.asarray(pcd.points)
        colors = np.asarray(pcd.colors)
        marker = scene.visuals.Markers()
        marker.set_gl_state("translucent", blend=True, depth_test=True)
        marker.set_data(
            points, edge_color=colors, face_color=colors, size=self.point_size
        )
        self.addViewChild(marker)



    def readMesh(self, fpath: Path, render=False, autoclear=False) -> o3d.geometry.TriangleMesh:
        """
        read in a ply file and return the mesh, render if necessary
        Args:
            autoclear: if true, clear the scene, otherwise, leave it alone
            render: if true, render the ply file
            fpath: File path to a data file. ex: a .ply file

        Returns:
            the mesh being rendered
        """
        mesh = o3d.io.read_triangle_mesh(fpath.as_posix())
        if render:
            self.renderMesh(mesh, autoclear=autoclear)
        return mesh

    def readPCD(self, fpath:Path, render=False, autoclear=False) -> o3d.geometry.PointCloud:
        """
        read in a ply file and return the pointcloud, render if necessary
        Args:
            autoclear: if true, clear the scene, otherwise, leave it alone
            render: if true, render the ply file
            fpath: File path to a data file. ex: a .ply file

        Returns:
            the mesh being rendered
        """
        pcd = o3d.io.read_point_cloud(fpath.as_posix())
        if render:
            self.renderPCD(pcd, autoclear=autoclear)
        return pcd

    @abstractmethod
    def on_mouse_release(self, event):
        raise NotImplementedError

