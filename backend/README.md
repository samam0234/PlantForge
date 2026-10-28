# 🌿 PlantForge Backend (Orchestrator)

PlantForge의 파일 업로드, AI 서버 오케스트레이션, MongoDB 데이터베이스 관리 및 컬렉션 CRUD를 담당하는 Express.js 기반 백엔드 서비스입니다.

---

## 📌 주요 역할
- **이미지 업로드 처리**: Multer 미들웨어로 단일 식물 이미지 수신 및 유효성 검사 (최대 10MB, JPG/PNG/WEBP)
- **AI 서비스 오케스트레이션**: 업로드된 이미지를 Flask AI 서버 (`POST /identify`)로 전달하고 통합 결과 수신
- **데이터 영속화 (MongoDB)**: 식물 컬렉션(`plants`) 및 식별 로그(`identifications`) 데이터베이스 관리
- **컬렉션 CRUD API**: 식물 등록, 목록 조회, 상세 조회, 삭제 기능 제공

---

## 🗂 디렉터리 구조

```text
backend/
├── src/
│   ├── app.js               # Express 서버 설정 및 엔트리포인트
│   ├── routes/
│   │   ├── identify.js      # POST /api/identify 라우트
│   │   └── plants.js        # GET, POST, DELETE /api/plants 라우트
│   ├── services/
│   │   └── aiClient.js      # Flask AI Server 통신 클라이언트 (Axios)
│   ├── middleware/
│   │   └── upload.js        # Multer 업로드 미들웨어
│   └── db/
│       └── database.js      # MongoDB 연결 (`plants`, `identifications` 컬렉션)
├── uploads/                 # 이미지 임시 저장소
├── package.json             # 패키지 명세
├── .env.example             # 환경 변수 템플릿
└── README.md
```

---

## ⚙️ API 명세

### 1. 헬스 체크
- `GET /health` : 서버 상태 및 연결된 AI 서버 상태 확인

### 2. 식물 식별 요청
- `POST /api/identify`
  - `Content-Type`: `multipart/form-data`
  - `Body`: `image` (File)
  - 응답: 식별된 종, 신뢰도, 상위 후보, 케어 가이드 JSON

### 3. 내 식물 컬렉션 CRUD
- `GET /api/plants` : 내 등록 식물 전체 목록 조회
- `GET /api/plants/:id` : 특정 식물 상세 조회
- `POST /api/plants` : 식별 결과 또는 식물을 내 컬렉션에 추가
  ```json
  {
    "nickname": "몬이",
    "species": "Monstera deliciosa",
    "common_name": "몬스테라",
    "scientific_name": "Monstera deliciosa",
    "care_guide": { "watering": "...", "light": "..." },
    "image_path": "/uploads/plant-xxx.jpg",
    "identification_id": "<POST /api/identify 응답의 identificationId>"
  }
  ```
- `DELETE /api/plants/:id` : 특정 식물 삭제

> 식물과 식별 기록의 `id`는 MongoDB ObjectId 문자열입니다. 식물을 삭제하면 연결된 식별 기록의 `plant_id`는 `null`이 됩니다.

---

## 🚀 로컬 실행 방법

```bash
# 1. 의존성 설치
npm install

# 2. 환경 변수 설정
cp .env.example .env

# 3. 개발 서버 실행 (Nodemon)
npm run dev

# 또는 일반 실행
npm start
# http://localhost:3000 에서 실행됩니다.
```

---

## 🗄 MongoDB 설정

| 환경 변수 | 설명 |
|---|---|
| `MONGODB_URI` | 연결 문자열. 로컬은 `mongodb://localhost:27017`, Atlas는 `mongodb+srv://사용자:비밀번호@클러스터주소/` (비밀번호의 특수문자는 URL 인코딩) |
| `MONGODB_DB` | DB 이름 (기본 `plantforge`). 컬렉션은 `plants`, `identifications` |
| `DNS_SERVERS` | 선택. `mongodb+srv` 조회(`querySrv ECONNREFUSED`)가 막힌 환경에서 `8.8.8.8,1.1.1.1` 지정 |
| `MONGOD_PATH` | 선택. `npm run db:start`가 쓸 mongod 실행 파일 경로 (기본 `~/mongodb-local/bin/mongod.exe`) |

```bash
npm run db:start       # 로컬 mongod 기동 (이미 떠 있으면 건너뜀, 데이터: backend/data/mongo)
npm run migrate:sqlite # 기존 plantforge.db(SQLite) 데이터를 MongoDB로 이관 (재실행 안전)
npm run verify:api     # 식물 CRUD 스모크 테스트 (임시 데이터는 자동 정리)
```

Atlas를 쓸 때는 Network Access의 IP 허용 목록에 현재 PC의 IP가 있어야 합니다. `.env`에는 비밀번호가 들어 있으니 커밋하지 마세요.
