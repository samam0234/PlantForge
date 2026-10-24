"""PlantForge AI Schemas and Response Models"""
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

@dataclass
class CareGuide:
    watering: str
    light: str
    temperature: str
    soil: str
    fertilizer: str
    notes: str

@dataclass
class Candidate:
    species: str
    common_name: str
    scientific_name: str
    confidence: float

@dataclass
class PlantIdentificationResponse:
    species: str
    common_name: str
    scientific_name: str
    confidence: float
    candidates: List[Dict[str, Any]]
    care_guide: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
