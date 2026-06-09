"""Ingredient data models."""

from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum
from dataclasses import field


class CoatingType(str, Enum):
    ANTI_CORROSION = "Anti-corrosion"
    EROSION_RESISTANT = "Erosion-resistant"
    THERMAL_BARRIER = "Thermal barrier"
    ANTIFOULING = "Antifouling"
    WEAR_RESISTANT = "Wear-resistant"
    NANOCOMPOSITE = "Nanocomposite"
    SMART_COATING = "Smart coating"
    SELF_HEALING = "Self-healing"
    SPRAY_COATING = "Spray coating"
    DIP_COATING = "Dip coating"


class SynthesisMethod(str, Enum):
    SOLUTION_BLENDING = "Solution blending"
    MELT_BLENDING = "Melt blending"
    IN_SITU_POLYMERIZATION = "In-situ polymerization"
    SOL_GEL = "Sol-gel process"
    ELECTRODEPOSITION = "Electrodeposition"
    SPRAY_COATING = "Spray coating"
    DIP_COATING = "Dip coating"
    SPIN_COATING = "Spin coating"


class ChemicalProperty(BaseModel):
    density: float = Field(0.0, description="g/cm³")
    viscosity: float = Field(0.0, description="cP at 25°C")
    solids_content: float = Field(0.0, description="% weight solids")
    voc: float = Field(0.0, description="g/L")
    cost_per_kg: float = Field(0.0, description="€/kg")


class Nanocomposite(BaseModel):
    name: str
    type: str
    particle_size_nm: float
    aspect_ratio: Optional[float] = None
    surface_area_m2_g: float
    purity_percent: float
    functionalization: Optional[str] = None
    properties: ChemicalProperty = Field(default_factory=ChemicalProperty)
    dispersion_method: str = "Ultrasonication"
    recommended_loading_wt: float = 1.0
    max_loading_wt: float = 5.0
    min_loading_wt: float = 0.1


class Polymer(BaseModel):
    name: str
    bigsmiles: Optional[str] = None
    chemical_properties: ChemicalProperty = Field(default_factory=ChemicalProperty)
    tg: float = Field(0.0, description="Glass transition temperature (°C)")
    solubility_parameter: float = Field(0.0, description="Hildebrand parameter (MPa^0.5)")
    molecular_weight: float = 0.0
    polydispersity: float = 1.0


class Ingredient(BaseModel):
    name: str
    category: str
    formula: str = ""
    polymer: Optional[Polymer] = None
    nanocomposite: Optional[Nanocomposite] = None
    properties: ChemicalProperty = Field(default_factory=ChemicalProperty)
    synthesis_methods: List[SynthesisMethod] = field(default_factory=list)
    typical_loading_wt: float = 0.0
    min_loading_wt: float = 0.0
    max_loading_wt: float = 100.0
    notes: str = ""