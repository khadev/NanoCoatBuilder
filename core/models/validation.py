"""Validation models."""

from pydantic import BaseModel
from typing import Optional


class ValidationRule(BaseModel):
    """Stores validation rule violations."""
    category: str
    severity: str  # error, warning, info
    message: str
    recommendation: str
    standard: Optional[str] = None