# 커밋 기록

- **날짜/시간**: 261028_0344
- **작성자**: samam0234
- **브랜치**: feature/mongodb-migration
- **커밋 메시지**: refactor(backend): SQLite에서 MongoDB로 DB 전환 및 데이터 이관 스크립트 추가
- **변경 내용**:
  - `backend/src/db/database.js`: `sqlite3`를 `mongodb` 드라이버로 교체 (`connect`/`getDb`/`close`, DB명 `MONGODB_DB`, `DNS_SERVERS` 옵션)
  - `routes/plants.js`, `routes/identify.js`: MongoDB 컬렉션(`plants`, `identifications`) 기반 async 처리. 식물 `id`는 ObjectId 문자열, 식물 삭제 시 식별 기록의 `plant_id`를 null로 되돌려 기존 `ON DELETE SET NULL` 동작 유지
  - `app.js`: MongoDB 연결 성공 후 서버 시작
  - `backend/scripts/migrate-sqlite-to-mongo.js` (`npm run migrate:sqlite`): `legacy_id` 기준 upsert로 SQLite 데이터를 이관 (재실행해도 중복 없음)
  - `backend/scripts/verify-api.js` (`npm run verify:api`): 식물 CRUD와 식별 기록 연결 스모크 테스트
  - `sqlite3`는 이관용 devDependency로만 유지
  - `.env.example`, `backend/.env.example`, `docker-compose.yml`, `.gitignore`(`backend/data/`), AGENTS.md, README, 프론트 표기 문구를 MongoDB 기준으로 갱신
- **관련 이슈/작업**: DB를 SQLite에서 MongoDB로 전환하고 기존 데이터 이관 (사용자 지시)
- **비고**:
  - 이관 결과: plants 0건, identifications 6건 (이미 없는 식물을 가리키던 `plant_id`는 null 처리). 재실행해도 6건 유지
  - `verify:api` 8개 항목 통과. `POST /api/identify`는 AI 서버가 꺼져 있어 end-to-end 미확인, 프론트 화면은 브라우저로 확인하지 않음
  - 로컬 mongod는 SocialForge의 mongodb-memory-server 캐시(8.2.6)로 `backend/data/mongo`에 띄움. 세션 종료 시 내려가므로 상시 사용은 별도 설치 또는 Atlas 필요
  - `backend/.env`(비밀값 포함)는 커밋하지 않음. push/병합은 하지 않음
