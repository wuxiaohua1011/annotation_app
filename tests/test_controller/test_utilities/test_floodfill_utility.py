from controller.utilities import floodfill_utility
import open3d as o3d
import numpy as np
import pytest


@pytest.fixture
def generate_sample_pointcloud():
    pcl = o3d.geometry.PointCloud()
    np.random.seed(1)  # So that I can reproduce the result
    pcl.points = o3d.utility.Vector3dVector(np.random.randn(10000, 3))
    pcl.colors = o3d.utility.Vector3dVector(np.random.randn(10000, 3))
    return pcl


def test_floodfill(generate_sample_pointcloud):
    picked_points_id = [0, 1, 2]
    surface_ids = floodfill_utility.floodfill(
        picked_points_id, generate_sample_pointcloud
    )
    actual_ans = [3329, 2]
    assert len(surface_ids) == 2
    assert surface_ids == actual_ans


def test_crop_reserve(generate_sample_pointcloud):
    picked_points_id = [0, 1, 2]
    surface_ids = floodfill_utility.floodfill(
        picked_points_id, generate_sample_pointcloud
    )
    r = floodfill_utility.crop_reserve(generate_sample_pointcloud, surface_ids)
    assert isinstance(r, o3d.geometry.PointCloud)
    assert len(np.asarray(r.points)) == 2


def test_crop_remove(generate_sample_pointcloud):
    picked_points_id = [0, 1, 2]
    surface_ids = floodfill_utility.floodfill(
        picked_points_id, generate_sample_pointcloud
    )
    r = floodfill_utility.crop_remove(generate_sample_pointcloud, surface_ids)
    assert isinstance(r, o3d.geometry.PointCloud)
    assert len(np.asarray(r.points)) == 10000 - 2
