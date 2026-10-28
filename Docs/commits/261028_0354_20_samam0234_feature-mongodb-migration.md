# 커밋 기록

- **날짜/시간**: 261028_0354
- **작성자**: samam0234
- **브랜치**: feature/mongodb-migration
- **커밋 메시지**: chore(backend): 로컬 mongod 기동 스크립트(db:start) 추가
- **변경 내용**:
  - `backend/scripts/start-mongod.js` 추가: 27017 포트가 닫혀 있으면 mongod를 분리 실행(detached)하고, 열려 있으면 아무것도 하지 않음
  - mongod 경로는 `MONGOD_PATH` 환경 변수, 없으면 `~/mongodb-local/bin/mongod.exe`. 데이터는 `backend/data/mongo`, 로그는 `backend/data/mongod.log`
  - `backend/package.json`에 `npm run db:start` 스크립트 추가
- **관련 이슈/작업**: 로컬 MongoDB를 세션과 무관하게 다시 띄울 수 있도록 함 (사용자 지시)
- **비고**:
  - mongod를 강제 종료 후 `db:start`로 재기동했을 때 identifications 6건이 유지됨을 확인
  - mongod 실행 파일(8.2.6)은 SocialForge의 mongodb-memory-server 캐시를 `C:\Users\User\mongodb-local\bin\mongod.exe`로 복사해 사용했고 저장소에는 포함하지 않음
  - Atlas 클러스터는 생성하지 못함 (Atlas MCP 접근 비활성화). 접속 문자열이 `backend/.env`에 들어오면 `MONGODB_URI`만 교체하면 됨
  - PC 시작 시 자동 실행 설정은 하지 않음. push/병합은 하지 않음
