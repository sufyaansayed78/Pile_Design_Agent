from pydantic import BaseModel
from typing import List, Optional
class PileShape(BaseModel):
    pile_tip_factor_s: float
    beta_p: float
    

class ClayAlphaModel(BaseModel):
    use_constant_value: bool
    #constant_value: float


class PileTypePropertiesOutput(BaseModel):
    alpha_p: float
    alpha_s_sand: float
    alpha_s_clay: ClayAlphaModel
    alpha_t_sand: float
    alpha_t_clay: ClayAlphaModel

    is_auger: bool
    is_low_vibrating: bool
    is_prefab: bool
    is_open_ended: bool

    negative_fr_delta_factor: float
    settlement_curve: float
    qc_z_a_lesser_1m: float
    qc_z_a_greater_1m: float
    qb_max_limit: float

    adhesion: Optional[float]

    installation_method: str
    diameter_method: str

class LowerBoundFriction(BaseModel):
    id: str 

class single_Uplift_Calculation_NEN(BaseModel):
    id : str

class single_Uplift_Calculation_CURR(BaseModel):
    id : str

class Multiple_Uplift_Calculation_NEN(BaseModel):
    id : str

class Multiple_Uplift_Calculation_CURR(BaseModel):
    id : str

class Bearing_Calculation_result(BaseModel):
    id : str

class Bearing_alculation_report(BaseModel):
    id : str
     
class Grouper_report(BaseModel):
    id : str

class Group_CPTs(BaseModel):
    id : str

class Group_metrics(BaseModel):
    id : str


#===========================Lower Bound Friction =========================

class LoadComponent(BaseModel):
    positive_top: float
    positive_bottom: float
    negative_top: float
    negative_bottom: float

class LowerBoundFrictionOutput(BaseModel):
    data : List[LoadComponent]





