# 🎨 PlantForge Frontend

PlantForge의 사용자 인터페이스(UI)이자 식물 사진 업로드, AI 식별 결과 카드, 관리 가이드 시각화, 내 식물 정원 컬렉션을 제공하는 Svelte + Vite 기반 프론트엔드 프로젝트입니다.

---

## 📌 주요 특징 (시각적 프리뷰 중심)

- **보태니컬 그린 감성 테마**: 포레스트 그린 및 세이지 그린 계열의 세련된 팔레트와 카드형 레이아웃
- **즉시 확인 가능한 시각적 데모 (Visual Preview)**:
  - 몬스테라, 스킨답서스, 다육식물 등 사전 등록된 샘플 데이터로 즉각적인 UI 확인 가능
  - 드래그 앤 드롭 업로드 및 실시간 사진 미리보기
- **AI 결과 시각화**:
  - 일치도(Confidence) 프로그레스 게이지 바
  - 상위 2~3위 후보 종 칩(Chip) 표시
  - 물주기, 채광, 적정온도, 토양, 비료, 반려동물 주의사항 등 6가지 시각적 케어 카드
- **내 식물 정원 (My Plants)**:
  - 식물 카드 그리드 뷰 및 상세 케어 가이드 모달

---

## 🗂 디렉터리 구조

```text
frontend/
├── src/
│   ├── lib/
│   │   ├── components/
│   │   │   ├── ImageUpload.svelte          # 이미지 드래그앤드롭 및 미리보기
│   │   │   ├── IdentificationResult.svelte # 식별 결과 카드 및 컬렉션 추가
│   │   │   ├── CareGuide.svelte            # 6종 관리 가이드 시각 카드
│   │   │   └── PlantCollection.svelte      # 내 식물 목록 갤러리 및 모달
│   │   ├── api/
│   │   │   └── plant.js                    # 백엔드 Express 연동 API 클라이언트
│   │   └── stores/
│   │       └── plants.js                   # Svelte Writable 스토어 & 목업 데이터
│   ├── App.svelte                          # 메인 대시보드 뷰
│   ├── app.css                             # 식물 테마 글로벌 스타일시트
│   └── main.js                             # 앱 마운트 엔트리포인트
├── index.html                              # 웹 HTML 템플릿
├── package.json                            # 프론트엔드 패키지 설정
├── vite.config.js                          # Vite 번들러 설정
└── README.md
```

---

## 🚀 로컬 실행 방법

```bash
# 1. frontend 디렉터리로 이동
cd frontend

# 2. 의존성 설치
npm install

# 3. 개발 서버 구동
npm run dev

# 접속 URL: http://localhost:5173
```

---

## 💡 데모 체험 가이드
1. 브라우저에서 `http://localhost:5173` 접속 시 즉시 **몬스테라**에 대한 식별 결과 카드 및 케어 가이드가 시각적으로 표시됩니다.
2. 좌측 상단의 **샘플 식물(스킨답서스, 다육식물)** 버튼을 누르면 사진과 가이드가 실시간으로 전환됩니다.
3. **내 식물에 추가** 버튼을 누르면 나만의 애칭과 함께 **내 식물 정원** 탭에 즉시 반영됩니다.
4. 상단 네비게이션의 **내 식물 정원** 탭을 클릭하여 등록된 식물 카드를 확인하고 카드를 클릭해 상세 모달을 열어볼 수 있습니다.
