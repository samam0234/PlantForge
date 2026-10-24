# PlantForge 에이전트 인수인계 및 규칙

**프로젝트명**: PlantForge  
**버전**: 1.0  
**작성일**: 2026-10-25  
**기술 스택**: Svelte (Vite) + Express.js + Flask + SQLite  
**유형**: 미니 프로젝트 (Vibe Coding 대상)  
**SSOT**: 루트 `AGENTS.md` (본 문서는 인수인계 및 규칙 원본, AGENTS.md는 이를 가리킴)

---

## 1. 프로젝트 개요

**PlantForge**는 사용자가 식물의 사진을 업로드하면 AI가 해당 식물의 종을 식별하고, 그에 맞는 상세한 관리 가이드(물주기, 햇빛, 온도, 토양, 비료, 주의사항 등)를 제공하는 플랫폼입니다.

**핵심 가치**: “사진 한 장으로 식물을 알아보고, 제대로 키우는 방법을 바로 알 수 있는 경험”

### 목표
1. 식물 사진 업로드 → 종 식별 → 관리 가이드 생성까지 End-to-End 흐름 구현
2. Svelte(UI) / Express(Orchestrator) / Flask(AI) 역할 분리 실습
3. Vibe Coding 방식으로 빠르게 동작하는 MVP 완성
4. 사용자가 등록한 식물 목록 관리 및 간단한 케어 기록 기능

### MVP 범위
- 식물 사진 업로드 (단일 이미지, JPG/PNG/WEBP, 최대 10MB)
- AI 기반 식물 종 식별 (상위 1~3개 후보 표시)
- 식별된 식물에 대한 상세 관리 가이드 생성
- 사용자별 식물 컬렉션 등록/조회 (세션 또는 로컬 ID 기반)
- 기본 케어 팁 및 주의사항 표시

### 제외 범위 (향후 확장)
- 실시간 카메라 스트리밍 식별
- 다중 식물 동시 식별
- 고급 사용자 인증 / 소셜 로그인
- 푸시 알림 기반 물주기 리마인더
- 식물 성장 타임라인 / 사진 기록
- 질병/해충 증상 진단
- 커뮤니티 / 공유 기능

---

## 2. 기술 스택 및 역할

| 레이어 | 기술 | 역할 | 기본 포트 |
|--------|------|------|-----------|
| Frontend | Svelte + Vite | UI, 이미지 업로드, 결과 표시, 식물 컬렉션 관리 | 5173 |
| Backend (Orchestrator) | Express.js (Node.js) | 파일 업로드 처리 (Multer), 메타데이터 관리, AI 서버 프록시, 세션/컬렉션 API | 3000 |
| AI Server | Flask | 이미지 전처리, 식물 종 식별 (Vision API/모델), LLM 기반 관리 가이드 생성 | 5000 |
| Database | SQLite | 식물 컬렉션, 식별 기록, 사용자 메타데이터 저장 | - (파일: `plantforge.db`) |
| 기타 | Multer, Axios, OpenAI Vision/GPT (MVP 추천) | 파일 처리 및 서비스 간 통신 | - |

**AI 옵션 (MVP 우선순위)**:
1. OpenAI Vision (`gpt-4o`) + GPT 가이드 생성
2. PlantNet API 또는 Hugging Face 식물 분류 모델 + LLM
3. 사전 정의된 식물 DB + LLM 조합

환경 변수는 각 레이어 `.env` / `.env.example`로 관리. API 키 절대 커밋 금지.

---

## 3. 시스템 아키텍처

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

### 역할 분담 (필수·예외 없음)
| 컴포넌트 | 책임 |
|----------|------|
| **Svelte** | 이미지 드래그앤드롭 업로드, 식별 결과 카드 표시, 관리 가이드 UI, 내 식물 목록. UI/상태 관리만. |
| **Express.js** | 파일 업로드 처리, 이미지 임시 저장, Flask 호출 오케스트레이션, 컬렉션 CRUD, 에러 핸들링, 세션. 비즈니스 로직 오케스트레이션만. |
| **Flask** | 이미지 분석, 식물 종 식별, 관리 가이드 LLM 생성, 결과 JSON 반환. AI 관련 작업만. |
| **SQLite** | `plants` (컬렉션), `identifications` (식별 기록) 테이블. |

### 오케스트레이션 흐름
1. 사용자가 Svelte에서 식물 사진 업로드
2. Express가 이미지를 받아 임시 저장 후 Flask `/identify` 호출
3. Flask가 이미지 분석 → 종 식별 → 관리 가이드 생성 후 Express에 결과 반환
4. Express가 결과 저장(선택) 후 Svelte에 응답
5. 사용자가 "내 식물에 추가" 시 Express가 DB에 기록
6. 내 식물 목록 조회 시 Express가 DB 조회 후 반환

---

## 4. 폴더 구조 (권장)

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
├── Docs/                         # 문서 저장 폴더 (아래 구조 필수)
│   ├── plan/
│   ├── Architecture/
│   ├── branchs/
│   ├── find_debug/
│   ├── guidance/
│   ├── trainings/
│   ├── repeater/
│   ├── vaildates/
│   └── web_management/
│
├── docker-compose.yml            # (선택) 전체 오케스트레이션
├── .env.example
├── AGENTS.md                     # SSOT (본 문서 규칙 요약 + 가리킴)
└── README.md
```

### Docs 폴더 용도 (필수)
| 폴더 | 용도 |
|------|------|
| [plan/](./Docs/plan/) | 초기 기획·로직·DB·배포 계획 |
| [Architecture/](./Docs/Architecture/) | 시스템·계층·데이터 흐름 아키텍처 |
| [branchs/](./Docs/branchs/) | 브랜치·커밋 기록 (템플릿 필수) |
| [find_debug/](./Docs/find_debug/) | 작업/실행 디버깅 일일 기록 |
| [guidance/](./Docs/guidance/) | 기능·실행 가이드 |
| [trainings/](./Docs/trainings/) | 학습·연구 정리 |
| [repeater/](./Docs/repeater/) | 서버 연결·인프라 장애와 해결 |
| [vaildates/](./Docs/vaildates/) | 검증·체크리스트 |
| [web_management/](./Docs/web_management/) | 배포 전/배포 시 웹 관리 기록 |

---

## 5. API 설계 요약

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

**응답 예시** (JSON):
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

### 데이터 모델
**plants 테이블**
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

**identifications 테이블** (선택)
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER PK | |
| plant_id | INTEGER FK | |
| confidence | REAL | |
| raw_result | TEXT | 원본 AI 응답 |

---

## 6. 공통 규칙 (필수·예외 없음)

### 6.1 커밋 메시지 형식
- **형식**: `type(scope): 한국어 요약`
- type/scope는 **영어**, 제목 요약과 본문은 **한국어**
- 예시:
  - ✅ `feat(frontend): 이미지 업로드 컴포넌트 추가`
  - ✅ `fix(ai-server): 종 식별 신뢰도 계산 오류 수정`
  - ✅ `docs(rules): 커밋 기록 템플릿 업데이트`
  - ❌ `feat: 이미지 업로드 추가` (한국어 type 금지, scope 누락)
  - ❌ `Add image upload` (영어 요약 금지)

**type 후보**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`

### 6.2 커밋 기록 문서화
- 커밋마다 `Docs/branchs/YYMMDD_HHMM_[id]_[이름]_[브랜치].md` 작성
- 템플릿 파일을 `Docs/branchs/_template.md`에 두고 사용
- 기록 파일도 같은 브랜치에 커밋·푸시
- 경로와 파일명 규칙 고정 (위치가 흩어지지 않게)

**템플릿 예시** (`Docs/branchs/_template.md`):
```markdown
# 커밋 기록

- **날짜/시간**: YYMMDD_HHMM
- **작성자**: [이름]
- **브랜치**: feature/xxx
- **커밋 메시지**: type(scope): 요약
- **변경 내용**:
  - 
- **관련 이슈/작업**:
- **비고**:
```

### 6.3 브랜치 전략
- 작업은 **feature/*** 에서만 수행
- `develop` / `main`은 병합 전용
- 병합은 `--no-ff`로 이력을 보존
- 브랜치 하나가 끝날 때마다 병합하지 않음
- 요청받은 작업을 **전부 커밋한 뒤 한 번에 총 병합**
- **사용자 명시적 지시 없이는 병합하지 않음**
- 병합 기록 문서도 총 병합 때 한 번에 작성

### 6.4 되돌리기 어려운 작업 (사전 확인 필수)
- `push`, 병합, 삭제, 덮어쓰기는 **명시적 지시가 있을 때만** 수행
- 한 번 승인한 것을 다른 상황에 확장 적용하지 않음
- force push, reset --hard 등 위험 명령 절대 금지 (사용자 확인 후에도 재확인)

### 6.5 규칙의 단일 출처 (SSOT)
- 루트 `AGENTS.md`에 공유 규칙을 두고, CLAUDE.md, .cursor/rules 등 에이전트별 파일은 이를 가리키기만 함
- 규칙이 여러 곳에 중복되어 어긋나는 것을 방지
- 다른 에이전트 도구로 바꿔도 재사용 가능

### 6.6 스택·실행 환경 요약 (AGENTS.md에 포함)
```
# 실행 정보
- Frontend (Svelte/Vite): http://localhost:5173
- Backend (Express): http://localhost:3000
- AI Server (Flask): http://localhost:5000
- Database: SQLite (./backend/plantforge.db 또는 지정 경로)
- 의존성: frontend/package.json, backend/package.json, ai-server/requirements.txt
- Docker 프로젝트명: plantforge (docker-compose.yml 사용 시)
- 업로드 임시 경로: backend/uploads/ (MVP)
```

### 6.7 Vibe Coding 가이드
1. **먼저 동작하게 만들기**: 완벽한 모델보다 간단한 API 호출로 MVP 완성
2. **역할 분리 명확히**: Svelte는 UI만, Express는 오케스트레이션만, Flask는 AI만
3. **환경 변수 관리**: API 키는 `.env`로 분리
4. **에러 핸들링**: 각 계층에서 적절한 에러 메시지 반환
5. **점진적 개선**: 식별 정확도는 나중에 모델 교체로 개선
6. 한국어 지원: 종 이름과 가이드를 한글로 생성하도록 프롬프트 조정

---

## 7. 에이전트 인수인계 대상

모든 에이전트는 본 문서와 `AGENTS.md`를 우선 참조.

| 에이전트 | 파일/위치 | 비고 |
|----------|-----------|------|
| .Agents | AGENTS.md (루트) | 공통 규칙 SSOT |
| .Claude | CLAUDE.md | AGENTS.md 가리킴 |
| .Codex | (AGENTS.md 또는 프로젝트 설정) | 동일 |
| .Grok | (대화 시 본 문서 참조) | 동일 |
| Gemini | (프로젝트 컨텍스트) | 동일 |
| .Antigravity | (설정 파일) | 동일 |
| .Cursor | .cursor/rules/ 또는 AGENTS.md | 동일 |
| .Manus | (프로젝트 지침) | 동일 |

**에이전트 공통 지시**:
- 작업 시작 전 `AGENTS.md` 및 본 인수인계 문서 확인
- feature/* 브랜치에서만 작업
- 커밋 시 반드시 `Docs/branchs/`에 기록 파일 생성
- 병합/push는 사용자 명시적 지시 후에만
- 역할 분리 위반 금지 (예: Svelte에서 AI 호출 직접 하지 말 것)

---

## 8. 개발 로드맵 (참고)

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

## 9. 참고 사항

- 이미지 저장: MVP에서는 로컬 `uploads/` 폴더, 이후 S3 등으로 확장
- 식물 식별 모델 후보: PlantNet API, Hugging Face 모델, OpenAI gpt-4o Vision
- 에러 핸들링 및 로딩 상태 각 계층에서 처리
- Docker 사용 시 docker-compose.yml로 전체 오케스트레이션 가능

---

**상태**: 기획 완료, 규칙 및 인수인계 문서 작성 완료 (2026-10-25)  
**다음 단계**: AGENTS.md 생성 후 feature 브랜치에서 개발 시작

---

*본 문서는 PlantForge 프로젝트의 단일 인수인계 및 규칙 원본입니다. 모든 에이전트는 이 규칙을 준수해야 합니다.*
