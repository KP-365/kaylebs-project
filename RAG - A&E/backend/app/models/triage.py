"""
Triage data models
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

from enum import Enum


class UrgencyBand(str, Enum):
    """Urgency band classification"""
    RED = "red"
    AMBER = "amber"
    GREEN = "green"


class RedFlag(BaseModel):
    """Red flag indicator"""
    flag: str = Field(..., description="Description of the red flag")
    severity: str = Field(..., description="Severity: red, amber, or green")


class TriageRequest(BaseModel):
    """Request model for triage assessment"""
    age: int = Field(..., ge=18, le=120, description="Patient age (must be 18+)")
    sex: str = Field(..., pattern="^(M|F|Other)$", description="Patient sex")
    chief_complaint: str = Field(
        ...,
        description="Main complaint: chest_pain, shortness_of_breath, abdominal_pain, headache, fever_infection, injury"
    )
    answers: Optional[Dict[str, any]] = Field(
        default_factory=dict,
        description="Answers to triage questions"
    )
    patient_id: Optional[str] = Field(None, description="Optional patient identifier")


class TriageResponse(BaseModel):
    """Response model for triage assessment"""
    urgency: UrgencyBand = Field(..., description="Urgency band: red, amber, or green")
    red_flags: List[RedFlag] = Field(default_factory=list, description="List of red flags detected")
    explanation: str = Field(..., description="Human-readable explanation")
    assessed_at: datetime = Field(..., description="Timestamp of assessment")
    model_version: str = Field(..., description="Version of the model/rules used")
    rule_version: str = Field(..., description="Version of the rules used")


