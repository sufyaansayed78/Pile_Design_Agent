from typing import List, Optional, Literal, Union, Annotated
from pydantic import BaseModel, Field, model_validator


# ---------------------------
# Primitive constrained types
# ---------------------------

PositiveFloat = Annotated[float, Field(gt=0)]
NonNegativeFloat = Annotated[float, Field(ge=0)]


# ---------------------------
# Sub Models
# ---------------------------

class Coordinates(BaseModel):
    x: float = Field(..., example=142892.19)
    y: float = Field(..., example=470783.87)


class CPTData(BaseModel):
    qc: List[NonNegativeFloat] = Field(
        ...,
        description="Cone resistance [MPa]"
    )

    depth: List[NonNegativeFloat] = Field(
        ...,
        description="Depth below service level [m]"
    )

    u: Optional[List[float]] = Field(
        default=None,
        description="Pore water pressure [MPa]. Must be of the same length as qc and depth if provided."
    )


class LayerTableData(BaseModel):
    thickness: Optional[List[PositiveFloat]] = None

    lower_boundary: List[NonNegativeFloat] = Field(
        ...,
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

    gamma_unsat: List[NonNegativeFloat] = Field(
        ..., # Required field
        min_length=1,
        max_length=100
    )

    gamma_sat: List[NonNegativeFloat] = Field(
        ...,
        min_length=1,
        max_length=100
    )

    phi: List[NonNegativeFloat] = Field(
        ...,
        min_length=1,
        max_length=100
    )

    main_component: List[
        Literal["gravel", "sand", "silt", "clay", "peat"]
    ] = Field(
        ...,
        min_length=1,
        max_length=100
    )

    D_50: Optional[List[PositiveFloat]] = Field(
        default=None,
        min_length=1,
        max_length=100
    )


class SoilProperties(BaseModel):
    cpt_data: CPTData
    layer_table_data: LayerTableData

    ref_height: float
    test_id: str

    water_pressure: float = Field(
        default=0.00981,
        description="Water unit weight [MPa]"
    )

    coordinates: Coordinates

    ocr: float = Field(
        default=1,
        description="Over-consolidation ratio"
    )


class LowerBound_Friction(BaseModel):
    soil_properties_list: List[SoilProperties] = Field(
        ...,
        min_length=1
    )

    pile_tip_level_nap: float

    pile_head_level_nap: Optional[
        Union[float, Literal["surface"]]
    ] = "surface"

    excavation_depth_nap: Optional[float] = None

    @model_validator(mode="after") 
    def validate_thickness(self): 
        for i in range(len(self.soil_properties_list)): 
            layer_data = self.soil_properties_list[i].layer_table_data 
            if layer_data.thickness is None: 
                raise ValueError(f"Thickness data is required for CPT data at index {i+1} in CPT data list.")
        return self
    
            
