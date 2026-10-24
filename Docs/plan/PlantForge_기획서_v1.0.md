# PlantForge 기획서 v1.0

**AI 기반 식물 식별 및 관리 가이드 플랫폼**

| 항목 | 내용 |
|------|------|
| 프로젝트명 | PlantForge |
| 버전 | 1.0 |
| 작성일 | 2026-10-25 |
| 기술 스택 | Svelte + Express.js + Flask |
| 유형 | 미니 프로젝트 (Vibe Coding 대상) |

---

## 1. 프로젝트 개요

**PlantForge**는 사용자가 식물의 사진을 업로드하면 AI가 해당 식물의 종을 식별하고, 그에 맞는 상세한 관리 가이드(물주기, 햇빛, 온도, 토양, 비료, 주의사항 등)를 제공하는 플랫폼입니다.

핵심 가치는 **“사진 한 장으로 식물을 알아보고, 제대로 키우는 방법을 바로 알 수 있는 경험”**입니다.

### 선정 배경
- 이전 미니 프로젝트들(일기 감정 분석, 문서 요약 Q&A, 스토리 생성 등)과 중복되지 않는 주제
- 5개 AI 주제 중 제비뽑기로 선정
- 이미지 기반 AI (Computer Vision + LLM) 패턴 학습에 적합
- Svelte + Express + Flask 3계층 아키텍처 연습에 적합

### 선정된 5개 후보 주제
1. AI 개인 재무 분석 및 예산 추천기
2. AI 언어 학습 대화 파트너
3. **AI 식물 식별 및 관리 가이드** ✅
4. AI 이메일 작성 및 톤 조절 도구
5. AI 습관 추적 및 인사이트 제공기

---

## 2. 목표 및 범위

### 목표
1. 식물 사진 업로드 → 종 식별 → 관리 가이드 생성까지 End-to-End 흐름 구현
2. Svelte(UI) / Express(Orchestrator) / Flask(AI) 역할 분리 실습
3. Vibe Coding 방식으로 빠르게 동작하는 MVP 완성
4. 사용자가 등록한 식물 목록 관리 및 간단한 케어 기록 기능

### 범위 (MVP)
- 식물 사진 업로드 (단일 이미지)
- AI 기반 식물 종 식별 (상위 1~3개 후보 표시)
- 식별된 식물에 대한 상세 관리 가이드 생성
- 사용자별 식물 컬렉션 등록/조회 (간단한 세션 또는 로컬 ID 기반)
- 기본적인 케어 팁 및 주의사항 표시

### 제외 범위 (향후 확장)
- 실시간 카메라 스트리밍 식별
- 다중 식물 동시 식별
- 고급 사용자 인증 / 소셜 로그인
- 푸시 알림 기반 물주기 리마인더
- 식물 성장 타임라인 / 사진 기록
- 질병/해충 증상 진단
- 커뮤니티 / 공유 기능

---

## 3. 기술 스택

| 레이어 | 기술 | 역할 |
|--------|------|------|
| Frontend | Svelte (Vite 기반) | UI, 이미지 업로드, 결과 표시, 식물 컬렉션 관리 |
| Backend (Orchestrator) | Express.js (Node.js) | 이미지 업로드 처리, 메타데이터 관리, AI 서버 프록시, 세션/컬렉션 API |
| AI Server | Flask | 이미지 전처리, 식물 종 식별 (모델/API), LLM 기반 관리 가이드 생성 |
| Database | SQLite (또는 PostgreSQL) | 식물 컬렉션, 식별 기록, 사용자 메타데이터 저장 |
| 기타 | Multer (파일 업로드), Axios | 파일 처리 및 서비스 간 통신 |

### AI 관련 기술 옵션
- **식별**: Hugging Face Transformers (식물 분류 모델), PlantNet API, 또는 OpenAI Vision / Gemini Vision API
- **가이드 생성**: OpenAI GPT / Claude / 로컬 LLM (Ollama 등)
- MVP에서는 **OpenAI Vision + GPT** 또는 **간단한 사전 정의된 식물 DB + LLM** 조합 추천

---

## 4. 시스템 아키텍처 및 오케스트레이션

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Svelte    │────▶│   Express.js     │────▶│     Flask       │
│  (Frontend) │◀────│  (Orchestrator)  │◀────│   (AI Server)   │
└─────────────┘     └──────────────────┘     └─────────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │   SQLite    │
                     └─────────────┘
```

### 역할 분담

| 컴포넌트 | 책임 |
|----------|------|
| **Svelte** | 이미지 드래그앤드롭 업로드, 식별 결과 카드 표시, 관리 가이드 UI, 내 식물 목록 |
| **Express.js** | 파일 업로드 처리 (Multer), 이미지 임시 저장, Flask 호출 오케스트레이션, 컬렉션 CRUD, 에러 핸들링 |
| **Flask** | 이미지 분석, 식물 종 식별, 관리 가이드 LLM 생성, 결과 JSON 반환 |
| **SQLite** | `plants` (컬렉션), `identifications` (식별 기록) 테이블 |

### 오케스트레이션 흐름

1. 사용자가 Svelte에서 식물 사진 업로드
2. Express가 이미지를 받아 임시 저장 후 Flask `/identify` 호출
3. Flask가 이미지 분석 → 종 식별 → 관리 가이드 생성 후 Express에 결과 반환
4. Express가 결과 저장(선택) 후 Svelte에 응답
5. 사용자가 "내 식물에 추가" 시 Express가 DB에 기록
6. 내 식물 목록 조회 시 Express가 DB 조회 후 반환

---

## 5. 폴더 구조

```
plantforge/
├── frontend/                     # Svelte + Vite
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/
│   │   │   │   ├── ImageUpload.svelte
│   │   │   │   ├── IdentificationResult.svelte
│   │   │   │   ├── CareGuide.svelte
│   │   │   │   └── PlantCollection.svelte
│   │   │   ├── api/
│   │   │   │   └── plant.js
│   │   │   └── stores/
│   │   │       └── plants.js
│   │   ├── routes/
│   │   │   └── +page.svelte
│   │   └── app.html
│   ├── package.json
│   └── vite.config.js
│
├── backend/                      # Express.js
│   ├── src/
│   │   ├── routes/
│   │   │   ├── plants.js
│   │   │   └── identify.js
│   │   ├── services/
│   │   │   └── aiClient.js
│   │   ├── db/
│   │   │   └── database.js
│   │   ├── middleware/
│   │   │   └── upload.js
│   │   └── app.js
│   ├── package.json
│   └── .env.example
│
├── ai-server/                    # Flask
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   │   └── identify.py
│   │   ├── services/
│   │   │   ├── vision_service.py
│   │   │   └── guide_service.py
│   │   └── models/
│   │       └── schemas.py
│   ├── requirements.txt
│   └── .env.example
│
├── docker-compose.yml            # (선택) 전체 오케스트레이션
├── .env.example
└── README.md
```

---

## 6. 주요 기능 상세

### 6.1 식물 식별
- 지원 형식: JPG, PNG, WEBP (최대 10MB)
- 응답: 종 이름(영문/한글), 학명, 신뢰도(%), 상위 후보 2~3개
- 식별 실패 시 적절한 에러 메시지

### 6.2 관리 가이드
- 물주기 주기 및 방법
- 빛 요구사항 (직사광/간접광 등)
- 적정 온도 범위
- 토양 종류
- 비료 주기
- 주의사항 / 독성 여부
- 계절별 관리 팁

### 6.3 식물 컬렉션
- 식별 결과를 "내 식물"에 추가
- 닉네임 지정 가능
- 등록일, 마지막 확인일 기록
- 목록 조회 및 삭제

---

## 7. API 설계

### Express.js API

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/identify` | 이미지 업로드 후 식별 + 가이드 요청 |
| GET | `/api/plants` | 내 식물 목록 조회 |
| POST | `/api/plants` | 식물 컬렉션에 추가 |
| DELETE | `/api/plants/:id` | 식물 삭제 |
| GET | `/api/plants/:id` | 특정 식물 상세 조회 |

### Flask AI Server API

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/identify` | 이미지 수신 → 종 식별 + 관리 가이드 생성 |

**응답 예시**:
```json
{
  "species": "Monstera Deliciosa",
  "common_name": "몬스테라",
  "scientific_name": "Monstera deliciosa",
  "confidence": 0.92,
  "candidates": [...],
  "care_guide": {
    "watering": "토양 표면이 마르면 충분히 물주기 (주 1~2회)",
    "light": "밝은 간접광",
    "temperature": "18~27°C",
    "soil": "배수가 잘 되는 다육식물용 흙",
    "fertilizer": "성장기 월 1회",
    "notes": "반려동물에게 독성이 있을 수 있음"
  }
}
```

---

## 8. 데이터 모델

### plants 테이블
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER PK | |
| nickname | TEXT | 사용자 지정 이름 |
| species | TEXT | 식별된 종 |
| scientific_name | TEXT | 학명 |
| care_guide | TEXT (JSON) | 관리 가이드 |
| image_path | TEXT | 저장된 이미지 경로 |
| created_at | DATETIME | |
| updated_at | DATETIME | |

### identifications 테이블 (선택)
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER PK | |
| plant_id | INTEGER FK | |
| confidence | REAL | |
| raw_result | TEXT | 원본 AI 응답 |

---

## 9. 개발 로드맵 (Vibe Coding 기준)

### Phase 1: 기본 골격 (1~2시간)
- 각 서버 기본 프로젝트 생성
- Express ↔ Flask 통신 확인
- Svelte 기본 업로드 UI

### Phase 2: 핵심 식별 기능 (2~3시간)
- 이미지 업로드 → Flask 전달
- Flask에서 Vision API 또는 모델 호출
- 결과 Svelte에 표시

### Phase 3: 관리 가이드 + 컬렉션 (2시간)
- LLM으로 가이드 생성
- DB 연동 및 컬렉션 CRUD

### Phase 4: 다듬기 (1시간)
- UI 개선, 에러 처리, 로딩 상태
- README 작성

---

## 10. Vibe Coding 가이드

1. **먼저 동작하게 만들기**: 완벽한 모델보다 간단한 API 호출로 MVP 완성
2. **역할 분리 명확히**: Svelte는 UI만, Express는 오케스트레이션만, Flask는 AI만
3. **환경 변수 관리**: API 키는 `.env`로 분리
4. **에러 핸들링**: 각 계층에서 적절한 에러 메시지 반환
5. **점진적 개선**: 식별 정확도는 나중에 모델 교체로 개선

---

## 11. 참고 사항

- 식물 식별 모델 후보: 
  - PlantNet API (공식)
  - Hugging Face `microsoft/resnet-50` 기반 fine-tuned 모델
  - OpenAI `gpt-4o` Vision
- 한국어 지원: 종 이름과 가이드를 한글로 생성하도록 프롬프트 조정
- 이미지 저장: MVP에서는 로컬 `uploads/` 폴더, 이후 S3 등으로 확장

---

**작성일**: 2026-10-25  
**상태**: 기획 완료, 개발 대기
