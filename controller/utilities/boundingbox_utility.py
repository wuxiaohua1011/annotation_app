import numpy as np  # type: ignore
import open3d as o3d  # type: ignore
from vispy import scene  # type: ignore


class BBOX:
    # spawn bbox unit cube, centered at origin
    # TODO: Support spawning at user-specified location
    def __init__(self):
        self.origin_bbox_min = np.array([-0.5, -0.5, -0.5, 1])
        self.origin_bbox_max = np.array([0.5, 0.5, 0.5, 1])
        # current 4D matrix for the bounding box
        self.scale = np.identity(4)
        self.x_rot = np.identity(4)
        self.y_rot = np.identity(4)
        self.z_rot = np.identity(4)
        self.translate = np.identity(4)
        # for internal verification purposes
        self.create_outline()

    def create_outline(self):
        self.outline_pts = [
            [-0.5, -0.5, -0.5],
            [0.5, -0.5, -0.5],
            [-0.5, 0.5, -0.5],
            [0.5, 0.5, -0.5],
            [-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],
            [-0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5],
        ]
        self.outline_lines = np.array(
            [
                [0, 1],
                [0, 2],
                [1, 3],
                [2, 3],
                [4, 5],
                [4, 6],
                [5, 7],
                [6, 7],
                [0, 4],
                [1, 5],
                [2, 6],
                [3, 7],
            ]
        )
        self.outline_colors = [[1, 0, 0] for i in range(len(self.outline_lines))]
        self.line_set = o3d.geometry.LineSet()
        self.line_set.lines = o3d.utility.Vector2iVector(self.outline_lines)
        self.line_set.colors = o3d.utility.Vector3dVector(self.outline_colors)

    def set_scale(self, x, y, z):
        self.scale = np.array([[x, 0, 0, 0], [0, y, 0, 0], [0, 0, z, 0], [0, 0, 0, 1]])

    def set_x_rot(self, theta):
        theta = np.radians(theta)
        self.x_rot = np.array(
            [
                [1, 0, 0, 0],
                [0, np.cos(theta), -np.sin(theta), 0],
                [0, np.sin(theta), np.cos(theta), 0],
                [0, 0, 0, 1],
            ]
        )

    def set_y_rot(self, theta):
        theta = np.radians(theta)
        self.y_rot = np.array(
            [
                [np.cos(theta), 0, np.sin(theta), 0],
                [0, 1, 0, 0],
                [-np.sin(theta), 0, np.cos(theta), 0],
                [0, 0, 0, 1],
            ]
        )

    def set_z_rot(self, theta):
        theta = np.radians(theta)
        self.z_rot = np.array(
            [
                [np.cos(theta), -np.sin(theta), 0, 0],
                [np.sin(theta), np.cos(theta), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )

    def set_translate(self, x, y, z):
        self.translate = np.array(
            [[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]]
        )

    # INPUT: point cloud object
    # OUTPUT: indices of points within the bbox
    def crop_idx(self, pcd_input):
        [[x1, x2], [y1, y2], [z1, z2], [_, _]] = list(
            zip(self.origin_bbox_min, self.origin_bbox_max)
        )
        # assume input parameters are not yet sorted
        [x_max, x_min, y_max, y_min, z_max, z_min] = [
            max(x1, x2),
            min(x1, x2),
            max(y1, y2),
            min(y1, y2),
            max(z1, z2),
            min(z1, z2),
        ]
        # return cropped pcd indices as numpy array
        current_mat = np.dot(
            self.translate,
            np.dot(self.z_rot, np.dot(self.y_rot, np.dot(self.x_rot, self.scale))),
        )
        a = np.asarray(
            [
                np.dot(np.linalg.inv(current_mat), np.append(pcd_pts, 1.0))[:3]
                for pcd_pts in pcd_input.points
            ]
        )
        return np.where(
            (a[:, 0] >= x_min)
            & (a[:, 0] <= x_max)
            & (a[:, 1] >= y_min)
            & (a[:, 1] <= y_max)
            & (a[:, 2] >= z_min)
            & (a[:, 2] <= z_max)
        )

    # OUTPUT: current outline of bounding box as line set
    def get_o3d_outline(self):
        current_mat = np.dot(
            self.translate,
            np.dot(self.z_rot, np.dot(self.y_rot, np.dot(self.x_rot, self.scale))),
        )
        current_points = [
            np.dot(current_mat, np.append(point, 1.0))[:3] for point in self.outline_pts
        ]
        self.line_set.points = o3d.utility.Vector3dVector(current_points)
        return self.line_set

    # OUTPUT: current outline of bounding box as array of corner coordinates
    def get_outline(self):
        current_mat = np.dot(
            self.translate,
            np.dot(self.z_rot, np.dot(self.y_rot, np.dot(self.x_rot, self.scale))),
        )
        current_points = [
            np.dot(current_mat, np.append(point, 1.0))[:3] for point in self.outline_pts
        ]
        return [
            [current_points[line[0]], current_points[line[1]]]
            for line in self.outline_lines
        ]


class Line(scene.visuals.Line):
    def __init__(self, *args, **kwargs):
        scene.visuals.Line.__init__(self, *args, **kwargs)
        self.unfreeze()
        self.markers = scene.visuals.Markers(parent=self)
        self.markers.set_data(
            pos=self.pos, face_color="red", edge_color="red", size=self.width
        )

    def update_markers(self, new_pos):
        self.unfreeze()
        self.markers.set_data(
            pos=new_pos, face_color="red", edge_color="red", size=self.width
        )
