import numpy as np  # type: ignore
import open3d as o3d  # type: ignore


class BoundingLine:
    """
    Sample usage:
        p1 = [0,0,0]
        p2 = [1,1,1]
        p = [2,3,2]
        axis = (0,1)
        bounding_line = BoudingLine(p1,p2,p,axis)
        print(bounding_line.checkSide([2,2,2]))
    """

    def __init__(self, line_start, line_end):
        self.line_start = line_start
        self.line_end = line_end

    def __str__(self):
        return " line_start: {} |  line_end: {} ".format(self.line_start, self.line_end)


def check_neighbor_condition(
    normals,
    coordinates,
    seed_id,
    current_neighbor,
    bounding_line,
    angle_error_tolerance,
):
    if bounding_line:
        if check_angle_condition(
            normals, seed_id, current_neighbor, angle_error_tolerance
        ) and check_distance(bounding_line, coordinates, current_neighbor):
            return True
    else:
        if check_angle_condition(
            normals, seed_id, current_neighbor, angle_error_tolerance
        ):
            return True
    return False


def check_angle_condition(normals, seed_id, current_neighbor, angle_error_tolerance):
    return (
        angle_between(normals[seed_id], normals[current_neighbor])
        < angle_error_tolerance
    )


def check_distance(bounding_line, coordinates, current_neighbor, threshold=0.1):
    """
    algorithm from wolfram alpha: http://mathworld.wolfram.com/Point-LineDistance3-Dimensional.html
    """
    x0 = coordinates[current_neighbor]
    x1 = bounding_line.line_start
    x2 = bounding_line.line_end
    d = np.linalg.norm(np.cross(x0 - x1, x0 - x2)) / np.linalg.norm(x2 - x1)
    return d > threshold


def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2', given that v1 and v2 are unit vectors:
    """
    return np.arccos(np.clip(np.dot(v1, v2), -1, 1))


def findNearestNeighbor(pcd, pcd_tree, current_point_id, batch_size):
    return pcd_tree.search_knn_vector_3d(pcd.points[current_point_id], batch_size)


def crop_remove(pcd, points_to_delete):
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)

    updated_points = np.delete(points, points_to_delete, axis=0)
    updated_color = np.delete(colors, points_to_delete, axis=0)
    pcd_updated = o3d.geometry.PointCloud()
    pcd_updated.points = o3d.utility.Vector3dVector(updated_points)
    pcd_updated.colors = o3d.utility.Vector3dVector(updated_color)
    return pcd_updated


def crop_reserve(pcd, points_to_reserve):
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)

    updated_points = np.take(points, points_to_reserve, axis=0)
    updated_color = np.take(colors, points_to_reserve, axis=0)

    pcd_updated = o3d.geometry.PointCloud()
    pcd_updated.points = o3d.utility.Vector3dVector(updated_points)
    pcd_updated.colors = o3d.utility.Vector3dVector(updated_color)
    return pcd_updated


def check_bounding_condition(bounding_line, coordinates, current_neighbor):
    return bounding_line.check(coordinates[current_neighbor])


class FloodfillError(Exception):
    pass


def floodfill(
    picked_points_id,
    pcd,
    batch_size=10,
    angle_error_tolerance=0.4,
    boundary_thickness=0.1,
):
    if not (len(picked_points_id) != 1 or len(picked_points_id) != 3):
        raise FloodfillError(
            "ERROR: {} points is chosen, only 1 and 3 point floodfill is implemented".format(
                len(picked_points_id)
            )
        )
    # set up
    pcd_tree = o3d.geometry.KDTreeFlann(pcd)
    pcd.estimate_normals()
    normals = np.asarray(pcd.normals)
    coordinates = np.asarray(pcd.points)
    bounding_line = None
    seed_id = None
    if len(picked_points_id) == 3:
        bounding_line = BoundingLine(
            coordinates[picked_points_id[0]], coordinates[picked_points_id[1]]
        )
        seed_id = picked_points_id[2]
    else:
        seed_id = picked_points_id[0]
    points_to_check = {seed_id}

    surface = set()

    counter = 0
    while len(points_to_check) != 0:
        current_point_id = points_to_check.pop()
        # find neighbors
        [k, idx, _] = findNearestNeighbor(pcd, pcd_tree, current_point_id, batch_size)
        neighbors = set(idx[1:])
        # parse the neighbors so that it does not contain points that are already in surface
        neighbors = neighbors.difference(surface)

        for current_neighbor in neighbors:
            # if angle_between(normals[seed_id], normals[n]) < angle_error_tolerance:
            if check_neighbor_condition(
                normals,
                coordinates,
                seed_id,
                current_neighbor,
                bounding_line,
                angle_error_tolerance,
            ):
                points_to_check.add(current_neighbor)
                surface.add(current_neighbor)
        counter += 1

    return list(surface)
