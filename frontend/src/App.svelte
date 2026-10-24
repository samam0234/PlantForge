<script>
  import ImageUpload from './lib/components/ImageUpload.svelte';
  import IdentificationResult from './lib/components/IdentificationResult.svelte';
  import CareGuide from './lib/components/CareGuide.svelte';
  import PlantCollection from './lib/components/PlantCollection.svelte';
  import { currentResult, plantCollection, isLoading, activeTab } from './lib/stores/plants.js';
  import { identifyPlantApi } from './lib/api/plant.js';

  let hasAnalyzed = true; // 시각적 프리뷰를 기본적으로 바로 보여줌
  let alertMessage = '';

  // 파일 선택 이벤트
  function handleFileSelected(event) {
    const { previewUrl, sampleName } = event.detail;
    if (previewUrl) {
      $currentResult.imageUrl = previewUrl;
    }
    if (sampleName) {
      if (sampleName === '스킨답서스') {
        $currentResult = {
          species: 'Epipremnum aureum',
          common_name: '스킨답서스 (골든 포토스)',
          scientific_name: 'Epipremnum aureum',
          confidence: 0.96,
          imageUrl: previewUrl,
          candidates: [
            { species: 'Epipremnum aureum', common_name: '스킨답서스', scientific_name: 'Epipremnum aureum', confidence: 0.96 },
            { species: 'Philodendron hederaceum', common_name: '필로덴드론', scientific_name: 'Philodendron hederaceum', confidence: 0.72 }
          ],
          care_guide: {
            watering: '겉흙이 마르면 관수 (주 1회 내외)',
            light: '반음지에서도 잘 적응하며 형광등 불빛으로도 생장',
            temperature: '18~24°C',
            soil: '일반 배양토 또는 수경재배',
            fertilizer: '성장기 2개월에 1회',
            notes: '공기 정화 능력이 탁월하며 번식력이 매우 좋습니다'
          }
        };
      } else if (sampleName === '다육이') {
        $currentResult = {
          species: 'Echeveria elegans',
          common_name: '에케베리아 (다육식물)',
          scientific_name: 'Echeveria elegans',
          confidence: 0.92,
          imageUrl: previewUrl,
          candidates: [
            { species: 'Echeveria elegans', common_name: '에케베리아', scientific_name: 'Echeveria elegans', confidence: 0.92 },
            { species: 'Haworthia fasciata', common_name: '십이지권', scientific_name: 'Haworthia fasciata', confidence: 0.65 }
          ],
          care_guide: {
            watering: '잎이 쪼글거리거나 속흙까지 완전히 마르면 듬뿍 (월 1~2회)',
            light: '직사광선 또는 매우 밝은 채광 필수',
            temperature: '15~28°C (겨울철 5°C 이상 유지)',
            soil: '마사토 비율이 50% 이상인 다육 전용토',
            fertilizer: '봄철 1회 소량만 시비',
            notes: '습기에 취약하므로 통풍이 잘되는 창가에 배치하세요'
          }
        };
      }
    }
  }

  // 분석 시작
  async function handleAnalyze(event) {
    const { file, previewUrl } = event.detail;
    $isLoading = true;

    try {
      if (file) {
        // 백엔드 API 호출 시도 (Express -> Flask)
        const res = await identifyPlantApi(file);
        if (res.success && res.data) {
          $currentResult = {
            ...res.data,
            imageUrl: previewUrl
          };
        }
      } else {
        // 시각적 데모 딜레이 연출
        await new Promise(r => setTimeout(r, 800));
      }
      hasAnalyzed = true;
    } catch (err) {
      console.warn('백엔드 서버 미응답 또는 오류 발생: 데모 목업 모드로 전환합니다', err);
      await new Promise(r => setTimeout(r, 600));
      hasAnalyzed = true;
    } finally {
      $isLoading = false;
    }
  }

  function handlePlantAdded() {
    showAlert('식물이 내 컬렉션에 추가되었습니다! 🌿');
  }

  function showAlert(msg) {
    alertMessage = msg;
    setTimeout(() => {
      alertMessage = '';
    }, 3000);
  }
</script>

<div class="app-layout">
  <!-- 상단 네비게이션 헤더 -->
  <header class="header">
    <div class="container header-inner">
      <div class="brand-group">
        <span class="brand-logo">🌱</span>
        <div class="brand-text">
          <h1 class="brand-title">PlantForge</h1>
          <span class="brand-subtitle">AI Plant Identification & Care</span>
        </div>
      </div>

      <nav class="nav-tabs">
        <button
          class="nav-tab {$activeTab === 'identify' ? 'active' : ''}"
          on:click={() => $activeTab = 'identify'}
        >
          🔍 식물 분석
        </button>
        <button
          class="nav-tab {$activeTab === 'collection' ? 'active' : ''}"
          on:click={() => $activeTab = 'collection'}
        >
          🪴 내 식물 정원
          <span class="collection-count">{$plantCollection.length}</span>
        </button>
      </nav>

      <div class="header-badges">
        <span class="badge badge-green">● 시스템 정상</span>
      </div>
    </div>
  </header>

  <!-- 알림 토스트 -->
  {#if alertMessage}
    <div class="toast-alert animate-fade-in">
      {alertMessage}
    </div>
  {/if}

  <main class="main-content container">
    <!-- 히어로 배너 섹션 -->
    <section class="hero-section">
      <div class="hero-content">
        <div class="hero-tag">
          <span class="badge badge-amber">⚡ Vibe Coding MVP v1.0</span>
        </div>
        <h2 class="hero-title">사진 한 장으로 식물을 알아보고,<br />맞춤형 케어 가이드를 확인하세요</h2>
        <p class="hero-desc">
          AI 비전 기술로 종을 식별하고, LLM을 통해 물주기·채광·온도·토양 등 세심한 관리법을 제안합니다.
        </p>
      </div>
    </section>

    <!-- 탭 1: 식물 식별 및 분석 화면 -->
    {#if $activeTab === 'identify'}
      <div class="identify-layout">
        <!-- 좌측: 업로드 & 샘플 컨트롤 -->
        <div class="col-left">
          <ImageUpload
            on:fileSelected={handleFileSelected}
            on:analyze={handleAnalyze}
          />

          <!-- 시각적 미리보기 안내 카드 -->
          <div class="info-card card">
            <h4 class="info-card-title">💡 시각적 프리뷰 가이드</h4>
            <p class="info-card-desc">
              현재 화면은 프론트엔드의 비주얼 인터페이스를 즉시 확인할 수 있도록 샘플 데이터와 함께 구성되어 있습니다. 사진을 변경하거나 샘플 버튼을 누르면 다른 식물의 가이드를 바로 볼 수 있습니다.
            </p>
          </div>
        </div>

        <!-- 우측: 식별 결과 & 상세 가이드 -->
        <div class="col-right">
          {#if hasAnalyzed && $currentResult}
            <div class="results-stack">
              <IdentificationResult
                result={$currentResult}
                on:added={handlePlantAdded}
              />

              <CareGuide
                guide={$currentResult.care_guide}
                speciesName={$currentResult.common_name || $currentResult.species}
              />
            </div>
          {:else}
            <div class="placeholder-card card">
              <span class="ph-icon">🌿</span>
              <h3>식물 사진을 업로드해주세요</h3>
              <p>왼쪽에서 사진을 올리거나 샘플 식물을 선택하면 AI 식별 결과와 관리 가이드가 여기에 나타납니다.</p>
            </div>
          {/if}
        </div>
      </div>
    {:else if $activeTab === 'collection'}
      <!-- 탭 2: 내 식물 컬렉션 화면 -->
      <PlantCollection />
    {/if}
  </main>

  <!-- 푸터 -->
  <footer class="footer">
    <div class="container footer-inner">
      <div class="arch-pills">
        <span class="pill">Svelte 5173</span>
        <span class="arrow">⇄</span>
        <span class="pill">Express 3000</span>
        <span class="arrow">⇄</span>
        <span class="pill">Flask 5000</span>
        <span class="arrow">⇄</span>
        <span class="pill">SQLite</span>
      </div>
      <p class="footer-copy">© 2026 PlantForge • AI 기반 식물 식별 및 관리 가이드 플랫폼</p>
    </div>
  </footer>
</div>

<style>
  .app-layout {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  /* Header */
  .header {
    background: #ffffff;
    border-bottom: 1px solid var(--border-color);
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 1px 4px rgba(0,0,0,0.02);
  }

  .header-inner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 70px;
  }

  .brand-group {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .brand-logo {
    font-size: 1.8rem;
  }

  .brand-title {
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--primary-hover);
    line-height: 1.1;
    letter-spacing: -0.03em;
  }

  .brand-subtitle {
    font-size: 0.75rem;
    color: var(--text-muted);
    font-weight: 600;
  }

  .nav-tabs {
    display: flex;
    gap: 8px;
    background: #f1f6f2;
    padding: 4px;
    border-radius: 9999px;
  }

  .nav-tab {
    background: transparent;
    padding: 8px 18px;
    border-radius: 9999px;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .nav-tab.active {
    background: #ffffff;
    color: var(--primary);
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
  }

  .collection-count {
    background: var(--primary-light);
    color: var(--primary-hover);
    font-size: 0.72rem;
    padding: 2px 7px;
    border-radius: 9999px;
    font-weight: 700;
  }

  /* Main & Hero */
  .main-content {
    flex: 1;
    padding-top: 36px;
    padding-bottom: 60px;
  }

  .hero-section {
    margin-bottom: 36px;
    background: linear-gradient(135deg, #e8f5e9 0%, #d8f3dc 100%);
    padding: 36px 32px;
    border-radius: var(--radius-lg);
    border: 1px solid #b7e4c7;
  }

  .hero-tag {
    margin-bottom: 12px;
  }

  .hero-title {
    font-size: 2rem;
    font-weight: 800;
    color: var(--primary-hover);
    line-height: 1.25;
    letter-spacing: -0.02em;
    margin-bottom: 12px;
  }

  .hero-desc {
    font-size: 1.05rem;
    color: #2d4f3b;
    max-width: 720px;
  }

  /* Identify Layout */
  .identify-layout {
    display: grid;
    grid-template-columns: 420px 1fr;
    gap: 28px;
    align-items: start;
  }

  @media (max-width: 900px) {
    .identify-layout {
      grid-template-columns: 1fr;
    }
  }

  .col-left {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .info-card {
    padding: 20px;
    background: #ffffff;
    border-radius: var(--radius-md);
    border-left: 4px solid var(--accent);
  }

  .info-card-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text-main);
    margin-bottom: 6px;
  }

  .info-card-desc {
    font-size: 0.85rem;
    color: var(--text-muted);
    line-height: 1.5;
  }

  .col-right {
    display: flex;
    flex-direction: column;
  }

  .results-stack {
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .placeholder-card {
    text-align: center;
    padding: 60px 24px;
    background: #ffffff;
    border-radius: var(--radius-lg);
  }

  .ph-icon {
    font-size: 3rem;
    display: block;
    margin-bottom: 12px;
  }

  .placeholder-card h3 {
    font-size: 1.2rem;
    color: var(--text-main);
    margin-bottom: 6px;
  }

  .placeholder-card p {
    font-size: 0.9rem;
    color: var(--text-muted);
    max-width: 400px;
    margin: 0 auto;
  }

  /* Toast Alert */
  .toast-alert {
    position: fixed;
    top: 86px;
    right: 24px;
    background: var(--primary);
    color: #fff;
    padding: 12px 20px;
    border-radius: var(--radius-md);
    font-weight: 600;
    box-shadow: var(--shadow-md);
    z-index: 1000;
  }

  /* Footer */
  .footer {
    background: #ffffff;
    border-top: 1px solid var(--border-color);
    padding: 24px 0;
    margin-top: auto;
  }

  .footer-inner {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
  }

  .arch-pills {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: center;
  }

  .pill {
    background: #edf6ef;
    color: var(--primary-hover);
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 700;
    border: 1px solid #cce5d4;
  }

  .arrow {
    color: var(--text-muted);
    font-size: 0.8rem;
  }

  .footer-copy {
    font-size: 0.8rem;
    color: var(--text-muted);
  }
</style>
