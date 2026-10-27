# PlantForge Agent Rules & SSOT (Single Source of Truth)

**프로젝트명**: PlantForge (AI 기반 식물 식별 및 관리 가이드 플랫폼)  
**버전**: 1.0  
**작성일**: 2026-10-25  
**기술 스택**: Svelte + Express.js + Flask + SQLite  
**상태**: 초기 스켈레톤 구축 및 개발 진행  

---

## 1. 프로젝트 개요 & 아키텍처

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

- **Frontend (`frontend/`)**: 포트 `5173`. Svelte + Vite. 시각적 UI, 이미지 업로드 인터페이스, 식별 결과 및 케어 가이드 표시, 내 식물 컬렉션 뷰. (UI/상태 관리만 담당)
- **Backend (`backend/`)**: 포트 `3000`. Express.js. Multer 기반 이미지 업로드 처리, Flask AI 호출 오케스트레이션, SQLite DB 연동, 컬렉션 CRUD API 제공.
- **AI Server (`ai-server/`)**: 포트 `5000`. Flask. 이미지 분석, 식물 종 식별(Vision AI / 식물 DB), LLM 기반 관리 가이드 생성.
- **Database**: SQLite (`backend/plantforge.db`). `plants`, `identifications` 테이블.

---

## 2. 필수 공통 규칙 (예외 없음)

### 2.1 커밋 메시지 규칙
- **형식**: `type(scope): 한국어 요약`
- `type` / `scope`는 **영어**, 제목 요약과 본문은 **한국어**
- 예시:
  - `feat(frontend): 이미지 업로드 및 결과 카드 컴포넌트 추가`
  - `chore(backend): Express 기본 라우트 및 SQLite 스켈레톤 설정`
  - `docs(root): README 및 인수인계 규칙 반영`
- **사용 가능한 type**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`

### 2.2 커밋 기록 문서화 (필수)
- 커밋마다 `Docs/commits/YYMMDD_HHMM_[id]_[이름]_[브랜치].md` 작성
- `Docs/commits/_template.md` 양식 준수
- 기록 파일도 해당 브랜치에 함께 커밋/푸시

### 2.3 브랜치 전략
- 모든 작업은 반드시 **`feature/*` 브랜치**에서만 수행
- `main` / `develop`은 병합 전용
- 병합은 `--no-ff` 옵션 사용 (이력 보존)
- **사용자의 명시적 지시 없이는 병합/push를 수행하지 않음**
- 전체 작업 완료 후 사용자의 지시를 받아 일괄 병합 진행

### 2.4 안전 규칙 (위험 명령 금지)
- `push`, 병합, 파일 대량 삭제, 덮어쓰기는 명시적 지시가 있을 때만 수행
- `git push -f`, `git reset --hard` 등 위험 명령 엄격 금지

### 2.5 Docs 폴더 구조
- `Docs/plan/`: 초기 기획, 로직, DB, 배포 계획
- `Docs/Architecture/`: 시스템, 계층, 데이터 흐름 아키텍처
- `Docs/commits/`: 커밋/브랜치 기록 (템플릿: `_template.md`)
- `Docs/find_debug/`: 작업 및 실행 디버깅 기록
- `Docs/guidance/`: 기능 및 실행 가이드
- `Docs/trainings/`: 학습 및 연구 정리
- `Docs/repeater/`: 서버 연결 및 인프라 이슈 해결 기록
- `Docs/vaildates/`: 검증 및 체크리스트
- `Docs/web_management/`: 웹 관리 및 배포 관련 기록

---

## 3. 원본 문서 참조
- 기획서 원본: [Docs/plan/PlantForge_기획서_v1.0.md](file:///d:/vscode/2026_my_WebSite_study/MiniProject/PlantForge/Docs/plan/PlantForge_기획서_v1.0.md)
- 인수인계 원본: [Docs/plan/PlantForge_인수인계.md](file:///d:/vscode/2026_my_WebSite_study/MiniProject/PlantForge/Docs/plan/PlantForge_인수인계.md)
