"""Plant Care Guide Service Skeleton"""
import os
from typing import Dict, Any

class GuideService:
    """LLM 기반 맞춤형 식물 관리 가이드 생성 서비스 기초"""

    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "mock")

    def generate_care_guide(self, species: str, common_name: str) -> Dict[str, Any]:
        """
        식물 종 이름을 기반으로 물주기, 햇빛, 온도, 토양 등 관리 가이드 생성
        추후 OpenAI GPT, Claude, 로컬 LLM(Ollama) 등으로 확장
        """
        return {
            "watering": "겉흙이 마르면 듬뿍 주세요 (보통 주 1~2회, 겨울철엔 관수 주기 연장)",
            "light": "직사광선을 피한 밝은 간접광이 가장 이상적입니다",
            "temperature": "18~27°C (최저 13°C 이상 유지)",
            "soil": "배수가 원활한 관엽식물 전용 배양토 + 펄라이트 배합",
            "fertilizer": "봄~가을 성장기 동안 액체 비료를 월 1회 희석하여 공급",
            "notes": "잎에 먼지가 쌓이면 호흡을 방해하므로 주기적으로 닦아주세요. 반려동물 섭취 시 가벼운 독성이 있을 수 있습니다."
        }
