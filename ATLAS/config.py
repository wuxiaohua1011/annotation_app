"""
Default static configuration for all applications
"""
from pathlib import Path

ROOT = Path("/Users/michaelwu/Desktop/projects/GD/ATLAS_annotation_tools")  # TODO: automatically find path here

DEFAULT_STYLE_SHEET_PATH = ROOT / "model" / "layout" / "MaterialDark.qss"  # the default style sheet
DEFAULT_SEGMENTATION_FILE_PATH = ROOT / "data" / "segment.json"  # refer to the default segment json file
DEFAULT_SCENE_FILE_PATH = ROOT / "data" / "scene.ply"  # refer to the default scene
DEFAULT_DATA_LOCATION = ROOT / "data"  # refer to the default data folder location
