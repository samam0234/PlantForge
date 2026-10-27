# 커밋 기록

- **날짜/시간**: 261028_0249
- **작성자**: samam0234
- **브랜치**: feature/agent-configs
- **커밋 메시지**: chore(root): 에이전트별 지침 폴더와 Cursor 규칙 추가
- **변경 내용**:
  - 인수인계 7장 표에 맞춰 `.Agents`, `.Claude`, `.Codex`, `.Grok`, `.Gemini`, `.Antigravity`, `.Manus` 폴더 추가 (각 `README.md`)
  - 각 README는 규칙을 복사하지 않고 `AGENTS.md`와 인수인계 문서를 가리킴
  - `.cursor/rules/plantforge.mdc` 추가 (`alwaysApply: true`, `AGENTS.md`를 참조)
- **관련 이슈/작업**: 인수인계 문서의 에이전트 인수인계 대상 반영
- **비고**:
  - 규칙 원본은 루트 `AGENTS.md` 하나만 유지함
  - `Gemini`는 표 표기와 달리 `.Gemini`로 생성함 (나머지 폴더와 이름 규칙 통일)
  - 병합과 push는 사용자 지시 전까지 수행하지 않음
