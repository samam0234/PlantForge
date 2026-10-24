# MVP 검증 체크리스트

작성일: 2026-10-25

- [x] Flask `POST /identify`가 예시 이미지에서 종, 후보, 가이드를 반환
- [x] Express `POST /api/identify`가 파일을 저장하고 Flask 결과와 `identificationId`를 반환
- [x] `POST /api/plants` 후 `identifications.plant_id`가 연결됨
- [x] `GET /api/plants`, `GET /api/plants/:id`, `DELETE /api/plants/:id`
- [x] 닉네임·종이 없으면 400
- [x] API 키 없이 `provider=local-catalog`, `care_guide.source=catalog`
- [x] 브라우저에서 샘플 식별, 정원 저장, 삭제를 한 번씩 수행
- [ ] `OPENAI_API_KEY`가 있는 환경에서 Vision·LLM 경로를 한 번 확인

로컬 카탈로그 검증에 사용한 예시는 `frontend/public/samples/`의 몬스테라, 스킨답서스, 에케베리아 이미지다.
