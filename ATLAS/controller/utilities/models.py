from typing import List, Tuple
from pydantic import BaseModel, Field
import pathlib
import pydantic.json
import abc
import open3d as o3d  # type: ignore
from typing import Optional

pydantic.json.ENCODERS_BY_TYPE[pathlib.PosixPath] = str
pydantic.json.ENCODERS_BY_TYPE[pathlib.WindowsPath] = str


class Geometry(BaseModel, abc.ABC):
    equation: Tuple[List[float], float] = Field(
        ...,
        title="Equation of the geometry",
        description="In the format of ((x, y, z), m)",
    )
    cad_model: o3d.geometry.TriangleMesh = Field(
        o3d.geometry.TriangleMesh(), title="CAD Model of the geometry"
    )

    class Config:
        arbitrary_types_allowed = True


class Plane(Geometry):
    def __init__(self, **data):
        super().__init__(**data)


class Segment(BaseModel):
    id: int
    data_file_name: str  # TODO: change all other things
    segment_name: str
    indices: List[int]
    type: str = "Layout"
    type_class: Tuple[str, int] = Field(..., title="the type of this segement")
    intersection: List[int] = []
    geometry: Geometry = Field(None, title="Geometry that represent this segment")
    vertices: List[List[float]] = []

    class Config:
        arbitrary_types_allowed = True
