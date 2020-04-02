import open3d as o3d
import numpy as np

pointcloud = o3d.io.read_point_cloud("./data/scene.ply")


orientedBoundingBox = o3d.geometry.OrientedBoundingBox.create_from_points(
    pointcloud.points
)

box_corners = np.asarray(orientedBoundingBox.get_box_points())
print("the eight points that define the bounding box ==> \n {} \n".format(box_corners))
box_center = np.asanyarray(orientedBoundingBox.get_center())
print("the center of the geometry coordinate ==> \n {} \n".format(box_center))
o3d.visualization.draw_geometries([pointcloud, orientedBoundingBox])

axis_aligned_bounding_box = orientedBoundingBox.get_axis_aligned_bounding_box()
o3d.visualization.draw_geometries([pointcloud, axis_aligned_bounding_box])


points = [
    box_center,
    box_center
    + np.cross(box_corners[1] - box_corners[0], box_corners[2] - box_corners[0]),
    box_center
    + np.cross(box_corners[4] - box_corners[3], box_corners[5] - box_corners[3]),
    box_center
    + np.cross(box_corners[1] - box_corners[0], box_corners[3] - box_corners[0]),
    box_center
    + np.cross(box_corners[4] - box_corners[2], box_corners[5] - box_corners[2]),
    box_center
    + np.cross(box_corners[2] - box_corners[0], box_corners[3] - box_corners[0]),
    box_center
    + np.cross(box_corners[6] - box_corners[1], box_corners[7] - box_corners[1]),
]

lines = [[0, 1], [0, 3], [0, 6]]
colors = [[0, 0, 1] for i in range(len(lines))]
line_set = o3d.geometry.LineSet(
    points=o3d.utility.Vector3dVector(points), lines=o3d.utility.Vector2iVector(lines)
)
line_set.colors = o3d.utility.Vector3dVector(colors)
o3d.visualization.draw_geometries([pointcloud, orientedBoundingBox, line_set])
