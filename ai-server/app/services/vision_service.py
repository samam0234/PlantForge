"""Plant identification from an uploaded image.

Provider selection (AI_PROVIDER):
- auto: OpenAI Vision when a real API key exists, otherwise the local catalog
- openai: try OpenAI Vision, then fall back to the local catalog
- local: color-feature match against the built-in houseplant catalog
"""
import base64
import io
import json
import os
from typing import Any, Dict, List

import requests
from PIL import Image

from .plant_catalog import PLANTS

WEIGHTS = {
    "green_ratio": 1.5,
    "brightness": 1.2,
    "saturation": 1.0,
    "contrast": 0.9,
    "warmth": 1.3,
}
LOCAL_NOTE = (
    "로컬 색상 카탈로그로 추정한 결과입니다. "
    "정확한 종 식별은 OPENAI_API_KEY를 설정한 뒤 AI_PROVIDER=auto 로 다시 분석하세요."
)


def _has_openai_key() -> bool:
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key or key.startswith("your_"):
        return False
    return True


def active_provider() -> str:
    mode = os.getenv("AI_PROVIDER", "auto").strip().lower()
    if mode == "local":
        return "local-catalog"
    if _has_openai_key() and mode in {"auto", "openai"}:
        return "openai-vision"
    return "local-catalog"


def provider_status() -> Dict[str, str]:
    mode = os.getenv("AI_PROVIDER", "auto").strip().lower()
    return {
        "configured": mode or "auto",
        "active": active_provider(),
        "vision_model": os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini"),
    }


def _features(image_bytes: bytes) -> Dict[str, float]:
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert("RGB")
    except Exception as exc:
        raise ValueError("이미지 파일을 열 수 없습니다. JPG, PNG, WEBP 파일인지 확인해 주세요.") from exc

    image.thumbnail((96, 96))
    pixels = list(image.getdata())
    if not pixels:
        raise ValueError("이미지에 분석할 픽셀이 없습니다.")

    green = 0
    brightness_sum = 0.0
    saturation_sum = 0.0
    warmth_sum = 0.0
    luminances: List[float] = []

    for red, green_ch, blue in pixels:
        if green_ch > red + 8 and green_ch > blue:
            green += 1
        luminance = (0.2126 * red + 0.7152 * green_ch + 0.0722 * blue) / 255
        luminances.append(luminance)
        brightness_sum += luminance
        peak = max(red, green_ch, blue)
        saturation_sum += 0 if peak == 0 else (peak - min(red, green_ch, blue)) / peak
        warmth_sum += (red - blue) / 255

    count = len(pixels)
    mean_luma = brightness_sum / count
    variance = sum((value - mean_luma) ** 2 for value in luminances) / count
    return {
        "green_ratio": green / count,
        "brightness": mean_luma,
        "saturation": saturation_sum / count,
        "contrast": variance ** 0.5,
        "warmth": warmth_sum / count,
    }


def _distance(features: Dict[str, float], profile: Dict[str, float]) -> float:
    total = 0.0
    for key, weight in WEIGHTS.items():
        total += weight * (features.get(key, 0) - profile.get(key, 0)) ** 2
    return total ** 0.5


def identify_local(image_bytes: bytes) -> Dict[str, Any]:
    features = _features(image_bytes)
    ranked = sorted(
        (( _distance(features, plant["profile"]), plant) for plant in PLANTS),
        key=lambda item: item[0],
    )
    best_distance, _best_plant = ranked[0]
    second_distance = ranked[1][0] if len(ranked) > 1 else best_distance + 0.2
    margin = max(0.0, second_distance - best_distance)
    confidence = 0.5 + min(0.4, margin * 1.6) - min(0.25, best_distance * 0.45)
    uncertain = best_distance > 0.42
    if uncertain:
        confidence = min(confidence, 0.58)
    confidence = max(0.34, min(0.9, confidence))

    candidates = []
    remaining = 1.0
    for index, (distance, plant) in enumerate(ranked[:3]):
        if index == 0:
            score = confidence
        else:
            score = max(0.05, min(remaining - 0.04, confidence * (0.72 ** index) * (second_distance / (distance + 1e-6))))
        remaining -= score
        candidates.append({
            "species": plant["species"],
            "common_name": plant["common_name"],
            "scientific_name": plant["scientific_name"],
            "confidence": round(score, 2),
        })

    top = candidates[0]
    note = LOCAL_NOTE
    if uncertain:
        note = "사진의 색 분포가 카탈로그와 멀리 떨어져 있어 신뢰도가 낮습니다. " + note

    return {
        "species": top["species"],
        "common_name": top["common_name"],
        "scientific_name": top["scientific_name"],
        "confidence": top["confidence"],
        "candidates": candidates,
        "provider": "local-catalog",
        "analysis_note": note,
    }


def _mime_from_bytes(image_bytes: bytes, mimetype: str) -> str:
    if mimetype in {"image/jpeg", "image/png", "image/webp"}:
        return mimetype
    header = image_bytes[:12]
    if header.startswith(b"\xff\xd8"):
        return "image/jpeg"
    if header.startswith(b"\x89PNG"):
        return "image/png"
    if header.startswith(b"RIFF") and image_bytes[8:12] == b"WEBP":
        return "image/webp"
    raise ValueError("지원하지 않는 파일 형식입니다. JPG, PNG, WEBP만 업로드할 수 있습니다.")


def identify_openai(image_bytes: bytes, mimetype: str) -> Dict[str, Any]:
    mime = _mime_from_bytes(image_bytes, mimetype or "")
    encoded = base64.b64encode(image_bytes).decode("ascii")
    model = os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")
    prompt = (
        "당신은 실내 식물 분류 전문가입니다. 사진 속 식물을 식별하고 JSON만 반환하세요. "
        "키: species(영문 일반명), common_name(한국어), scientific_name(학명), "
        "confidence(0과 1 사이 숫자), candidates(가능성 높은 순 3개, 각 항목은 같은 키). "
        "식물이 아니거나 판별이 어려우면 confidence를 0.4 이하로 두고 "
        "common_name은 '식별이 어려운 식물'로 하세요. 설명 문장은 넣지 마세요."
    )
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY', '').strip()}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{mime};base64,{encoded}"},
                        },
                    ],
                }
            ],
        },
        timeout=45,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"Vision API 오류 ({response.status_code})")

    content = response.json()["choices"][0]["message"]["content"]
    parsed = json.loads(content)
    candidates = []
    for item in (parsed.get("candidates") or [])[:3]:
        candidates.append({
            "species": item.get("species") or parsed.get("species") or "Unknown",
            "common_name": item.get("common_name") or "",
            "scientific_name": item.get("scientific_name") or "",
            "confidence": float(item.get("confidence") or 0),
        })
    if not candidates:
        candidates.append({
            "species": parsed.get("species") or "Unknown",
            "common_name": parsed.get("common_name") or "",
            "scientific_name": parsed.get("scientific_name") or "",
            "confidence": float(parsed.get("confidence") or 0),
        })

    return {
        "species": parsed.get("species") or candidates[0]["species"],
        "common_name": parsed.get("common_name") or candidates[0]["common_name"],
        "scientific_name": parsed.get("scientific_name") or candidates[0]["scientific_name"],
        "confidence": round(float(parsed.get("confidence") or candidates[0]["confidence"] or 0), 2),
        "candidates": candidates,
        "provider": "openai-vision",
        "analysis_note": f"OpenAI Vision({model})으로 식별했습니다.",
    }


class VisionService:
    def identify_plant(self, image_bytes: bytes, mimetype: str = "") -> Dict[str, Any]:
        if not image_bytes:
            raise ValueError("식물 사진 파일이 비어 있습니다.")
        if len(image_bytes) > 10 * 1024 * 1024:
            raise ValueError("이미지 용량은 10MB 이하여야 합니다.")
        _mime_from_bytes(image_bytes, mimetype or "")

        mode = os.getenv("AI_PROVIDER", "auto").strip().lower()
        if mode != "local" and _has_openai_key():
            try:
                return identify_openai(image_bytes, mimetype)
            except Exception as exc:
                local = identify_local(image_bytes)
                local["analysis_note"] = (
                    f"Vision API 호출에 실패해 로컬 카탈로그로 대체했습니다 ({exc}). "
                    + LOCAL_NOTE
                )
                local["provider"] = "local-catalog"
                return local

        if mode == "openai" and not _has_openai_key():
            local = identify_local(image_bytes)
            local["analysis_note"] = "OPENAI_API_KEY가 없어 로컬 카탈로그로 식별했습니다. " + LOCAL_NOTE
            return local

        return identify_local(image_bytes)
