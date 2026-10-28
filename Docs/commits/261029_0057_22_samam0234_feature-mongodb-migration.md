# 커밋 기록

- **날짜/시간**: 261029_0057
- **작성자**: samam0234
- **브랜치**: feature/mongodb-migration
- **커밋 메시지**: docs(backend): MongoDB 환경 변수와 실행 스크립트 안내 추가
- **변경 내용**:
  - `backend/README.md`에 MongoDB 설정 표(`MONGODB_URI`, `MONGODB_DB`, `DNS_SERVERS`, `MONGOD_PATH`)와 `db:start`, `migrate:sqlite`, `verify:api` 사용법 추가
  - API 명세의 `identification_id` 예시를 숫자에서 ObjectId 문자열로 수정하고, id 형식과 삭제 시 `plant_id` null 처리 설명 추가
  - Atlas 사용 시 IP 허용 목록과 `.env` 커밋 금지 주의사항 추가
- **관련 이슈/작업**: MongoDB 전환 후 문서 보완
- **비고**:
  - Atlas 연결 상태에서 식별, 컬렉션 등록, 목록, 삭제를 curl과 브라우저 UI로 확인함 (테스트 데이터는 정리함)
  - push/병합은 하지 않음
