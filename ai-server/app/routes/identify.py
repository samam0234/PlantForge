"""Identification Route Blueprint"""
from flask import Blueprint, request, jsonify
from ..services.vision_service import VisionService
from ..services.guide_service import GuideService

identify_bp = Blueprint("identify", __name__)
vision_service = VisionService()
guide_service = GuideService()

@identify_bp.route("/identify", methods=["POST"])
def identify():
    """
    식물 이미지 식별 및 관리 가이드 생성 엔드포인트
    multipart/form-data (image 필드) 또는 JSON payload 지원
    """
    try:
        image_file = request.files.get("image")
        
        # 1. Vision 분석으로 식물 종 식별
        vision_result = vision_service.identify_plant(image_file)
        
        # 2. 식별된 종 기반 케어 가이드 생성
        care_guide = guide_service.generate_care_guide(
            species=vision_result.get("species", "Unknown"),
            common_name=vision_result.get("common_name", "")
        )
        
        # 3. 통합 결과 반환
        response_data = {
            "status": "success",
            "species": vision_result.get("species"),
            "common_name": vision_result.get("common_name"),
            "scientific_name": vision_result.get("scientific_name"),
            "confidence": vision_result.get("confidence"),
            "candidates": vision_result.get("candidates", []),
            "care_guide": care_guide
        }
        
        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"식물 식별 처리 중 오류가 발생했습니다: {str(e)}"
        }), 500
