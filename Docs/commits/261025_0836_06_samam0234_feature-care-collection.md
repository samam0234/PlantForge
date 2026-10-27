# 커밋 기록

- **날짜/시간**: 261025_0836
- **작성자**: samam0234
- **브랜치**: feature/care-collection
- **커밋 메시지**: feat(collection): LLM 관리 가이드와 식물 컬렉션 CRUD 연동
- **변경 내용**:
  - Flask 가이드 서비스가 OpenAI가 있으면 한국어 관리 가이드를 생성하고, 없으면 종별 카탈로그 가이드를 반환
  - plants 테이블에 common_name을 저장하고, 컬렉션 추가 시 식별 기록과 plant_id를 연결
  - Svelte 컬렉션 추가·조회·삭제가 SQLite API를 사용
- **관련 이슈/작업**: Phase 3 관리 가이드와 컬렉션
- **비고**: AI_PROVIDER=local 이거나 API 키가 없으면 가이드 source는 catalog
