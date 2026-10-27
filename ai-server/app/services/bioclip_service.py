"""Local zero-shot plant identification with BioCLIP (open_clip).

The photo is compared with the scientific names in plant_labels.LABELS.
Runs on CUDA when torch can see a GPU, otherwise on CPU. The model is
downloaded from Hugging Face on first use and then kept in memory.
"""
import io
import os
import threading
from typing import Any, Dict

from PIL import Image

from .plant_labels import LABELS

DEFAULT_MODEL = "hf-hub:imageomics/bioclip-2"
UNCERTAIN_BELOW = 0.35

_lock = threading.Lock()
_state: Dict[str, Any] = {}


def model_name() -> str:
    return os.getenv("BIOCLIP_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL


def available() -> bool:
    try:
        import open_clip  # noqa: F401
        import torch  # noqa: F401
    except ImportError:
        return False
    return True


def device_name() -> str:
    import torch

    return "cuda" if torch.cuda.is_available() else "cpu"


def _load() -> Dict[str, Any]:
    with _lock:
        if _state:
            return _state

        import open_clip
        import torch

        name = model_name()
        device = device_name()
        model, _, preprocess = open_clip.create_model_and_transforms(name)
        tokenizer = open_clip.get_tokenizer(name)
        model = model.to(device).eval()

        prompts = [f"a photo of {scientific}." for scientific, _ in LABELS]
        with torch.no_grad():
            tokens = tokenizer(prompts).to(device)
            text_features = model.encode_text(tokens)
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)

        _state.update(
            model=model,
            preprocess=preprocess,
            text_features=text_features,
            device=device,
            scale=float(model.logit_scale.exp().item()),
        )
        return _state


def identify(image_bytes: bytes) -> Dict[str, Any]:
    import torch

    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as exc:
        raise ValueError("이미지 파일을 열 수 없습니다. JPG, PNG, WEBP 파일인지 확인해 주세요.") from exc

    state = _load()
    device = state["device"]
    with torch.no_grad():
        batch = state["preprocess"](image).unsqueeze(0).to(device)
        features = state["model"].encode_image(batch)
        features = features / features.norm(dim=-1, keepdim=True)
        probs = (state["scale"] * features @ state["text_features"].T).softmax(dim=-1)[0]
        top = probs.topk(min(3, len(LABELS)))

    candidates = []
    for score, index in zip(top.values.tolist(), top.indices.tolist()):
        scientific, korean = LABELS[index]
        candidates.append({
            "species": scientific,
            "common_name": korean,
            "scientific_name": scientific,
            "confidence": round(score, 2),
        })

    best = candidates[0]
    note = f"BioCLIP({model_name().split('/')[-1]}, {device})로 후보 {len(LABELS)}종 중에서 식별했습니다."
    if best["confidence"] < UNCERTAIN_BELOW:
        note = "후보 목록에 없는 식물이거나 사진이 불명확할 수 있어 신뢰도가 낮습니다. " + note

    return {
        "species": best["species"],
        "common_name": best["common_name"],
        "scientific_name": best["scientific_name"],
        "confidence": best["confidence"],
        "candidates": candidates,
        "provider": "bioclip",
        "analysis_note": note,
    }
