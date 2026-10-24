"""Identification Route Blueprint"""
from flask import Blueprint, jsonify, request

from ..services.guide_service import GuideService
from ..services.vision_service import VisionService

identify_bp = Blueprint("identify", __name__)
vision_service = VisionService()
guide_service = GuideService()


@identify_bp.route("/identify", methods=["POST"])
def identify():
    """Receive one plant photo and return species candidates plus a care guide."""
    image_file = request.files.get("image")
    if image_file is None or not image_file.filename:
        return jsonify({
            "status": "error",
            "message": "식물 사진 파일을 업로드해 주세요."
        }), 400

    image_bytes = image_file.read()
    try:
        vision_result = vision_service.identify_plant(image_bytes, image_file.mimetype or "")
        care_guide = guide_service.generate_care_guide(
            species=vision_result.get("species", "Unknown"),
            common_name=vision_result.get("common_name", ""),
            scientific_name=vision_result.get("scientific_name", ""),
        )
    except ValueError as exc:
        return jsonify({"status": "error", "message": str(exc)}), 400
    except Exception as exc:
        return jsonify({
            "status": "error",
            "message": f"식물 식별 처리 중 오류가 발생했습니다: {exc}"
        }), 500

    return jsonify({
        "status": "success",
        "species": vision_result.get("species"),
        "common_name": vision_result.get("common_name"),
        "scientific_name": vision_result.get("scientific_name"),
        "confidence": vision_result.get("confidence"),
        "candidates": vision_result.get("candidates", []),
        "provider": vision_result.get("provider"),
        "analysis_note": vision_result.get("analysis_note", ""),
        "care_guide": care_guide,
    }), 200
