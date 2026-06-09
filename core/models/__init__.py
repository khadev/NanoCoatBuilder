"""Data models for NanoCoatBuilder."""

from pydantic import BaseModel


class FormulationItem(BaseModel):
    ingredient_name: str
    weight_grams: float = 0.0
    notes: str = ""


class ValidationRule(BaseModel):
    category: str
    severity: str
    message: str
    recommendation: str
    standard: str = ""


__all__ = ['FormulationItem', 'ValidationRule']