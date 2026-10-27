# 커밋 기록

- **날짜/시간**: 261025_0833
- **작성자**: samam0234
- **브랜치**: feature/core-identify
- **커밋 메시지**: feat(identify): 이미지 업로드부터 Flask 식별 결과 표시까지 연결
- **변경 내용**:
  - Flask가 업로드 이미지를 읽어 OpenAI Vision 또는 로컬 식물 카탈로그로 종을 식별
  - 식별된 종에 맞는 카탈로그 관리 가이드를 같은 응답에 포함
  - Express가 목업 응답 대신 Flask 결과와 오류를 그대로 전달하고 식별 로그를 저장
  - Svelte 업로드·샘플 이미지가 실제 `/api/identify`를 호출하고 결과 카드에 표시
- **관련 이슈/작업**: Phase 2 핵심 식별 기능
- **비고**: API 키가 없으면 `local-catalog`, 키가 있으면 `openai-vision` (`AI_PROVIDER=auto`)
