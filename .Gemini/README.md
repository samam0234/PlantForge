# PlantForge - Gemini 지침

이 프로젝트의 규칙은 루트의 [AGENTS.md](../AGENTS.md)가 단일 원본(SSOT)입니다.
이 파일에는 규칙을 복사하지 말고, 아래 문서를 먼저 읽으세요.

1. [AGENTS.md](../AGENTS.md): 공통 규칙, 커밋 메시지 형식, 브랜치 전략, Docs 폴더 구조
2. [PlantForge_인수인계.md](../PlantForge_인수인계.md): 인수인계 원본 (7장 에이전트 인수인계 대상)

## 공통 지시
- 작업 시작 전 `AGENTS.md`와 인수인계 문서를 확인합니다.
- `feature/*` 브랜치에서만 작업합니다.
- 커밋마다 `Docs/commits/`에 기록 파일을 만듭니다.
- 병합과 push는 사용자의 명시적 지시가 있을 때만 합니다.
- 역할 분리를 지킵니다. Svelte는 UI만, Express는 오케스트레이션만, Flask는 AI만 담당합니다.

## 참고
프로젝트 컨텍스트에 `AGENTS.md`와 인수인계 문서를 포함해 사용하세요.
