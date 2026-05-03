from typing import Any, Dict, List, Literal, Optional, Tuple, Union
from Input_Models.Friction_Ranges import NonNegativeFloat
from Input_Models.Report import PositiveFloat
from pydantic import BaseModel, Field, conlist, confloat

# --- 1. EXCAVATION SETTINGS ---

class ConstantExcavationSettings(BaseModel):
    stress_reduction_method: Literal["constant"] = "constant"

class BegemannExcavationSettings(BaseModel):
    stress_reduction_method: Literal["begemann"]
    excavation_width: float = Field(
        ..., 
        gt=0, 
        description="Width of the excavation in meters (must be > 0)."
    )
    excavation_edge_distance: float = Field(
        ..., 
        ge=0, 
        description="Distance from pile centerline to edge in meters."
    )

ExcavationSettings = Union[ConstantExcavationSettings, BegemannExcavationSettings]


# --- 2. PILE GRID ---

class PileGrid(BaseModel):
    locations: List[List[float]] = Field(
        ..., 
        min_length=2, 
        description="List of X and Y coordinate pairs."
    )
    pile_index: int = Field(
        0, 
        ge=0, 
        description="Pile location used by given an index of the list."
    )


# --- 3. OVERRULE XI CORRELATION FACTORS ---

class OverruleXiFactors(BaseModel):
    xi3: float
    xi4: float
    xi4_single: float

OverruleXi = Union[float, OverruleXiFactors]


# --- 4. PILE PROPERTIES: MATERIALS ---

class RGBColor(BaseModel):
    r: int = Field(..., ge=0, le=255)
    g: int = Field(..., ge=0, le=255)
    b: int = Field(..., ge=0, le=255)

ColorType = Union[str, RGBColor]

class MaterialBase(BaseModel):
    name: str = Field(..., description="Unique name of the material.")
    elastic_modulus: float = Field(..., description="Young's modulus (MPa).")
    color: ColorType

class LinearElasticMaterial(MaterialBase):
    pass # Follows base strictly

class ElastoPlasticMaterial(MaterialBase):
    yield_stress: float = Field(..., ge=0, description="Yield stress in MPa.")

class ElasticBrittleMaterial(MaterialBase):
    tensile_strength: float = Field(..., ge=0, description="Tensile stress in kN/m2.")

Material = Union[LinearElasticMaterial, ElastoPlasticMaterial, ElasticBrittleMaterial]


# --- 5. PILE PROPERTIES: GEOMETRY ---

class RectangularComponent(BaseModel):
    outer_shape: Literal["rectangle"] = "rectangle"
    primary_dimension: Optional[Dict[str, Any]] = None
    secondary_dimension: Optional[List[Any]] = None
    tertiary_dimension: Optional[List[Any]] = None
    material: Optional[List[Any]] = None

class RoundComponent(BaseModel):
    outer_shape: Literal["round"] = "round"
    primary_dimension: Optional[Dict[str, Any]] = None
    diameter: Optional[List[Any]] = None
    material: Optional[List[Any]] = None

Component = Union[RectangularComponent, RoundComponent]

class PileGeometry(BaseModel):
    components: List[Component] = Field(..., min_length=1, max_length=2)
    materials: Optional[List[Material]] = None


# --- 6. PILE PROPERTIES: TYPES & CUSTOM SPECS ---

class PileCustomProperties(BaseModel):
    pile_tip_factor_s: Optional[float] = None
    beta_p: Optional[float] = None

class StandardPileReference(BaseModel):
    reference: Literal[
        "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", 
        "S1", "S2", "S4", "S3", "S5", "S6", "S7", 
        "H1", "H2", "MA1", "MA2", "MB1", "MB2", "MC", "MD", "ME", "MF"
    ]


class AlphaSClayDepends(BaseModel):
    use_constant_value: Literal[False]


class AlphaSClayConstant(BaseModel):
    use_constant_value: Literal[True]
    constant_value: float


AlphaSClay = Union[AlphaSClayDepends, AlphaSClayConstant]

class PileTypeCustomProperties(BaseModel):
    """Properties shared between standard and custom pile definitions."""
    alpha_s_sand: Optional[float] = None
    alpha_s_clay: Optional[AlphaSClay] = None
    alpha_p: Optional[float] = None
    alpha_t_sand: Optional[float] = None
    settlement_curve: Optional[int] = None
    negative_fr_delta_factor: Optional[int] = None
    adhesion: Optional[int] = None
    is_auger: bool  
    diameter_method: Literal["section", "default", "diameter_micro"]
    installation_method: Literal["driven", "screwed", "excavated", "vibrated", "pressed", "jetted"]
    is_low_vibrating:bool
    is_prefab: bool
    is_open_ended: bool
    qc_z_a_lesser_1m: int = Field(12, ge=0, description="Maximum cone resistance qc value allowed for layers with thickness < 1m in the calculation of positive skin friction resistance.")
    qc_z_a_greater_1m: int = Field(15, ge=0, description="Maximum cone resistance qc value allowed for layers with thickness >= 1m in the calculation of positive skin friction resistance.")
    qb_max_limit: int = Field(15, ge=0, description="Maximum value allowed for the pile tip resistance qb_max obtained according to NEN 9997-1+C2:2017 7.6.2.3.(10)(e).")

class StandardPileType(BaseModel):
    standard_pile: StandardPileReference
    custom_properties: Optional[PileTypeCustomProperties] = None

class CustomPileType(BaseModel):
    custom_properties: PileTypeCustomProperties

PileType = Union[StandardPileType, CustomPileType]

class PileProperties(BaseModel):
    name: str
    geometry: PileGeometry
    custom_properties: Optional[PileCustomProperties] = None
    pile_type: PileType


# --- 7. SOIL PROPERTIES ---

class CPTData(BaseModel):
    qc: Optional[Annotated[List[NonNegativeFloat], Field(description="Cone resistance [MPa]")]] = Field(
        default=None
    )

    depth: Optional[List[NonNegativeFloat]] = Field(
        default=None,
        description="Depth below service level [m]"
    )

    u: Optional[List[float]] = Field(
        default=None,
        description="Pore water pressure [MPa]. Must be of the same length as qc and depth if provided."
    )

class LayerTableData(BaseModel):
    thickness: Optional[List[PositiveFloat]] = None

    lower_boundary: Optional[List[NonNegativeFloat]] = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    C_s: Optional[List[PositiveFloat]] = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    C_p: Optional[List[PositiveFloat]] = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    tau_mob_max: Optional[List[PositiveFloat]] = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    qc_gem_failure_test: Optional[List[PositiveFloat]] = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    gamma_unsat: Optional[List[NonNegativeFloat]] = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    gamma_sat: Optional[List[NonNegativeFloat]] = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    phi: Optional[List[NonNegativeFloat]] = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    main_component: Optional[List[
        Literal["gravel", "sand", "silt", "clay", "peat"]
    ]] = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    D_50: Optional[List[PositiveFloat]] = Field(
        default=None,
        min_length=1,
        max_length=100
    )

class Coordinates(BaseModel):
    x: Optional[float] = Field(None, example=142892.19)
    y: Optional[float] = Field(None, example=470783.87)

class SoilPropertyProfile(BaseModel):
    cpt_data: CPTData
    layer_table_data: LayerTableData
    ref_height: float = Field(..., description="Surface height (m).")
    test_id: str
    water_pressure: Optional[float] = 0.00981
    coordinates: Optional[Coordinates] = None
    ocr: Optional[float] = Field(1.0, description="Over-consolidation ratio.")
    groundwater_level_nap: Optional[float] = Field(None, description="GWL relative to NAP.")
    top_of_tension_zone_nap: Optional[float] = None
    unique_id: Optional[str] = None

class Norms(BaseModel):
    NEN99971_version: Literal["2017", "2025"] = "2017"
    CUR236_version: Literal["2023"] = "2023"
# --- 8. ROOT API ENDPOINT SCHEMA ---

class UpliftSingleNEN(BaseModel):
    norms: Optional[Dict[str, Any]] = None
    pile_tip_levels_nap: List[float] = Field(..., min_length=1)
    
    excavation_settings: Optional[ExcavationSettings] = None
    pile_grid: Optional[PileGrid] = None
    pile_head_level_nap: Union[Literal["surface"], float]
    
    excavation_depth_nap: Optional[float] = None
    top_of_tension_zone_nap: Optional[float] = None
    
    void_ratio_max: float = Field(0.8, gt=0)
    void_ratio_min: float = Field(0.4, gt=0)
    
    pile_load_sls_max: float = Field(1.0, gt=0)
    pile_load_sls_min: float = Field(1.0)
    
    gamma_s_t: float = 1.35
    overrule_xi: Union[Optional[OverruleXi],int] = None
    
    pile_properties: List[PileProperties] = Field(..., min_length=1)
    
    construction_sequence: Literal["cpt-pile", "pile-cpt"] = "cpt-pile"
    excavation_param_t: Literal[1.0,0.5] = 1.0
    
    list_soil_properties: List[SoilPropertyProfile] = Field(..., min_length=1)
    compute_stiffness: bool = True