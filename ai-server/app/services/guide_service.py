"""Care guide generation.

Phase 2 uses the built-in catalog so every identification has a species-specific
Korean guide. An LLM provider is added in the collection phase.
"""
from typing import Any, Dict

from .plant_catalog import guide_for


class GuideService:
    def generate_care_guide(self, species: str, common_name: str, scientific_name: str = "") -> Dict[str, Any]:
        return guide_for(scientific_name, species, common_name)
