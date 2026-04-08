from typing import List, Optional, Literal, Annotated
from pydantic import BaseModel, Field


# -----------------------
# Reusable Types
# -----------------------

NonNegativeFloat = Annotated[float, Field(ge=0)]
PositiveFloat = Annotated[float, Field(gt=0)]
XiPattern = Annotated[str, Field(pattern=r"^ξ\d$")]


# -----------------------
# GeoJSON Polygon
# -----------------------

class BuildingPolygon(BaseModel):
    type: Literal["Polygon"]

    coordinates: List[  # list of rings
        List[           # ring
            List[float] # [x, y]
        ]
    ] = Field(
        ...,
        min_length=1,
        description="GeoJSON Polygon coordinates"
    )


# -----------------------
# Table Data
# -----------------------

class SubGroupTable(BaseModel):
    variation_coefficient: List[float] = Field(..., min_length=1)
    net_design_bearing_capacity: List[float] = Field(..., min_length=1)
    xi_values: List[float] = Field(..., min_length=1)
    pile_tip_level: List[float] = Field(..., min_length=1)

    mean_calculated_bearing_capacity: List[float] = Field(..., min_length=1)
    min_calculated_bearing_capacity: List[float] = Field(..., min_length=1)

    xi_factor: List[XiPattern] = Field(..., min_length=1)
    nominal_cpt: List[str] = Field(..., min_length=1)

    characteristic_bearing_capacity: List[float] = Field(..., min_length=1)
    design_negative_friction: List[float] = Field(..., min_length=1)
    design_bearing_capacity: List[float] = Field(..., min_length=1)

    group_centre_to_centre_validation_15: List[bool] = Field(..., min_length=1)
    group_centre_to_centre_validation_20: List[bool] = Field(..., min_length=1)
    group_centre_to_centre_validation_25: List[bool] = Field(..., min_length=1)
    group_centre_to_centre_validation: List[bool] = Field(..., min_length=1)


# -----------------------
# SubGroup Model
# -----------------------

class SubGroup(BaseModel):
    names: List[str] = Field(..., min_length=1)

    variation_check: bool
    spatial_check: bool
    centre_to_centre_check: bool

    minimum_pile_level: float
    maximum_pile_level: float

    number_of_consecutive_pile_levels: int

    coordinates: List[List[float]] = Field(
        ...,
        min_length=1,
        description="List of [x, y] coordinates"
    )

    table: SubGroupTable


# -----------------------
# Root Model
# -----------------------

class Grouper_Report(BaseModel):

    gamma_shaft: NonNegativeFloat = 1.2
    gamma_bottom: NonNegativeFloat = 1.2

    stiff_construction: bool = True

    cpt_grid_rotation: float = 0

    building_polygon: Optional[BuildingPolygon] = None

    include_centre_to_centre_check: bool = False

    sub_groups: List[SubGroup] = Field(..., min_length=1)

    project_name: str = Field(..., min_length=0, max_length=100)
    project_number: str = Field(..., min_length=0, max_length=100)
    project_remark: Optional[str] = Field(None, min_length=0, max_length=100)
    author: str = Field(..., min_length=0, max_length=100)
