"""
Default static configuration for all applications
"""
from pathlib import Path

from appdirs import *

appname = "ATLAS"
appauthor = "FHL VIVE"

INSTALLATION_PATH = Path(__file__).parent
DEFAULT_STYLE_SHEET_PATH = (
    INSTALLATION_PATH / "model" / "layout" / "MaterialDark.qss"
)  # the default style sheet

ROOT = Path(user_data_dir(appname=appname, appauthor=appauthor))
DEFAULT_SEGMENTATION_FILE_PATH = (
    ROOT / "data" / "segment.json"
)  # refer to the default segment json file
DEFAULT_SCENE_FILE_PATH = ROOT / "data" / "scene.ply"  # refer to the default scene
DEFAULT_DATA_LOCATION = ROOT / "data"  # refer to the default data folder location
