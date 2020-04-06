import trimesh
import json
from ATLAS.controller.utilities.floodfill_utility import *
from ATLAS.controller.utilities.models import *

# TODO: parse json file
# TODO: find the intersection of planes


class PlaneFitting:
    # read in data and setup the corresponding fields
    def __init__(self):
        # read in scene.ply and display essential vertices
        self.pcd = o3d.io.read_point_cloud("./data/scene.ply")
        self.pcd_copy = o3d.io.read_point_cloud("./data/scene.ply")
        self.orientedBoundingBox = o3d.geometry.OrientedBoundingBox.create_from_points(
            self.pcd.points
        )
        self.box_corners = np.asarray(self.orientedBoundingBox.get_box_points())
        print(
            "the eight points that define the bounding box ==> \n {} \n".format(
                self.box_corners
            )
        )
        self.box_center = np.asanyarray(self.orientedBoundingBox.get_center())
        print(
            "the center of the geometry coordinate ==> \n {} \n".format(self.box_center)
        )
        # calculate norm for each face
        points = [self.box_center]
        normal1 = np.cross(
            self.box_corners[1] - self.box_corners[0],
            self.box_corners[2] - self.box_corners[0],
        )
        points.append(self.box_center + normal1)
        normal4 = np.cross(
            self.box_corners[4] - self.box_corners[3],
            self.box_corners[5] - self.box_corners[3],
        )
        points.append(self.box_center + normal4)
        normal2 = np.cross(
            self.box_corners[1] - self.box_corners[0],
            self.box_corners[3] - self.box_corners[0],
        )
        points.append(self.box_center + normal2)
        normal5 = np.cross(
            self.box_corners[4] - self.box_corners[2],
            self.box_corners[5] - self.box_corners[2],
        )
        points.append(self.box_center + normal5)
        normal3 = np.cross(
            self.box_corners[2] - self.box_corners[0],
            self.box_corners[3] - self.box_corners[0],
        )
        points.append(self.box_center + normal3)
        normal6 = np.cross(
            self.box_corners[6] - self.box_corners[1],
            self.box_corners[7] - self.box_corners[1],
        )
        points.append(self.box_center + normal6)
        self.normal_list = [None, normal1, normal2, normal3, normal4, normal5, normal6]
        # calculate three axis
        lines = [[0, 1], [0, 3], [0, 6]]
        colors = [[0, 0, 2] for i in range(len(lines))]
        self.line_set = o3d.geometry.LineSet(
            points=o3d.utility.Vector3dVector(points),
            lines=o3d.utility.Vector2iVector(lines),
        )
        self.line_set.colors = o3d.utility.Vector3dVector(colors)
        self.segments = []

    # handle mouse click event and crop the relevant plane
    def handle_click(self):
        to_display = [self.orientedBoundingBox, self.pcd]
        original_colors = self.pcd.colors
        for _ in range(5):  # only display 5 segments for now
            point = pick_points(self.pcd_copy)
            surface_to_crop = floodfill([point[0]], self.pcd_copy)
            self.crop_plane(to_display, surface_to_crop)
        # display
        o3d.visualization.draw_geometries(to_display)

    # handle json file, return a list of segment objects
    # print(data[0].keys())
    # dict_keys(['id', 'data_file_name', 'segment_name', 'indices', 'type', 'type_class', 'intersection', 'plane_equation', 'vertices'])
    def handle_json(self, filepath):
        to_display = [self.orientedBoundingBox, self.pcd]
        segment_list = []
        original_colors = self.pcd.colors
        with open(filepath) as f:
            data = json.load(f)
        for seg in data:
            surface_to_crop = seg["indices"]
            mesh, n, d = self.crop_plane_bbox(surface_to_crop)
            data = dict(
                id=seg["id"],
                data_file_name=seg["data_file_name"],
                segment_name=seg["segment_name"],
                indices=surface_to_crop,
                type=seg["type"],
                type_class=seg["type_class"],
                intersection=[],  # b/c we are using the json file generated from old Segment class
                geometry=Plane(cad_model=mesh, equation=(n, d)),
                vertices=seg["vertices"],
            )
            segment_list.append(Segment(**data))

        for segment in segment_list:
            self.crop_plane(to_display, segment, segment_list)

        # display
        o3d.visualization.draw_geometries(to_display)
        return segment_list, [self.orientedBoundingBox, self.pcd]

    # crop a plane according to the surface_to_crop and return the mesh object and 3d points
    def crop_plane_bbox(self, surface_to_crop):
        points = np.asarray(self.pcd_copy.points)[
            surface_to_crop
        ]  # convert index to real points and index error here
        seg = o3d.geometry.PointCloud()
        seg.points = o3d.utility.Vector3dVector(points)

        tuple = seg.segment_plane(0.1, 3, 10)
        n = tuple[0][:-1]
        n /= np.linalg.norm(n)
        d = tuple[0][-1]
        a = [-n[1], n[0], 0]
        a /= np.linalg.norm(a)
        b = np.cross(n, a)
        b /= np.linalg.norm(b)
        r = get_r(n)
        r = r.T

        vertices = np.array(
            [[-0.5, 0.5, 0], [0.5, 0.5, 0], [0.5, -0.5, 0], [-0.5, -0.5, 0]]
        )
        vertices = np.dot(vertices, 10)

        triangles = np.array([[0, 1, 3], [1, 2, 3]])

        vertices = [np.matmul(v, r) - np.multiply(n, d) for v in vertices]

        mesh = o3d.geometry.TriangleMesh()
        mesh.vertices = o3d.utility.Vector3dVector(np.asarray(vertices))
        mesh.triangles = o3d.utility.Vector3iVector(np.asarray(triangles))
        trimesh_mesh = trimesh.Trimesh(
            vertices=np.asarray(mesh.vertices), faces=np.asarray(mesh.triangles)
        )
        trimesh_mesh = trimesh_mesh.slice_plane(
            self.box_corners[0], self.normal_list[1]
        )
        trimesh_mesh = trimesh_mesh.slice_plane(
            self.box_corners[0], -self.normal_list[2]
        )
        trimesh_mesh = trimesh_mesh.slice_plane(
            self.box_corners[0], self.normal_list[3]
        )
        trimesh_mesh = trimesh_mesh.slice_plane(
            self.box_corners[5], -self.normal_list[4]
        )
        trimesh_mesh = trimesh_mesh.slice_plane(
            self.box_corners[5], self.normal_list[5]
        )
        trimesh_mesh = trimesh_mesh.slice_plane(
            self.box_corners[6], self.normal_list[6]
        )
        mesh.vertices = o3d.utility.Vector3dVector(np.asarray(trimesh_mesh.vertices))
        mesh.triangles = o3d.utility.Vector3iVector(np.asarray(trimesh_mesh.faces))
        # to_display.append(mesh) # mesh is a CAD model, plane equation, indices of points
        return mesh, list(n), d

    def crop_plane(self, to_display, target, planes):
        old_mesh = target.geometry.cad_model
        trimesh_mesh = trimesh.Trimesh(
            vertices=np.asarray(old_mesh.vertices), faces=np.asarray(old_mesh.triangles)
        )
        for plane in planes:
            if plane != target:
                trimesh_mesh = trimesh_mesh.slice_plane(
                    self.pcd.points[plane.indices[0]], plane.geometry.equation[0]
                )
        target.geometry.cad_model.vertices = o3d.utility.Vector3dVector(
            np.asarray(trimesh_mesh.vertices)
        )
        target.geometry.cad_model.triangles = o3d.utility.Vector3iVector(
            np.asarray(trimesh_mesh.faces)
        )
        to_display.append(target.geometry.cad_model)


##### HELPER FUNCTION #####

# pick points clicked by mouse
def pick_points(pcd):
    print("")
    print("1) Please pick at least three correspondences using [shift + left click]")
    print("   Press [shift + right click] to undo point picking")
    print("2) Afther picking points, press q for close the window")
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(pcd)
    vis.run()  # user picks points
    vis.destroy_window()
    print("")
    return vis.get_picked_points()


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


########### END ###########

if __name__ == "__main__":
    print("Plane Fitting Begins\n")
    pf = PlaneFitting()
    # print("Mouse Click Begins\n")
    # pf.handle_click()

    # parse Json file
    print("Parse Json Begins")
    segment_list, base = pf.handle_json("data/segment.json")
    segment_list = [None] + segment_list
    print("Parse Json Ends.\n")

    # intersect
    # print("Intersect Begins")
    # plane_list[2].display()
    # plane_list[3].display()
    # plane_list[2].intersect(plane_list[3])
    # print("Intersect Ends.\n ")
