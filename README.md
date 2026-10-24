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
│   (UI / Mock Preview)   │         │ (Upload, DB, Route API) │         │ (Vision AI / Guide LLM) │
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
│   │   │   ├── api/              # plant.js (API 클라이언트 뼈대)
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
│   │   ├── services/             # aiClient.js (Flask AI 연동 스켈레톤)
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
│   │   ├── services/             # vision_service.py, guide_service.py
│   │   ├── models/               # schemas.py
│   │   └── main.py               # Flask 엔트리포인트
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── Docs/                         # 인수인계 및 프로젝트 문서 표준 폴더
│   ├── plan/                     # 기획서 및 인수인계 문서
│   ├── Architecture/             # 시스템 아키텍처 다이어그램 및 설계서
│   ├── branchs/                  # 커밋 기록 (_template.md 필수 포함)
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

### 2. 각 서비스 실행 방법

#### Frontend (Svelte + Vite)
```bash
cd frontend
npm install
npm run dev
# 접속: http://localhost:5173
```

#### Backend (Express.js)
```bash
cd backend
npm install
npm run dev # 또는 node src/app.js
# 실행: http://localhost:3000
```

#### AI Server (Flask)
```bash
cd ai-server
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate
pip install -r requirements.txt
python app/main.py
# 실행: http://localhost:5000
```

---

## 🌿 주요 기능 안내

1. **식물 사진 업로드 (UI 프리뷰)**:
   - 드래그 앤 드롭 및 파일 브라우징 지원
   - 업로드 즉시 이미지 실시간 미리보기
2. **AI 종 식별 결과 카드**:
   - 한글 명칭, 학명, 일치 신뢰도(%) 시각화
   - 2~3위 상위 후보 종 비교 표시
3. **상세 식물 관리 가이드**:
   - 💧 물주기 (주기 및 팁)
   - ☀️ 채광 조건 (직사광, 간접광 등)
   - 🌡️ 적정 온도 범위
   - 🪴 토양 및 분갈이 팁
   - ⚠️ 반려동물 독성 및 주의사항
4. **내 식물 컬렉션 관리**:
   - 나만의 애칭(Nickname) 부여
   - 즐겨찾기 및 식물 관리 목록 보관

---

## 📜 협업 및 규칙
프로젝트에 기여하거나 AI 에이전트를 활용할 때는 [AGENTS.md](./AGENTS.md)의 커밋 컨벤션(`type(scope): 한국어 요약`), `Docs/branchs/` 커밋 기록 생성 규칙, 브랜치 전략(`feature/*`)을 반드시 준수해야 합니다.
