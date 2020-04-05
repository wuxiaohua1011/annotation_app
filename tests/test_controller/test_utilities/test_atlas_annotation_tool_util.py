from ATLAS.controller.utilities import atlas_annotation_tool_util
import pytest


def test_readSegment():
    err_f_path = "/"
    with pytest.raises(IsADirectoryError) as e:
        atlas_annotation_tool_util.readSegmentation(err_f_path)


def test_distance_traveled():
    d = [0, 1]
    assert atlas_annotation_tool_util.distanceTraveled(d) == 1

    d = [0, -1]
    assert atlas_annotation_tool_util.distanceTraveled(d) == 1
