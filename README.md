# 🌱 PlantForge

> **AI 기반 식물 식별 및 관리 가이드 플랫폼**  
> *"사진 한 장으로 식물을 알아보고, 제대로 키우는 방법을 바로 알 수 있는 경험"*

---

## 📖 프로젝트 개요

**PlantForge**는 식물의 사진을 업로드하면 AI가 해당 식물의 종을 식별하고, 맞춤형 관리 가이드(물주기, 채광, 적정 온도, 분갈이/토양, 비료 주기, 반려동물 주의사항 등)를 즉시 제공하는 3계층 아키텍처 웹 서비스입니다.

- **버전**: v1.0
- **작성일**: 2026-10-25
- **유형**: 미니 프로젝트 (Vibe Coding 대상)
- **SSOT 규칙 문서**: [AGENTS.md](./AGENTS.md)

---

## 🏗 시스템 아키텍처

```
┌─────────────────────────┐         ┌─────────────────────────┐         ┌─────────────────────────┐
│     Svelte (Vite)       │ ──────▶ │       Express.js        │ ──────▶ │      Flask (Python)     │
│       Frontend          │ ◀────── │      Orchestrator       │ ◀────── │        AI Server        │
│  (업로드 · 결과 · 정원) │         │ (Upload, DB, Route API) │         │ (Vision / 카탈로그 가이드) │
│       Port: 5173        │         │       Port: 3000        │         │       Port: 5000        │
└─────────────────────────┘         └─────────────────────────┘         └─────────────────────────┘
                                                 │
                                                 ▼
                                    ┌─────────────────────────┐
                                    │      SQLite DB          │
                                    │   (plantforge.db)       │
                                    └─────────────────────────┘
```

---

## 📁 디렉터리 구조

```text
plantforge/
├── frontend/                     # Svelte + Vite (UI 및 시각적 컴포넌트 프리뷰)
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/       # ImageUpload, IdentificationResult, CareGuide, PlantCollection
│   │   │   ├── api/              # plant.js (Express API 클라이언트)
│   │   │   └── stores/           # plants.js (식물 상태 저장소)
│   │   ├── App.svelte            # 메인 시각적 대시보드 뷰
│   │   ├── main.js
│   │   └── app.css
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
│
├── backend/                      # Express.js (오케스트레이션 및 CRUD API)
│   ├── src/
│   │   ├── routes/               # identify.js, plants.js
│   │   ├── services/             # aiClient.js (Flask 식별 호출)
│   │   ├── db/                   # database.js (SQLite 스키마 초기화)
│   │   ├── middleware/           # upload.js (Multer 파일 업로드)
│   │   └── app.js                # Express 엔트리포인트
│   ├── uploads/                  # 업로드 임시 저장소
│   ├── package.json
│   ├── .env.example
│   └── README.md
│
├── ai-server/                    # Flask (AI 이미지 분석 및 가이드 생성)
│   ├── app/
│   │   ├── routes/               # identify.py (/identify 엔드포인트)
│   │   ├── services/             # vision_service.py, guide_service.py, plant_catalog.py
│   │   ├── models/               # schemas.py
│   │   └── main.py               # Flask 엔트리포인트
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── Docs/                         # 인수인계 및 프로젝트 문서 표준 폴더
│   ├── plan/                     # 기획서 및 인수인계 문서
│   ├── Architecture/             # 시스템 아키텍처 다이어그램 및 설계서
│   ├── commits/                  # 커밋 기록 (_template.md 필수 포함)
│   ├── find_debug/               # 디버깅 일일 기록
│   ├── guidance/                 # 가이드라인
│   ├── trainings/                # 연구 및 학습 자료
│   ├── repeater/                 # 인프라/네트워크 장애 처리 기록
│   ├── vaildates/                # 검증 및 테스트 체크리스트
│   └── web_management/           # 배포 및 운영 관리 기록
│
├── docker-compose.yml            # 도커 오케스트레이션 구성
├── .env.example                  # 공통 환경 변수 템플릿
├── AGENTS.md                     # 에이전트 협업 규칙 (SSOT)
└── README.md                     # 루트 안내서
```

---

## 🚀 빠른 시작 (Quick Start)

### 1. 사전 요구사항
- Node.js (v18+)
- Python (3.10+)
- npm 또는 pnpm

API 키 없이도 동작합니다. `ai-server/.env`에 `OPENAI_API_KEY`를 넣고 `AI_PROVIDER=auto`로 두면 종 식별과 관리 가이드가 OpenAI를 사용하고, 키가 없거나 호출에 실패하면 내장 식물 카탈로그로 넘어갑니다.

서버는 AI 서버, Express, Svelte 순서로 켭니다.

### 2. 각 서비스 실행 방법

#### AI Server (Flask)
```bash
cd ai-server
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
python run.py
# 실행: http://localhost:5000
```

#### Backend (Express.js)
```bash
cd backend
npm install
copy .env.example .env
npm run dev
# 실행: http://localhost:3000
```

#### Frontend (Svelte + Vite)
```bash
cd frontend
npm install
npm run dev
# 접속: http://localhost:5173
```

---

## 🌿 주요 기능 안내

1. **식물 사진 업로드**: JPG, PNG, WEBP, 최대 10MB. 드래그 앤 드롭과 샘플 이미지를 지원합니다.
2. **종 식별**: Express가 이미지를 Flask에 전달합니다. 결과 카드에 한글 이름, 학명, 신뢰도, 상위 후보가 표시됩니다.
3. **관리 가이드**: 물주기, 채광, 온도, 토양, 비료, 주의사항, 계절 팁을 보여 줍니다.
4. **내 식물 정원**: 애칭과 함께 SQLite에 저장하고, 목록 조회와 삭제가 가능합니다. 상단 배지는 백엔드와 AI 서버 연결 상태를 표시합니다.

---

## 📜 협업 및 규칙
프로젝트에 기여하거나 AI 에이전트를 활용할 때는 [AGENTS.md](./AGENTS.md)의 커밋 컨벤션(`type(scope): 한국어 요약`), `Docs/commits/` 커밋 기록 생성 규칙, 브랜치 전략(`feature/*`)을 반드시 준수해야 합니다.
