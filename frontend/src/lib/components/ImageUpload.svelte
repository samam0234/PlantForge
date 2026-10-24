<script>
  import { createEventDispatcher } from 'svelte';
  import { isLoading } from '../stores/plants.js';

  const dispatch = createEventDispatcher();

  let isDragging = false;
  let previewUrl = null;
  let selectedFile = null;

  function handleFileSelect(event) {
    const file = event.target.files?.[0];
    if (file) {
      processFile(file);
    }
  }

  function handleDrop(event) {
    event.preventDefault();
    isDragging = false;
    const file = event.dataTransfer.files?.[0];
    if (file) {
      processFile(file);
    }
  }

  function handleDragOver(event) {
    event.preventDefault();
    isDragging = true;
  }

  function handleDragLeave() {
    isDragging = false;
  }

  const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];

  function processFile(file) {
    if (!ALLOWED_TYPES.includes(file.type)) {
      dispatch('error', { message: 'JPG, PNG, WEBP 파일만 업로드할 수 있습니다.' });
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      dispatch('error', { message: '이미지 용량은 10MB 이하여야 합니다.' });
      return;
    }
    selectedFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      previewUrl = e.target.result;
      dispatch('fileSelected', { file, previewUrl });
    };
    reader.readAsDataURL(file);
  }

  function startAnalysis() {
    if (!selectedFile) {
      dispatch('error', { message: '분석할 식물 사진을 먼저 선택해 주세요.' });
      return;
    }
    dispatch('analyze', { file: selectedFile, previewUrl });
  }

  function resetImage() {
    previewUrl = null;
    selectedFile = null;
  }

  async function loadSample(url, name) {
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error('샘플 이미지를 불러오지 못했습니다.');
      }
      const blob = await response.blob();
      const file = new File([blob], `${name}.jpg`, { type: blob.type || 'image/jpeg' });
      processFile(file);
    } catch (err) {
      dispatch('error', { message: err.message || '샘플 이미지를 불러오지 못했습니다.' });
    }
  }
</script>

<div class="upload-wrapper card">
  <div class="upload-header">
    <div class="header-icon">📸</div>
    <div>
      <h3 class="title">식물 사진 업로드</h3>
      <p class="subtitle">잎이나 꽃이 선명하게 보이도록 촬영된 사진을 올려주세요</p>
    </div>
  </div>

  {#if !previewUrl}
    <!-- 드래그 & 드롭 영역 -->
    <div
      class="dropzone {isDragging ? 'dragging' : ''}"
      role="region"
      aria-label="식물 사진 드래그 앤 드롭 영역"
      on:drop={handleDrop}
      on:dragover={handleDragOver}
      on:dragleave={handleDragLeave}
    >
      <input
        type="file"
        id="plant-file-input"
        accept="image/jpeg,image/png,image/webp"
        on:change={handleFileSelect}
        hidden
      />
      <label for="plant-file-input" class="dropzone-label">
        <div class="cloud-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="17 8 12 3 7 8" />
            <line x1="12" y1="3" x2="12" y2="15" />
          </svg>
        </div>
        <span class="main-text">사진을 이곳에 끌어다 놓거나 <strong>클릭하여 업로드</strong></span>
        <span class="sub-text">지원 형식: JPG, PNG, WEBP (최대 10MB)</span>
      </label>
    </div>

    <!-- 빠른 체험용 샘플 버튼 -->
    <div class="sample-section">
      <span class="sample-label">💡 샘플 사진으로 바로 시도:</span>
      <div class="sample-buttons">
        <button
          type="button"
          class="sample-btn"
          on:click={() => loadSample('/samples/monstera.jpg', '몬스테라')}
        >
          🌿 몬스테라
        </button>
        <button
          type="button"
          class="sample-btn"
          on:click={() => loadSample('/samples/pothos.jpg', '스킨답서스')}
        >
          🍃 스킨답서스
        </button>
        <button
          type="button"
          class="sample-btn"
          on:click={() => loadSample('/samples/echeveria.jpg', '에케베리아')}
        >
          🪴 다육식물
        </button>
      </div>
    </div>
  {:else}
    <!-- 이미지 미리보기 & 분석 트리거 영역 -->
    <div class="preview-container animate-fade-in">
      <div class="image-box">
        <img src={previewUrl} alt="업로드된 식물 미리보기" class="preview-img" />
        <button class="remove-btn" on:click={resetImage} title="다른 사진 선택">✕</button>
      </div>

      <div class="action-box">
        <div class="info-pill">
          <span>준비 완료: 식물 사진이 정상적으로 로드되었습니다</span>
        </div>
        <button
          class="btn-primary analyze-btn"
          on:click={startAnalysis}
          disabled={$isLoading}
        >
          {#if $isLoading}
            <span class="spinner"></span> AI 정밀 분석 중...
          {:else}
            🔍 AI 식물 종 식별 & 관리 가이드 생성
          {/if}
        </button>
      </div>
    </div>
  {/if}
</div>

<style>
  .upload-wrapper {
    padding: 24px;
    background: #ffffff;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
  }

  .upload-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 20px;
  }

  .header-icon {
    font-size: 2rem;
    background: var(--primary-light);
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
  }

  .title {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-main);
  }

  .subtitle {
    font-size: 0.88rem;
    color: var(--text-muted);
  }

  .dropzone {
    border: 2px dashed #95d5b2;
    background: #fbfdfb;
    border-radius: var(--radius-md);
    padding: 36px 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .dropzone:hover, .dropzone.dragging {
    border-color: var(--primary);
    background: #f0fdf4;
    transform: translateY(-2px);
  }

  .dropzone-label {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    cursor: pointer;
  }

  .cloud-icon {
    color: var(--accent);
  }

  .main-text {
    font-size: 1rem;
    color: var(--text-main);
  }

  .main-text strong {
    color: var(--primary);
    text-decoration: underline;
  }

  .sub-text {
    font-size: 0.8rem;
    color: var(--text-muted);
  }

  .sample-section {
    margin-top: 18px;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 10px;
    font-size: 0.85rem;
  }

  .sample-label {
    color: var(--text-muted);
    font-weight: 600;
  }

  .sample-buttons {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }

  .sample-btn {
    background: #edf7f0;
    color: var(--primary-hover);
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    border: 1px solid #b7e4c7;
  }

  .sample-btn:hover {
    background: var(--primary-light);
    transform: scale(1.03);
  }

  /* Preview Section */
  .preview-container {
    display: flex;
    flex-direction: column;
    gap: 18px;
  }

  .image-box {
    position: relative;
    max-height: 320px;
    overflow: hidden;
    border-radius: var(--radius-md);
    background: #000;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .preview-img {
    width: 100%;
    max-height: 320px;
    object-fit: cover;
    border-radius: var(--radius-md);
  }

  .remove-btn {
    position: absolute;
    top: 12px;
    right: 12px;
    background: rgba(0, 0, 0, 0.65);
    color: #fff;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 0.9rem;
  }

  .remove-btn:hover {
    background: #e63946;
  }

  .action-box {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .info-pill {
    background: #e8f5e9;
    color: #2e7d32;
    padding: 8px 14px;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 500;
  }

  .btn-primary {
    background: var(--primary);
    color: #ffffff;
    padding: 14px 24px;
    border-radius: var(--radius-md);
    font-size: 1rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    box-shadow: 0 4px 14px rgba(45, 106, 79, 0.25);
  }

  .btn-primary:hover:not(:disabled) {
    background: var(--primary-hover);
    transform: translateY(-2px);
  }

  .btn-primary:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  .spinner {
    width: 18px;
    height: 18px;
    border: 2px solid #ffffff;
    border-top: 2px solid transparent;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }
</style>
