"""Plant Identification Vision Service Skeleton"""
import os
from typing import Dict, Any, List

class VisionService:
    """식물 이미지 분석 및 종 식별 서비스 기초"""

    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "mock")

    def identify_plant(self, image_bytes_or_path: Any) -> Dict[str, Any]:
        """
        이미지 데이터를 기반으로 식물 종 식별
        추후 OpenAI Vision, PlantNet API, Hugging Face 모델 연동 가능
        기본 스켈레톤에서는 표준 식별 결과 구조를 반환
        """
        # 기본 식별 샘플 데이터 (몬스테라 기준)
        return {
            "species": "Monstera Deliciosa",
            "common_name": "몬스테라 델리시오사",
            "scientific_name": "Monstera deliciosa",
            "confidence": 0.94,
            "candidates": [
                {
                    "species": "Monstera Deliciosa",
                    "common_name": "몬스테라 델리시오사",
                    "scientific_name": "Monstera deliciosa",
                    "confidence": 0.94
                },
                {
                    "species": "Epipremnum aureum",
                    "common_name": "스킨답서스 (골든 포토스)",
                    "scientific_name": "Epipremnum aureum",
                    "confidence": 0.78
                },
                {
                    "species": "Philodendron hederaceum",
                    "common_name": "하트리프 필로덴드론",
                    "scientific_name": "Philodendron hederaceum",
                    "confidence": 0.65
                }
            ]
        }
