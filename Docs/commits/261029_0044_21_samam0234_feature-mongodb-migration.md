# 커밋 기록

- **날짜/시간**: 261029_0044
- **작성자**: samam0234
- **브랜치**: feature/mongodb-migration
- **커밋 메시지**: docs(root): MongoDB Atlas 클러스터 연결 및 데이터 이관 기록
- **변경 내용**:
  - Atlas에 Organization `PlantForge`, 프로젝트 `PlantForge`, 무료(M0) 클러스터 `Cluster0`(AWS 서울)를 새로 생성
  - Atlas 자동 보안 설정으로 DB 사용자와 현재 IP 허용 목록이 생성됨. 접속 문자열과 `DNS_SERVERS=8.8.8.8,1.1.1.1`은 `backend/.env`에만 저장 (커밋 제외)
  - `npm run migrate:sqlite`로 SQLite의 identifications 6건(plants 0건)을 Atlas `plantforge` DB로 이관. 재실행해도 6건 유지
  - AGENTS.md의 Database 항목을 Atlas 기준으로 갱신
- **관련 이슈/작업**: Atlas 클러스터 생성 및 연결 (사용자 지시)
- **비고**:
  - Atlas `verify:api` 8개 항목 통과, 서버 기동 후 `GET /api/plants` 응답 확인
  - 기존 SocialForge의 Cluster0는 사용하지 않고 별도 조직/프로젝트로 분리함
  - 로컬 개발용 mongod(`npm run db:start`)는 그대로 유지. 로컬 DB의 데이터는 Atlas와 별개
  - 클러스터 생성 중 reCAPTCHA는 사용자가 직접 해결. push/병합은 하지 않음
