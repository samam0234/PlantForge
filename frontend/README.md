# 🎨 PlantForge Frontend

PlantForge의 사용자 인터페이스(UI)이자 식물 사진 업로드, AI 식별 결과 카드, 관리 가이드 시각화, 내 식물 정원 컬렉션을 제공하는 Svelte + Vite 기반 프론트엔드 프로젝트입니다.

---

## 📌 주요 특징

- **보태니컬 그린 감성 테마**: 포레스트 그린 및 세이지 그린 계열의 팔레트와 카드형 레이아웃
- **실제 식별 요청**: 업로드와 샘플 이미지는 Express `/api/identify`로 전달되고, 응답이 오기 전에는 로딩 카드가 표시됩니다
- **드래그 앤 드롭**: JPG, PNG, WEBP, 최대 10MB. 형식이 다르면 토스트로 알립니다
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
│   │       └── plants.js                   # 식별 결과, 컬렉션, 로딩 스토어
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

## 💡 사용 흐름
1. Express(`3000`)와 Flask(`5000`)를 켠 뒤 `http://localhost:5173`에 접속합니다. 상단 배지가 두 서버 상태를 보여 줍니다.
2. 사진을 올리거나 샘플 버튼을 누른 다음 **AI 식물 종 식별**을 실행합니다.
3. 결과 카드에서 애칭을 입력하고 **내 식물에 추가**를 누르면 MongoDB 컬렉션에 저장됩니다.
4. **내 식물 정원** 탭에서 카드를 열어 가이드를 보고, 삭제하면 서버에서도 지워집니다.
