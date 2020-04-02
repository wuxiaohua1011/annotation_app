"""
Default static configuration for all applications
"""
from pathlib import Path

DEFAULT_STYLE_SHEET_LOCATION = Path.cwd().parent / "model" / "layout" / "MaterialDark.qss"  # the default style sheet
DEFAULT_SEGMENTATION_FILE_LOCATION = Path.cwd().parent / "data" / "segment.json"  # refer to the default segment json file
DEFAULT_SCENE_LOCATION = Path.cwd().parent / "data" / "scene.ply"  # refer to the default scene
DEFAULT_DATA_LOCATION = Path.cwd().parent / "data"  # refer to the default data folder location
