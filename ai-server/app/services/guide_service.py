"""Care guide generation.

Source order (AI_PROVIDER=local skips both LLMs):
1. OpenAI when OPENAI_API_KEY is set and AI_PROVIDER is auto or openai
2. Ollama when OLLAMA_GUIDE_MODEL is set (OpenAI-compatible /v1 endpoint)
3. The Korean guide stored in the houseplant catalog
"""
import json
import os
from typing import Any, Dict, Optional

import requests

from .plant_catalog import guide_for
from .vision_service import _has_openai_key

GUIDE_KEYS = ("watering", "light", "temperature", "soil", "fertilizer", "notes", "seasonal_tip")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"


def _mode() -> str:
    return os.getenv("AI_PROVIDER", "auto").strip().lower()


def _ollama_model() -> str:
    return os.getenv("OLLAMA_GUIDE_MODEL", "").strip()


def _ollama_url() -> str:
    base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").strip().rstrip("/")
    return f"{base}/v1/chat/completions"


def _llm_target() -> Optional[Dict[str, Any]]:
    """Return the chat endpoint to use, or None to stay on the catalog guide."""
    mode = _mode()
    if mode == "local":
        return None
    if _has_openai_key() and mode in {"auto", "openai"}:
        return {
            "name": "openai",
            "url": OPENAI_URL,
            "headers": {"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY', '').strip()}"},
            "model": os.getenv("OPENAI_GUIDE_MODEL", "gpt-4o-mini"),
        }
    if _ollama_model():
        return {"name": "ollama", "url": _ollama_url(), "headers": {}, "model": _ollama_model()}
    return None


class GuideService:
    def generate_care_guide(self, species: str, common_name: str, scientific_name: str = "") -> Dict[str, Any]:
        fallback = guide_for(scientific_name, species, common_name)
        fallback["source"] = "catalog"

        target = _llm_target()
        if target is None:
            return fallback

        try:
            generated = self._from_llm(target, species, common_name, scientific_name)
        except Exception as exc:
            fallback["notes"] = f"LLM 가이드 생성에 실패해 카탈로그 가이드를 사용했습니다 ({exc}). " + fallback["notes"]
            return fallback

        merged = dict(fallback)
        for key in GUIDE_KEYS:
            value = generated.get(key)
            if isinstance(value, str) and value.strip():
                merged[key] = value.strip()
        merged["source"] = "llm"
        return merged

    def _from_llm(self, target: Dict[str, Any], species: str, common_name: str, scientific_name: str) -> Dict[str, Any]:
        label = common_name or species or scientific_name or "실내 식물"
        prompt = (
            f"식물 '{label}' (영문명: {species}, 학명: {scientific_name})의 실내 관리 가이드를 "
            "한국어 JSON으로만 작성하세요. 키는 watering, light, temperature, soil, fertilizer, "
            "notes, seasonal_tip 입니다. 각 값은 2문장 이내여야 하고, notes에는 반려동물 독성이나 "
            "과습처럼 실제로 주의할 점을 넣으세요."
        )
        response = requests.post(
            target["url"],
            headers={"Content-Type": "application/json", **target["headers"]},
            json={
                "model": target["model"],
                "temperature": 0.4,
                "response_format": {"type": "json_object"},
                "messages": [
                    {"role": "system", "content": "당신은 실내 식물 원예 전문가입니다. JSON만 반환합니다."},
                    {"role": "user", "content": prompt},
                ],
            },
            timeout=120 if target["name"] == "ollama" else 45,
        )
        if response.status_code >= 400:
            raise RuntimeError(f"가이드 API 오류 ({target['name']} {response.status_code})")
        content = response.json()["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            raise RuntimeError("가이드 응답 형식이 올바르지 않습니다.")
        return parsed
