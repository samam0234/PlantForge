<script>
  import { createEventDispatcher } from 'svelte';
  import { plantCollection } from '../stores/plants.js';

  export let result;

  const dispatch = createEventDispatcher();
  let nickname = '';
  let isSaving = false;
  let saveSuccess = false;

  $: confidencePercentage = Math.round((result?.confidence || 0) * 100);

  function handleAddToCollection() {
    if (!nickname.trim()) {
      nickname = result.common_name || result.species;
    }

    isSaving = true;

    // 컬렉션 스토어에 추가
    const newPlant = {
      id: Date.now(),
      nickname: nickname.trim(),
      species: result.species,
      common_name: result.common_name,
      scientific_name: result.scientific_name,
      image_path: result.imageUrl || 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=600&q=80',
      created_at: new Date().toISOString().split('T')[0],
      care_guide: result.care_guide
    };

    plantCollection.update(list => [newPlant, ...list]);

    setTimeout(() => {
      isSaving = false;
      saveSuccess = true;
      dispatch('added', newPlant);
      setTimeout(() => (saveSuccess = false), 3000);
    }, 400);
  }
</script>

<div class="result-card card animate-fade-in">
  <div class="card-badge-row">
    <span class="badge badge-green">{result.provider === 'openai-vision' ? 'Vision 식별 완료' : '카탈로그 추정 완료'}</span>
    <span class="match-score">일치도 <strong>{confidencePercentage}%</strong></span>
  </div>

  <div class="main-info">
    <div class="names">
      <h2 class="common-name">{result.common_name || result.species}</h2>
      <p class="scientific-name"><i>{result.scientific_name || result.species}</i></p>
    </div>
    <div class="meter-container">
      <div class="meter-bar">
        <div class="meter-fill" style="width: {confidencePercentage}%"></div>
      </div>
    </div>
  </div>

  {#if result.analysis_note}
    <p class="analysis-note">{result.analysis_note}</p>
  {/if}

  <!-- 상위 후보 2~3위 리스트 -->
  {#if result.candidates && result.candidates.length > 1}
    <div class="candidates-box">
      <span class="candidates-title">유사 후보군:</span>
      <div class="candidate-chips">
        {#each result.candidates.slice(1, 3) as candidate}
          <div class="candidate-chip">
            <span class="cand-name">{candidate.common_name || candidate.species}</span>
            <span class="cand-score">{Math.round((candidate.confidence || 0) * 100)}%</span>
          </div>
        {/each}
      </div>
    </div>
  {/if}

  <!-- 내 식물 컬렉션 저장 영역 -->
  <div class="save-box">
    <div class="input-group">
      <input
        type="text"
        placeholder="나만의 식물 애칭 (예: 쑥쑥이)"
        bind:value={nickname}
        class="nickname-input"
      />
      <button
        class="btn-save {saveSuccess ? 'btn-saved' : ''}"
        on:click={handleAddToCollection}
        disabled={isSaving}
      >
        {#if saveSuccess}
          ✓ 내 식물에 저장됨!
        {:else if isSaving}
          저장 중...
        {:else}
          🌱 내 식물에 추가
        {/if}
      </button>
    </div>
  </div>
</div>

<style>
  .result-card {
    padding: 24px;
    background: #ffffff;
    border-radius: var(--radius-lg);
    border-left: 5px solid var(--accent);
  }

  .card-badge-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }

  .match-score {
    font-size: 0.9rem;
    color: var(--primary);
  }

  .match-score strong {
    font-size: 1.1rem;
    color: var(--primary-hover);
  }

  .common-name {
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--text-main);
    letter-spacing: -0.02em;
  }

  .scientific-name {
    font-size: 0.95rem;
    color: var(--text-muted);
    margin-top: 2px;
  }

  .analysis-note {
    margin-top: 12px;
    font-size: 0.84rem;
    color: var(--text-muted);
    line-height: 1.45;
  }

  .meter-container {
    margin-top: 14px;
  }

  .meter-bar {
    width: 100%;
    height: 8px;
    background: #e9ecef;
    border-radius: 9999px;
    overflow: hidden;
  }

  .meter-fill {
    height: 100%;
    background: linear-gradient(90deg, #52b788, #2d6a4f);
    border-radius: 9999px;
    transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .candidates-box {
    margin-top: 20px;
    padding-top: 16px;
    border-top: 1px dashed var(--border-color);
  }

  .candidates-title {
    font-size: 0.82rem;
    color: var(--text-muted);
    font-weight: 600;
    display: block;
    margin-bottom: 8px;
  }

  .candidate-chips {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }

  .candidate-chip {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #f4f8f5;
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 0.85rem;
    border: 1px solid #e1eee5;
  }

  .cand-name {
    color: var(--text-main);
    font-weight: 500;
  }

  .cand-score {
    color: var(--primary);
    font-weight: 700;
    font-size: 0.8rem;
  }

  .save-box {
    margin-top: 22px;
    padding-top: 16px;
    border-top: 1px solid var(--border-color);
  }

  .input-group {
    display: flex;
    gap: 10px;
  }

  .nickname-input {
    flex: 1;
    padding: 10px 14px;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    font-size: 0.92rem;
    transition: border 0.2s ease;
  }

  .nickname-input:focus {
    outline: none;
    border-color: var(--primary);
  }

  .btn-save {
    background: var(--primary);
    color: #fff;
    padding: 10px 18px;
    border-radius: var(--radius-sm);
    font-size: 0.92rem;
    font-weight: 600;
    white-space: nowrap;
  }

  .btn-save:hover {
    background: var(--primary-hover);
  }

  .btn-saved {
    background: #2e7d32 !important;
  }
</style>
