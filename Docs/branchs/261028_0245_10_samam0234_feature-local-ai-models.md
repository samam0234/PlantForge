# 커밋 기록

- **날짜/시간**: 261028_0245
- **작성자**: samam0234
- **브랜치**: feature/local-ai-models
- **커밋 메시지**: feat(ai-server): BioCLIP 로컬 식별과 Ollama 가이드 생성 추가
- **변경 내용**:
  - 색상 통계만 비교하던 로컬 식별을 BioCLIP 2 zero-shot 식별(`bioclip_service.py`)로 대체, CUDA가 있으면 GPU를 자동 사용
  - 후보 종 목록 `plant_labels.py` 추가 (실내 식물 50종 + 딸기·토마토 등 정원·텃밭 식물 28종)
  - `AI_PROVIDER=bioclip` 추가, auto는 OpenAI 키 → BioCLIP → 색상 카탈로그 순으로 선택하고 실패 시 단계적으로 폴백
  - 관리 가이드를 OpenAI 키가 없으면 Ollama(`OLLAMA_GUIDE_MODEL`, 기본 예시 gemma4:12b)로 생성
  - `.env.example`, `requirements.txt`, `docker-compose.yml`, `ai-server/README.md`에 설정과 GPU 설치 방법 반영
- **관련 이슈/작업**: 식물 식별 정확도 개선(로컬 모델 도입)
- **비고**:
  - Flask 테스트 클라이언트로 `/health`, `/identify` 확인. 딸기 잎 사진을 딸기(1.0)로 식별하고 가이드는 Ollama가 생성
  - 후보 목록에 없는 식물은 가장 비슷한 종으로 높은 신뢰도가 나올 수 있음. 에케베리아로 오인되던 딸기 사진이 후보 확장 후 해결됨
  - 현재 설치된 torch가 CPU 빌드(`2.12.1+cpu`)라 검증은 CPU에서 수행. GPU 사용은 README의 CUDA torch 설치 후 확인 필요
  - 프론트 샘플 이미지(`frontend/public/samples`)는 색 도형이라 실제 식별 검증에 쓸 수 없음
