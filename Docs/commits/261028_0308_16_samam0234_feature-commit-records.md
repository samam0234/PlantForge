# 커밋 기록

- **날짜/시간**: 261028_0308
- **작성자**: samam0234
- **브랜치**: feature/commit-records
- **커밋 메시지**: docs(root): 커밋 기록 폴더를 Docs/commits로 분리
- **변경 내용**:
  - `Docs/commits/` 폴더를 만들고 기존 `Docs/branchs/`의 기록 파일 15개와 `_template.md`를 `git mv`로 이동 (이력 보존)
  - `AGENTS.md`, `PlantForge_인수인계.md`, `Docs/plan/PlantForge_인수인계.md`, `README.md`, 에이전트별 폴더 README와 `.cursor/rules/plantforge.mdc`의 경로를 `Docs/commits/`로 수정
  - 이후 커밋 기록은 `Docs/commits/YYMMDD_HHMM_[id]_[이름]_[브랜치].md`에 작성
- **관련 이슈/작업**: 커밋 기록 저장 위치 변경 (사용자 지시)
- **비고**:
  - 기존 인수인계 문서에는 `commits` 폴더 언급이 없고 `Docs/branchs/`로만 적혀 있어, 사용자 지시에 맞춰 문서도 함께 갱신함
  - 과거 기록 문서 본문에 적힌 옛 경로 표현은 이력이라 수정하지 않음
  - `Docs/branchs/`는 비어 있어 더 이상 존재하지 않음
