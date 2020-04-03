import trimesh

from open3d.open3d.geometry import TriangleMesh

from ATLAS.config import DEFAULT_SEGMENTATION_FILE_PATH
from typing import Union, Dict
from ATLAS.controller.utilities.atlas_annotation_tool_util import *


class PlaneFittingUtil:
    def __init__(self, pcd: Union[o3d.geometry.PointCloud, Path]):
        self.pcd = o3d.io.read_point_cloud(pcd.as_posix()) if isinstance(pcd, Path) else pcd
        self.pcd_copy = o3d.io.read_point_cloud(pcd.as_posix()) if isinstance(pcd, Path) else pcd
        self.orientedBoundingBox = o3d.geometry.OrientedBoundingBox.create_from_points(self.pcd.points)
        self.box_corners = np.asarray(self.orientedBoundingBox.get_box_points())
        # print("the eight points that define the bounding box ==> \n {} \n".format(self.box_corners))
        self.box_center = np.asanyarray(self.orientedBoundingBox.get_center())
        # print("the center of the geometry coordinate ==> \n {} \n".format(self.box_center))
        # calculate norm for each face
        points = [self.box_center]
        normal1 = np.cross(self.box_corners[1] - self.box_corners[0], self.box_corners[2] - self.box_corners[0])
        points.append(self.box_center + normal1)
        normal4 = np.cross(self.box_corners[4] - self.box_corners[3], self.box_corners[5] - self.box_corners[3])
        points.append(self.box_center + normal4)
        normal2 = np.cross(self.box_corners[1] - self.box_corners[0], self.box_corners[3] - self.box_corners[0])
        points.append(self.box_center + normal2)
        normal5 = np.cross(self.box_corners[4] - self.box_corners[2], self.box_corners[5] - self.box_corners[2])
        points.append(self.box_center + normal5)
        normal3 = np.cross(self.box_corners[2] - self.box_corners[0], self.box_corners[3] - self.box_corners[0])
        points.append(self.box_center + normal3)
        normal6 = np.cross(self.box_corners[6] - self.box_corners[1], self.box_corners[7] - self.box_corners[1])
        points.append(self.box_center + normal6)
        self.normal_list = [None, normal1, normal2, normal3, normal4, normal5, normal6]
        # calculate three axis
        lines = [[0, 1], [0, 3], [0, 6]]
        colors = [[0, 0, 2] for i in range(len(lines))]
        self.line_set = o3d.geometry.LineSet(
            points=o3d.utility.Vector3dVector(points), lines=o3d.utility.Vector2iVector(lines)
        )
        self.line_set.colors = o3d.utility.Vector3dVector(colors)

    def auto_clip_segments(self,
                           segments: Union[Path, List[Segment]] = DEFAULT_SEGMENTATION_FILE_PATH) -> \
            Tuple[List[Segment], o3d.geometry.OrientedBoundingBox, o3d.geometry.PointCloud]:
        """
        1. Parse the JSON file and read in the segements
        2. generate mesh for all segments
        3. clip mesh against each other

        Args:
            segments: List of Segments or file path to json of a list of segment

        Returns:

        """

        # first read in segments
        if isinstance(segments, Path):
            segments = readSegmentation(segments)  # turn segments into a List[Segment]
        # then generate mesh for all segments
        for seg in segments:
            surface_to_crop = seg.indices
            if len(surface_to_crop) == 0:
                continue
            mesh, n, d = self.crop_plane_bbox(surface_to_crop=surface_to_crop)
            seg.intersection = []
            seg.geometry = Plane(cad_model=mesh, equation=(n, d))
        # then clip each segment mesh against all other segments'
        for seg in segments:
            self.crop_plane(target=seg, planes=segments)

        return segments, self.orientedBoundingBox, self.pcd

    def crop_plane_bbox(self, surface_to_crop: List[int]) -> \
            Tuple[TriangleMesh, List[float], float]:
        """
        crop a plane according to the surface_to_crop and return the mesh object and 3d plane equation
        Args:
            surface_to_crop: list of integer representing the indices of in the pcd that should be cropped out

        Returns:
            mesh -> the cropped mesh resulting from taking surface_to_crop from self.pcd
            n, d -> plane equation resulting from o3d.PointCloud.segment_plane function
        """
        points = np.asarray(self.pcd_copy.points)[surface_to_crop]  # convert index to real points and index error here
        seg = o3d.geometry.PointCloud()
        seg.points = o3d.utility.Vector3dVector(points)

        segmented_plane = seg.segment_plane(0.1, 3, 10)
        segmented_plane_equation = segmented_plane[0]
        n: List[float] = segmented_plane_equation[:-1]
        n /= np.linalg.norm(n)
        d: float = segmented_plane_equation[-1]
        a = [-n[1], n[0], 0]
        a /= np.linalg.norm(a)
        b = np.cross(n, a)
        b /= np.linalg.norm(b)
        r = get_r(n)
        r = r.T

        vertices = np.array([
            [-0.5, 0.5, 0],
            [0.5, 0.5, 0],
            [0.5, -0.5, 0],
            [-0.5, -0.5, 0]
        ])
        vertices = np.dot(vertices, 10)

        triangles = np.array([
            [0, 1, 3],
            [1, 2, 3]
        ])

        vertices = [np.matmul(v, r) - np.multiply(n, d) for v in vertices]
        mesh = o3d.geometry.TriangleMesh()
        mesh.vertices = o3d.utility.Vector3dVector(np.asarray(vertices))
        mesh.triangles = o3d.utility.Vector3iVector(np.asarray(triangles))
        trimesh_mesh = trimesh.Trimesh(vertices=np.asarray(mesh.vertices), faces=np.asarray(mesh.triangles))
        trimesh_mesh = trimesh_mesh.slice_plane(self.box_corners[0], self.normal_list[1])
        trimesh_mesh = trimesh_mesh.slice_plane(self.box_corners[0], - self.normal_list[2])
        trimesh_mesh = trimesh_mesh.slice_plane(self.box_corners[0], self.normal_list[3])
        trimesh_mesh = trimesh_mesh.slice_plane(self.box_corners[5], - self.normal_list[4])
        trimesh_mesh = trimesh_mesh.slice_plane(self.box_corners[5], self.normal_list[5])
        trimesh_mesh = trimesh_mesh.slice_plane(self.box_corners[6], self.normal_list[6])
        mesh.vertices = o3d.utility.Vector3dVector(np.asarray(trimesh_mesh.vertices))
        mesh.triangles = o3d.utility.Vector3iVector(np.asarray(trimesh_mesh.faces))
        return mesh, list(n), d

    def crop_plane(self, target: Segment, planes: List[Segment]):
        """
        clip target against all other plane in planes.
        Note: this function will modify target's cad_model field in place
        Args:
            target: the desired plane to be clipped
            planes: all other planes used to clip target

        Returns:
            None

        """
        old_mesh = target.geometry.cad_model
        trimesh_mesh = trimesh.Trimesh(vertices=np.asarray(old_mesh.vertices), faces=np.asarray(old_mesh.triangles))
        for plane in planes:
            if plane != target:
                trimesh_mesh = trimesh_mesh.slice_plane(self.pcd.points[plane.indices[0]], plane.geometry.equation[0])
        target.geometry.cad_model.vertices = o3d.utility.Vector3dVector(np.asarray(trimesh_mesh.vertices))
        target.geometry.cad_model.triangles = o3d.utility.Vector3iVector(np.asarray(trimesh_mesh.faces))


def getMeshesFromSegment(segment: Segment) -> Dict[str, o3d.geometry.TriangleMesh]:
    """
    Takes a segment, return meshes that it represent
    1. The mesh that can be red from data_file_name
    2. cad_model
    Args:
        segment:

    Returns:
        Dictionary of  NAME -> Mesh
        ex:
        {
            "base": BASE_MESH
            "cad_model": CAD_MODEL_MESH
        }

    """
    result: Dict[str, o3d.geometry.TriangleMesh] = dict()
    if segment.data_file_name:
        base = o3d.io.read_triangle_mesh(segment.data_file_name)
        result["base"] = base
    if segment.geometry and segment.geometry.cad_model:
        result["cad_model"] = segment.geometry.cad_model
    return result

# TODO: adding comments
def get_r(n):
    n = n / np.linalg.norm(n)
    n_hat = hat_operator(n)
    a = None
    b = None
    epsilon = 0.01
    for i in range(3):
        if np.linalg.norm(n_hat[i, :]) > epsilon:  # none zero
            a = n_hat[i, :] / np.linalg.norm(n_hat[i, :])
            if np.abs(np.dot(n, a)) < epsilon:  # orthogonal
                b = np.cross(n, a)
                break
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)
    b = np.cross(n, a)
    r = np.eye(3)
    r[:, 0] = a
    r[:, 1] = b
    r[:, 2] = n
    return r


# return a 3 by 3 hat matrix for a vector, used for cross product
def hat_operator(vector):
    w1 = vector[0]
    w2 = vector[1]
    w3 = vector[2]

    matrix = np.zeros((3, 3))
    matrix[0, 1] = -w3
    matrix[0, 2] = w2
    matrix[1, 0] = w3
    matrix[1, 2] = -w1
    matrix[2, 0] = -w2
    matrix[2, 1] = w1
    return matrix


def parseCurrSegmentText(value: str) -> Tuple[int, str]:
    """
    parse the CurrSegmentText
    ex: value = ID: 0 | wall1
    return: (0, wall1)
    Args:
        value:

    Returns:
        ID and name of the value
    """
    ID, name = value.split("|", maxsplit=1)
    if name is None:
        raise Exception("Unknown CurrSegmentText encountered --> [{}]".format(value))
    try:
        int(ID)
    except ValueError:
        raise Exception("Cannot convert ID [{}] to int ".format(ID))
    return int(ID), name


def findSegment(ID: int, name: str, segments: List[Segment]) -> Union[Segment, None]:
    """
    Use ID and name to find segemnt in a list of segments
    Args:
        ID: integer representing the ID of a segment
        name: name of the segement
        segments: list of segement to find

    Returns:
        None if does not exist
        segment if found
    """
    for seg in segments:
        if seg.id == ID:
            return seg
    return None


class Scene(scene.SceneCanvas):
    def __init__(self):
        scene.SceneCanvas.__init__(self, keys="interactive", size=(800, 800))
        self.unfreeze()
        self.camera_mode = "turntable"
        self.view = self.setView()
        self.point_size = 3.5
        self.meshes: List[o3d.geometry.TriangleMesh] = []

    def setView(self):
        """
        initialize the current view
        Returns:
            current view

        """
        view = self.central_widget.add_view()
        view.camera = self.camera_mode
        return view

    def clearView(self):
        """
        clear the current view
        Returns:

        """
        self.central_widget.remove_widget(self.view)
        self.view = self.central_widget.add_view()

    def render_mesh(self):
        """
        render all meshes in self.meshes

        Returns:
            None
        """
        for mesh in self.meshes:
            print("rendering mesh", mesh)
            if mesh.is_empty():
                continue
            points = np.asarray(mesh.vertices)
            faces = np.asarray(
                mesh.triangles
            )  # nx3 array of ints each element is the index of point in the triangle
            # create scatter object and fill in the data
            scatter = scene.visuals.Mesh(
                vertices=points, faces=faces, vertex_colors= mesh.vertex_colors if mesh.has_vertex_colors() else None
            )
            self.view.add(scatter)

    def setMeshes(self, meshes: List[o3d.geometry.TriangleMesh]):
        self.meshes = meshes

    def clear(self):
        """
        clear the current view
        clear meshes
        reset self.view
        Returns:
            None
        """
        self.clearView()
        self.meshes.clear()
        self.view = self.setView()


    def on_mouse_release(self, event):
        if event.button == 1 and distance_traveled(event.trail()) <= 2:
            print("Mouse Released")
