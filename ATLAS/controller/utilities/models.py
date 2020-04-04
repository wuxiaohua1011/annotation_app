from typing import List, Tuple
from pydantic import BaseModel, FilePath
import pathlib
import pydantic.json
import abc
import open3d as o3d
from typing import Optional
import numpy as np

pydantic.json.ENCODERS_BY_TYPE[pathlib.PosixPath] = str
pydantic.json.ENCODERS_BY_TYPE[pathlib.WindowsPath] = str


class Geometry(BaseModel, abc.ABC):
    equation: Tuple[List[float], float] = ()
    cad_model: o3d.geometry.TriangleMesh = o3d.geometry.TriangleMesh()

    class Config:
        arbitrary_types_allowed = True


class Plane(Geometry):
    def __init__(self, **data):
        super().__init__(**data)


class Segment(BaseModel):
    id: int
    data_file_name: str  #  TODO: change all other things
    segment_name: str
    indices: List[int]
    type: str = "Layout"
    type_class: Tuple[str, int] = ()
    intersection: List[int] = []
    geometry: Optional[Geometry] = None
    vertices: List[List[float]] = []

    class Config:
        arbitrary_types_allowed = True
