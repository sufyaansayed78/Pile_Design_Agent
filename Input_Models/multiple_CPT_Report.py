from typing import List, Optional, Union, Literal, Annotated
from pydantic import BaseModel, Field


# =========================================================
# Basic Constrained Types
# =========================================================

NonNegativeFloat = Annotated[float, Field(ge=0)]
PositiveFloat = Annotated[float, Field(gt=0)]
UnitInterval = Annotated[float, Field(ge=0, le=1)]


# =========================================================
# CPT DATA
# =========================================================

class CPTData(BaseModel):
    qc: List[NonNegativeFloat] = Field(..., min_length=1)
    depth: List[NonNegativeFloat] = Field(..., min_length=1)
    u: Optional[List[float]] = Field(None, min_length=1)


# =========================================================
# LAYER TABLE
# =========================================================

SoilEnum = Literal["gravel", "sand", "silt", "clay", "peat"]

class LayerTableData(BaseModel):
    thickness: List[PositiveFloat] = Field(..., min_length=1, max_length=100)
    lower_boundary: List[NonNegativeFloat] = Field(..., min_length=1, max_length=100)

    C_s: Optional[List[PositiveFloat]] = Field(None, min_length=1, max_length=100)
    C_p: Optional[List[PositiveFloat]] = Field(None, min_length=1, max_length=100)
    tau_mob_max: Optional[List[PositiveFloat]] = Field(None, min_length=1, max_length=100)
    qc_gem_failure_test: Optional[List[PositiveFloat]] = Field(None, min_length=1, max_length=100)

    gamma_unsat: List[NonNegativeFloat] = Field(..., min_length=1, max_length=100)
    gamma_sat: List[NonNegativeFloat] = Field(..., min_length=1, max_length=100)
    phi: List[NonNegativeFloat] = Field(..., min_length=1, max_length=100)

    main_component: List[SoilEnum] = Field(..., min_length=1, max_length=100)

    D_50: Optional[List[PositiveFloat]] = Field(None, min_length=1, max_length=100)


# =========================================================
# CPT COORDINATES
# =========================================================

class Coordinates(BaseModel):
    x: float
    y: float


# =========================================================
# FRICTION SETTINGS (GENERAL + CPT)
# =========================================================

FrictionStrategyAuto = Literal["lower_bound", "settlement_driven"]
FrictionStrategyManual = Literal["manual"]

class FrictionAuto(BaseModel):
    friction_range_strategy: FrictionStrategyAuto = "lower_bound"
    negative_friction: Optional[NonNegativeFloat] = None


class FrictionManual(BaseModel):
    friction_range_strategy: FrictionStrategyManual
    negative_friction_range_nap: List[float] = Field(..., min_length=2, max_length=2)
    positive_friction_range_nap: List[Union[float, Literal["ptl"]]] = Field(
        ..., min_length=2, max_length=2
    )


class FrictionManualPositiveOnly(BaseModel):
    friction_range_strategy: FrictionStrategyManual
    negative_friction: Optional[NonNegativeFloat] = None
    positive_friction_range_nap: List[Union[float, Literal["ptl"]]] = Field(
        ..., min_length=2, max_length=2
    )


FrictionSettings = Union[FrictionAuto, FrictionManual, FrictionManualPositiveOnly]


# =========================================================
# SINGLE CPT OBJECT
# =========================================================

class SoilProperty(BaseModel):
    cpt_data: CPTData
    layer_table_data: Optional[LayerTableData] = None

    ref_height: float
    test_id: str

    water_pressure: float = 0.00981
    coordinates: Optional[Coordinates] = None
    ocr: float = 1

    friction_settings: Optional[FrictionSettings] = None

    groundwater_level_nap: Optional[float] = None
    unique_id: Optional[str] = None


# =========================================================
# MATERIALS
# =========================================================

class RGBColor(BaseModel):
    r: Annotated[int, Field(ge=0, le=255)]
    g: Annotated[int, Field(ge=0, le=255)]
    b: Annotated[int, Field(ge=0, le=255)]


ColorType = Union[str, RGBColor]


class LinearElasticMaterial(BaseModel):
    name: str
    elastic_modulus: float
    color: Optional[ColorType] = None


class ElastoPlasticMaterial(BaseModel):
    name: str
    elastic_modulus: float
    yield_stress: NonNegativeFloat
    color: Optional[ColorType] = None


class BrittleMaterial(BaseModel):
    name: str
    elastic_modulus: float
    tensile_strength: NonNegativeFloat
    color: Optional[ColorType] = None


Material = Union[LinearElasticMaterial, ElastoPlasticMaterial, BrittleMaterial]


# =========================================================
# PILE GEOMETRY
# =========================================================

class RectangularComponent(BaseModel):
    outer_shape: Literal["rectangle", "rect"]
    secondary_dimension: Annotated[float, Field(ge=0.05, le=1.5)]
    tertiary_dimension: Optional[Annotated[float, Field(ge=0.05, le=1.5)]] = None
    length: Optional[NonNegativeFloat] = None
    material: Optional[str] = None


class RoundComponent(BaseModel):
    outer_shape: Literal["round"]
    diameter: Annotated[float, Field(ge=0.05, le=1.5)]
    length: Optional[NonNegativeFloat] = None
    material: Optional[str] = None


PileComponent = Union[RectangularComponent, RoundComponent]


class Geometry(BaseModel):
    components: List[PileComponent] = Field(..., min_length=1, max_length=2)


# =========================================================
# PILE TYPE
# =========================================================

StandardReference = Literal[
    "B1","B2","B3","B4","B5","B6","B7","B8",
    "S1","S2","S3","S4","S5","S6","S7",
    "H1","H2","MA1","MA2","MB1","MB2","MC","MD","ME","MF"
]

class StandardPile(BaseModel):
    reference: StandardReference


class PileType(BaseModel):
    standard_pile: Optional[StandardPile] = None
    custom_properties: Optional[dict] = None


class PileProperties(BaseModel):
    name: Optional[str] = None
    geometry: Geometry
    materials: Optional[List[Material]] = None
    pile_type: PileType


# =========================================================
# EXCAVATION
# =========================================================

class ExcavationConstant(BaseModel):
    stress_reduction_method: Literal["constant"]


class ExcavationBegemann(BaseModel):
    stress_reduction_method: Literal["begemann"]
    excavation_width: PositiveFloat
    excavation_edge_distance: NonNegativeFloat


ExcavationSettings = Union[ExcavationConstant, ExcavationBegemann]


# =========================================================
# NORMS
# =========================================================

class NormSettings(BaseModel):
    NEN99971_version: Literal["2017", "2025"] = "2017"
    CUR236_version: Literal["2023"] = "2023"


# =========================================================
# GENERAL INFO
# =========================================================

class GeneralInfo(BaseModel):
    project_name: str
    project_id: str
    author: str
    date: Optional[str] = None


# =========================================================
# ROOT MODEL
# =========================================================

class MultipleCPTReportInput(BaseModel):

    pile_tip_levels_nap: List[float] = Field(..., min_length=2)
    list_soil_properties: List[SoilProperty] = Field(..., min_length=1)

    pile_properties: PileProperties

    pile_load: Optional[float] = None
    rel_pile_load: UnitInterval = 0.7

    pile_head_level_nap: Optional[Union[float, Literal["surface"]]] = None

    excavation_depth_nap: Optional[float] = None
    excavation_param_t: Optional[Literal[1, 0.5]] = 1
    excavation_settings: Optional[ExcavationSettings] = None

    friction_settings: Optional[FrictionSettings] = None

    soil_load: float = 0
    gamma_f_nk: float = 1
    gamma_r_b: float = 1.2
    gamma_r_s: float = 1.2

    use_almere_rules: bool = False
    apply_qc3_reduction: Optional[bool] = None

    norms: Optional[NormSettings] = None

    stiff_construction: bool = False

    cpts_group: Optional[List[str]] = None

    general: GeneralInfo
