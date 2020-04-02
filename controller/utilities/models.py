from typing import List, Tuple, Optional
from pydantic import BaseModel, FilePath
import pathlib
import pydantic.json

pydantic.json.ENCODERS_BY_TYPE[pathlib.PosixPath] = str
pydantic.json.ENCODERS_BY_TYPE[pathlib.WindowsPath] = str


class Segment(BaseModel):
    id: int
    data_file_name: str
    segment_name: str
    indices: List[int]
    type: str = "Layout"
    type_class: Optional[Tuple[str, int]] = None
    intersection: int = 0
    plane_equation: Optional[Tuple[List[float], float]] = None
    vertices: Optional[List[List[float]]] = None
