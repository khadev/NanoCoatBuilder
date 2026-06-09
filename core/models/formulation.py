"""Formulation data models."""

import uuid
from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from dataclasses import field
from core.models.ingredient import CoatingType, SynthesisMethod
from core.models.validation import ValidationRule


class FormulationItem(BaseModel):
    ingredient_name: str
    weight_grams: float = 0.0
    notes: str = ""


class SynthesisProtocol(BaseModel):
    method: SynthesisMethod
    steps: List[str]
    temperature_c: float
    time_hours: float
    stirring_speed_rpm: int
    sonication_minutes: int = 0
    curing_conditions: Optional[str] = None
    post_treatment: Optional[str] = None
    safety_notes: List[str] = field(default_factory=list)
    equipment_needed: List[str] = field(default_factory=list)


class PerformancePrediction(BaseModel):
    corrosion_rate_mm_year: Optional[float] = None
    adhesion_MPa: Optional[float] = None
    salt_spray_hours: Optional[int] = None
    water_vapor_transmission: Optional[float] = None
    theoretical_volume_solids: float = 0.0
    theoretical_voc: float = 0.0
    cost_per_liter: float = 0.0
    estimated_life_years: Optional[float] = None
    hardness_pencil: Optional[str] = None
    contact_angle_degrees: Optional[float] = None
    thermal_conductivity: Optional[float] = None
    youngs_modulus_GPa: Optional[float] = None


class FormulationRecord(BaseModel):
    unique_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    date: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    operator: str = ""
    coating_type: CoatingType = CoatingType.ANTI_CORROSION
    target_environment: str = "C5 (very high corrosivity)"
    synthesis_protocol: Optional[SynthesisProtocol] = None
    items: List[FormulationItem] = Field(default_factory=list)
    timestamp: float = Field(default_factory=datetime.now().timestamp)

    def total_weight(self) -> float:
        return sum(i.weight_grams for i in self.items)

    def get_display_name(self) -> str:
        dt = datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d %H:%M")
        return f"{self.name} ({self.date}) - {self.operator} [{dt}]"


class AnalysisResult(BaseModel):
    formulation: FormulationRecord
    total_weight_g: float
    total_cost: float
    performance: PerformancePrediction
    iso_compliance: List[str]
    iso_violations: List[Dict]
    validation_rules: List[ValidationRule] = Field(default_factory=list)
    references: List[Dict]
    synthesis_protocol: Optional[SynthesisProtocol] = None
    characterization_data: Dict = Field(default_factory=dict)
    statistical_analysis: Dict = Field(default_factory=dict)
    raw_data: Dict = Field(default_factory=dict)
    application_sector: str = Field(default="Industry / Manufacturing")