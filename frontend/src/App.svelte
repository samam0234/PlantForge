<script>
  import ImageUpload from './lib/components/ImageUpload.svelte';
  import IdentificationResult from './lib/components/IdentificationResult.svelte';
  import CareGuide from './lib/components/CareGuide.svelte';
  import PlantCollection from './lib/components/PlantCollection.svelte';
  import { currentResult, plantCollection, isLoading, activeTab } from './lib/stores/plants.js';
  import { identifyPlantApi } from './lib/api/plant.js';

  let toast = { type: '', message: '' };
  let toastTimer;

  function handleFileSelected() {
    $currentResult = null;
  }

  async function handleAnalyze(event) {
    const { file, previewUrl } = event.detail;
    if (!file) {
      showToast('분석할 식물 사진을 먼저 선택해 주세요.', 'error');
      return;
    }

    $isLoading = true;
    $currentResult = null;

    try {
      const res = await identifyPlantApi(file);
      $currentResult = {
        ...res.data,
        imageUrl: previewUrl,
        serverImagePath: res.imageUrl,
        identificationId: res.identificationId
      };
    } catch (err) {
      showToast(err.message || '식물 식별에 실패했습니다.', 'error');
    } finally {
      $isLoading = false;
    }
  }

  function handlePlantAdded() {
    showToast('식물이 내 컬렉션에 추가되었습니다.', 'success');
  }

  function handleUploadError(event) {
    showToast(event.detail.message, 'error');
  }

  function showToast(message, type = 'success') {
    toast = { type, message };
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toast = { type: '', message: '' };
    }, 4000);
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
  {#if toast.message}
    <div class="toast-alert {toast.type} animate-fade-in">
      {toast.message}
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
            on:error={handleUploadError}
          />

          <div class="info-card card">
            <h4 class="info-card-title">사진 한 장이 분석까지</h4>
            <p class="info-card-desc">
              업로드한 이미지는 Express가 보관한 뒤 Flask로 전달됩니다. API 키가 있으면 Vision 모델이, 없으면 내장 식물 카탈로그가 종과 관리 가이드를 돌려줍니다.
            </p>
          </div>
        </div>

        <!-- 우측: 식별 결과 & 상세 가이드 -->
        <div class="col-right">
          {#if $isLoading}
            <div class="placeholder-card card">
              <span class="ph-icon spinner-lg"></span>
              <h3>식물을 살펴보는 중입니다</h3>
              <p>사진을 Express로 보낸 뒤 Flask가 종과 관리 가이드를 만들고 있습니다.</p>
            </div>
          {:else if $currentResult}
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
    max-width: min(420px, calc(100vw - 32px));
  }

  .toast-alert.error {
    background: #9b2226;
  }

  .spinner-lg {
    width: 42px;
    height: 42px;
    border: 3px solid var(--accent-soft);
    border-top-color: var(--primary);
    border-radius: 50%;
    display: inline-block;
    animation: spin 0.8s linear infinite;
    font-size: 0;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
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
