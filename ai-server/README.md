# 🤖 PlantForge AI Server

PlantForge의 식물 이미지 분석, 종 식별(Vision AI) 및 LLM 기반 맞춤형 식물 관리 가이드 생성을 담당하는 Flask 기반 마이크로서비스입니다.

---

## 📌 주요 역할
- **이미지 수신 및 전처리**: Express 백엔드로부터 전달받은 식물 이미지 파싱
- **종 식별 (Vision AI)**: 이미지 기반 식물 종, 학명, 일치 신뢰도(Confidence), 상위 후보군 추출
- **케어 가이드 생성 (LLM)**: 식별된 종의 특성에 맞는 맞춤형 가이드(물주기, 빛, 온도, 흙, 비료, 주의사항) 생성

---

## 🗂 디렉터리 구조

```text
ai-server/
├── app/
│   ├── main.py               # Flask 서버 앱 생성 및 엔트리포인트
│   ├── routes/
│   │   ├── __init__.py
│   │   └── identify.py       # POST /identify 라우트 블루프린트
│   ├── services/
│   │   ├── __init__.py
│   │   ├── vision_service.py # 이미지 분석 및 종 식별 스켈레톤
│   │   └── guide_service.py  # 식물 관리 가이드 생성 스켈레톤
│   └── models/
│       ├── __init__.py
│       └── schemas.py        # 응답 데이터 클래스 및 스키마
├── requirements.txt          # 파이썬 의존성 목록
├── .env.example              # 환경 변수 설정 템플릿
└── README.md
```

---

## ⚙️ API 명세

### 1. 헬스 체크
- **URL**: `GET /health` 또는 `GET /`
- **응답**:
```json
{
  "service": "PlantForge AI Server",
  "status": "online",
  "version": "1.0.0"
}
```

### 2. 식물 식별 및 가이드 요청
- **URL**: `POST /identify`
- **Content-Type**: `multipart/form-data`
- **Body**:
  - `image`: 식물 사진 파일 (JPG, PNG, WEBP)
- **응답 예시**:
```json
{
  "status": "success",
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
    }
  ],
  "care_guide": {
    "watering": "겉흙이 마르면 듬뿍 주세요 (보통 주 1~2회)",
    "light": "직사광선을 피한 밝은 간접광이 가장 이상적입니다",
    "temperature": "18~27°C (최저 13°C 이상 유지)",
    "soil": "배수가 원활한 관엽식물 전용 배양토 + 펄라이트 배합",
    "fertilizer": "봄~가을 성장기 동안 액체 비료를 월 1회 희석하여 공급",
    "notes": "반려동물 섭취 시 가벼운 독성이 있을 수 있습니다."
  }
}
```

---

## 🚀 로컬 실행 방법

```bash
# 1. 가상환경 생성 및 활성화
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac / Linux:
# source venv/bin/activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 환경 변수 설정
cp .env.example .env

# 4. 서버 구동
python run.py
# http://localhost:5000 에서 실행됩니다.
```
