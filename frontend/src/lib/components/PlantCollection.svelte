<script>
  import { plantCollection } from '../stores/plants.js';

  let selectedPlant = null;

  function removePlant(id, event) {
    event.stopPropagation();
    if (confirm('이 식물을 내 컬렉션에서 삭제하시겠습니까?')) {
      plantCollection.update(list => list.filter(item => item.id !== id));
      if (selectedPlant?.id === id) {
        selectedPlant = null;
      }
    }
  }

  function openDetails(plant) {
    selectedPlant = plant;
  }

  function closeDetails() {
    selectedPlant = null;
  }
</script>

<div class="collection-wrapper animate-fade-in">
  <div class="collection-header">
    <div>
      <h2 class="title">🌿 내 식물 정원 (My Plants)</h2>
      <p class="subtitle">등록된 반려식물 { $plantCollection.length }그루를 함께 가꿔요</p>
    </div>
  </div>

  {#if $plantCollection.length === 0}
    <div class="empty-state card">
      <div class="empty-icon">🌱</div>
      <h3>아직 등록된 식물이 없습니다</h3>
      <p>식물 사진을 업로드하고 AI 분석을 통해 내 식물 컬렉션에 등록해보세요!</p>
    </div>
  {:else}
    <div class="plant-grid">
      {#each $plantCollection as plant (plant.id)}
        <div
          class="plant-card card"
          role="button"
          tabindex="0"
          on:click={() => openDetails(plant)}
          on:keydown={(e) => (e.key === 'Enter' || e.key === ' ') && openDetails(plant)}
        >
          <div class="img-wrapper">
            <img src={plant.image_path} alt={plant.nickname} class="plant-img" />
            <button
              type="button"
              class="del-btn"
              on:click={(e) => removePlant(plant.id, e)}
              title="컬렉션에서 삭제"
            >
              ✕
            </button>
          </div>
          <div class="plant-body">
            <div class="title-row">
              <h4 class="plant-nickname">{plant.nickname}</h4>
              <span class="reg-date">{plant.created_at}</span>
            </div>
            <p class="plant-species">{plant.common_name || plant.species}</p>
            <p class="plant-scientific"><i>{plant.scientific_name || ''}</i></p>

            <div class="tags">
              <span class="care-badge">💧 주 1~2회</span>
              <span class="care-badge">☀️ 반양지</span>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}

  <!-- 식물 상세 가이드 모달 -->
  {#if selectedPlant}
    <div
      class="modal-overlay"
      role="dialog"
      aria-modal="true"
      tabindex="-1"
      on:click={closeDetails}
      on:keydown={(e) => e.key === 'Escape' && closeDetails()}
    >
      <div
        class="modal-content card"
        role="document"
        on:click|stopPropagation
        on:keydown|stopPropagation
      >
        <button class="modal-close-btn" on:click={closeDetails}>✕</button>
        <div class="modal-header">
          <img src={selectedPlant.image_path} alt={selectedPlant.nickname} class="modal-img" />
          <div class="modal-info">
            <span class="badge badge-green">반려식물 프로필</span>
            <h2>{selectedPlant.nickname}</h2>
            <p class="modal-species">{selectedPlant.common_name || selectedPlant.species} ({selectedPlant.scientific_name})</p>
            <p class="modal-date">등록일: {selectedPlant.created_at}</p>
          </div>
        </div>

        <div class="modal-body">
          <h4 class="section-title">🪴 상세 케어 가이드</h4>
          {#if selectedPlant.care_guide}
            <div class="guide-list">
              <div class="guide-item">
                <strong>💧 물주기:</strong> {selectedPlant.care_guide.watering}
              </div>
              <div class="guide-item">
                <strong>☀️ 햇빛:</strong> {selectedPlant.care_guide.light}
              </div>
              <div class="guide-item">
                <strong>🌡️ 온도:</strong> {selectedPlant.care_guide.temperature}
              </div>
              <div class="guide-item">
                <strong>🌱 토양:</strong> {selectedPlant.care_guide.soil}
              </div>
              <div class="guide-item">
                <strong>⚠️ 주의사항:</strong> {selectedPlant.care_guide.notes}
              </div>
            </div>
          {:else}
            <p>등록된 관리 가이드 정보가 없습니다.</p>
          {/if}
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .collection-wrapper {
    margin-top: 10px;
  }

  .collection-header {
    margin-bottom: 24px;
  }

  .title {
    font-size: 1.4rem;
    font-weight: 800;
    color: var(--text-main);
  }

  .subtitle {
    font-size: 0.9rem;
    color: var(--text-muted);
  }

  .empty-state {
    text-align: center;
    padding: 60px 20px;
    background: #fff;
    border-radius: var(--radius-lg);
  }

  .empty-icon {
    font-size: 3.5rem;
    margin-bottom: 12px;
  }

  .empty-state h3 {
    font-size: 1.2rem;
    color: var(--text-main);
    margin-bottom: 6px;
  }

  .empty-state p {
    font-size: 0.9rem;
    color: var(--text-muted);
  }

  .plant-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 22px;
  }

  .plant-card {
    background: #fff;
    border-radius: var(--radius-lg);
    overflow: hidden;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  .plant-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-md);
  }

  .img-wrapper {
    position: relative;
    height: 200px;
    overflow: hidden;
  }

  .plant-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
  }

  .plant-card:hover .plant-img {
    transform: scale(1.04);
  }

  .del-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background: rgba(0, 0, 0, 0.6);
    color: #fff;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    font-size: 0.8rem;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .del-btn:hover {
    background: #e63946;
  }

  .plant-body {
    padding: 18px;
  }

  .title-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 4px;
  }

  .plant-nickname {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-main);
  }

  .reg-date {
    font-size: 0.75rem;
    color: var(--text-muted);
  }

  .plant-species {
    font-size: 0.9rem;
    color: var(--primary);
    font-weight: 600;
  }

  .plant-scientific {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-bottom: 12px;
  }

  .tags {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
  }

  .care-badge {
    background: #f1f8f3;
    color: var(--primary-hover);
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.76rem;
    font-weight: 600;
  }

  /* Modal */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 20px;
    backdrop-filter: blur(3px);
  }

  .modal-content {
    background: #fff;
    max-width: 600px;
    width: 100%;
    max-height: 85vh;
    overflow-y: auto;
    border-radius: var(--radius-lg);
    padding: 26px;
    position: relative;
    animation: fadeIn 0.3s ease;
  }

  .modal-close-btn {
    position: absolute;
    top: 18px;
    right: 18px;
    background: #f1f3f5;
    border-radius: 50%;
    width: 34px;
    height: 34px;
    font-size: 1rem;
    color: var(--text-muted);
  }

  .modal-header {
    display: flex;
    gap: 18px;
    margin-bottom: 20px;
    align-items: center;
  }

  .modal-img {
    width: 110px;
    height: 110px;
    border-radius: var(--radius-md);
    object-fit: cover;
  }

  .modal-info h2 {
    font-size: 1.4rem;
    color: var(--text-main);
    margin: 4px 0;
  }

  .modal-species {
    font-size: 0.9rem;
    color: var(--primary);
    font-weight: 600;
  }

  .modal-date {
    font-size: 0.8rem;
    color: var(--text-muted);
  }

  .section-title {
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 12px;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 8px;
  }

  .guide-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    font-size: 0.9rem;
  }

  .guide-item {
    background: #f9fbf9;
    padding: 10px 14px;
    border-radius: 8px;
    border-left: 3px solid var(--primary);
  }
</style>
