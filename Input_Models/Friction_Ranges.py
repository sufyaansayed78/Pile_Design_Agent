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
    x: Optional[float] = Field(None, example=142892.19)
    y: Optional[float] = Field(None, example=470783.87)


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


class SoilProperties(BaseModel):
    cpt_data: CPTData
    layer_table_data: LayerTableData

    ref_height: Optional[float] = None
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
    def validate_attributes(self): 
        for i in range(len(self.soil_properties_list)): 
            soil_properties = self.soil_properties_list[i]
            layer_data = self.soil_properties_list[i].layer_table_data 
            if layer_data.thickness is None: 
                raise ValueError(f"Thickness data is required for CPT data at index {i+1} in CPT data list.")
            if soil_properties.ref_height is None: 
                raise ValueError(f"Reference height is required for CPT data at index {i+1} in CPT data list.")
            if soil_properties.test_id is None: 
                raise ValueError(f"Test ID is required for CPT data at index {i+1} in CPT data list.")
            if soil_properties.cpt_data.qc is None: 
                raise ValueError(f"qc data is required for CPT data at index {i+1} in CPT data list.")
            if soil_properties.cpt_data.depth is None: 
                raise ValueError(f"Depth data is required for CPT data at index {i+1} in CPT data list.")
            if len(soil_properties.cpt_data.qc) != len(soil_properties.cpt_data.depth): 
                raise ValueError(f"qc and depth data must be of the same length for CPT data at index {i+1} in CPT data list.")
            if layer_data.lower_boundary is None: 
                raise ValueError(f"Lower boundary data is required for CPT data at index {i+1} in CPT data list.")
            if layer_data.gamma_unsat is None: 
                raise ValueError(f"Dry unit weight data is required for CPT data at index {i+1} in CPT data list.")
            if layer_data.C_s and layer_data.C_p and len(layer_data.C_s) != len(layer_data.C_p):
                raise ValueError(f"C_s and C_p(Koppejan parameters) data must be of the same length for CPT data at index {i+1} in CPT data list.")
            if layer_data.gamma_sat is None: 
                raise ValueError(f"Saturated unit weight data is required for CPT data at index {i+1} in CPT data list.")
            if len(layer_data.gamma_unsat) != len(layer_data.gamma_sat):
                raise ValueError(f"Unsaturated and saturated unit weight data must be of the same length for CPT data at index {i+1} in CPT data list.")
            
            if layer_data.phi is None: 
                raise ValueError(f"Internal Friction angle data is required for CPT data at index {i+1} in CPT data list.")
            if layer_data.main_component is None: 
                raise ValueError(f"Main component data(gravel, sand, silt, clay, peat) is required for CPT data at index {i+1} in CPT data list.")
        return self
    
    


            
