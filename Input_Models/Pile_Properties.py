from typing import Annotated, List, Literal, Optional, Union
from pydantic import BaseModel, Field, conlist, model_validator


# ----------------------------
# Shared Sub-Models
# ----------------------------

# class Material(BaseModel):
#     name: Optional[str] = None
#     model: Optional[str] = None  # e.g. "linear-elastic", "elasto-plastic"

class PrimaryDimension(BaseModel):
    length : Optional[float] = None




# ----------------------------
# Rectangular Component
# ----------------------------

# class RectangularComponent(BaseModel):
#     outer_shape: Literal["rectangle"]
#     material: Optional[str] = None
#     primary_dimension: Optional[PrimaryDimension] = None
#     secondary_dimension: float = Field(..., gt=0, description="Secondary dimension needs to be explicitly mentioned in the prompt")
#     tertiary_dimension: float | None = None


# ----------------------------
# Round Component
# ----------------------------

# class RoundComponent(BaseModel):
#     outer_shape: Literal["round"]
#     material: Optional[str] = None
#     primary_dimension: float = Field(..., gt=0, description="Primary dimension (length) of the round component")
#     diameter: float = Field(..., gt=0, description="Diameter of the round component")   


# ----------------------------
# Discriminated Union (oneOf)
# ----------------------------
# PileComponent = Annotated[
#     Union[RectangularComponent, RoundComponent],
#     Field(discriminator="outer_shape")
# ]
#----------------------------------------------------
#New component 
class PileComponent(BaseModel):
    outer_shape: Literal["rectangle", "round"]  # "rectangle" or "round"
    material: Optional[str] = None
    primary_dimension: Optional[PrimaryDimension] = None
    secondary_dimension: float = None 
    tertiary_dimension: Optional[float] = None
    diameter: Optional[float] = Field(None, gt=0, description="Diameter of the round component (only for  outer_shape == 'round')") 

# ----------------------------
# Main Geometry Model
# ----------------------------

class PileGeometry(BaseModel):
    components: List[PileComponent] = Field(
        min_length=1,
        max_length=2,description=""
    )
    phi: float = Field(
        default=40,
        ge=0,
        description="Degree of internal friction [deg] at pile-tip-level"
    )

    @model_validator(mode="after")
    def validate_same_outer_shape(self):
        first_component = self.components[0]

        if getattr(first_component, "primary_dimension", None) is not None:
            raise ValueError(
                "The first component must not contain 'primary_dimension'"
            )
        
        for component in self.components:
            if component.secondary_dimension == 0.0 :
                raise ValueError(f"The secondary dimension of the component : {component}  is null ")
               
        
        shapes = {component.outer_shape for component in self.components}
        if len(shapes) > 1:
            raise ValueError("All components must have the same outer_shape")
        return self


#`----------------------------------------------------------------------------------------------`
class Norms(BaseModel):
    NEN99971_version: Literal["2017", "2025"] = "2017"
    CUR236_version: Literal["2023"] = "2023"

class NNORMS(BaseModel):
    norms : Norms
# ---------------------------------
# NEN9997-1 Standard Pile
# ---------------------------------

class NENStandardPile(BaseModel):
    #standard: Literal["NEN9997-1"]
    reference: Literal[
        "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8",
        "S1", "S2", "S3", "S4", "S5", "S6", "S7",
        "H1", "H2",
        "MA1", "MA2", "MB1", "MB2",
        "MC", "MD", "ME", "MF"
    ] = None


# ---------------------------------
# CUR-236 Standard Pile
# ---------------------------------

class CURStandardPile(BaseModel):
    #standard: Literal["CUR-236"]
    reference: Literal[
        "AA1", "AA2", "AB1", "AB2",
        "AC", "AD", "AE"
    ] = None


# ---------------------------------
# Discriminated Union (oneOf)
# ---------------------------------

PileProperties =Union[NENStandardPile, CURStandardPile]
    #Field(discriminator="standard")



# ---------------------------------
# Main Request Model
# ---------------------------------
# class PileProperties(BaseModel):
#     reference : str 
    
class PilePropertiesType(BaseModel):
    norms: NNORMS
    pile_properties: PileProperties

    # @model_validator(mode='after')
    # def validate(self):
    #     if self.pile_properties.reference not in [
    #     "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8",
    #     "S1", "S2", "S3", "S4", "S5", "S6", "S7",
    #     "H1", "H2",
    #     "MA1", "MA2", "MB1", "MB2",
    #     "MC", "MD", "ME", "MF","AA1", "AA2", "AB1", "AB2","AC", "AD", "AE"]:
    #         raise ValueError("""The reference value provided is invalid. The reference value should be one of these : [
    #     "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8",
    #     "S1", "S2", "S3", "S4", "S5", "S6", "S7",
    #     "H1", "H2",
    #     "MA1", "MA2", "MB1", "MB2",
    #     "MC", "MD", "ME", "MF","AA1", "AA2", "AB1", "AB2","AC", "AD", "AE"] """)


    




