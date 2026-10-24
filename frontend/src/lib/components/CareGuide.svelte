<script>
  export let guide = {};
  export let speciesName = '';
</script>

<div class="care-guide-container card animate-fade-in">
  <div class="guide-header">
    <div class="title-row">
      <span class="icon">🪴</span>
      <h3 class="guide-title">
        {speciesName ? `${speciesName} 맞춤형 관리 가이드` : '식물 관리 가이드'}
      </h3>
    </div>
    <span class="badge badge-green">AI 케어 닥터</span>
  </div>

  <div class="guide-grid">
    <!-- 물주기 -->
    <div class="guide-card watering">
      <div class="card-top">
        <span class="card-icon">💧</span>
        <span class="card-label">물주기 (Watering)</span>
      </div>
      <p class="card-desc">{guide.watering || '겉흙이 마르면 듬뿍 물을 주세요 (주 1~2회)'}</p>
    </div>

    <!-- 채광 -->
    <div class="guide-card light">
      <div class="card-top">
        <span class="card-icon">☀️</span>
        <span class="card-label">햇빛 & 조명 (Light)</span>
      </div>
      <p class="card-desc">{guide.light || '직사광선을 피한 밝은 간접광이 가장 적합합니다'}</p>
    </div>

    <!-- 온도 -->
    <div class="guide-card temp">
      <div class="card-top">
        <span class="card-icon">🌡️</span>
        <span class="card-label">적정 온도 (Temperature)</span>
      </div>
      <p class="card-desc">{guide.temperature || '18~27°C (겨울철 최저 13°C 이상 유지)'}</p>
    </div>

    <!-- 토양 -->
    <div class="guide-card soil">
      <div class="card-top">
        <span class="card-icon">🌱</span>
        <span class="card-label">토양 & 분갈이 (Soil)</span>
      </div>
      <p class="card-desc">{guide.soil || '배수가 원활한 관엽 전용토 및 펄라이트 배합 추천'}</p>
    </div>

    <!-- 비료 -->
    <div class="guide-card fertilizer">
      <div class="card-top">
        <span class="card-icon">🧪</span>
        <span class="card-label">영양 & 비료 (Fertilizer)</span>
      </div>
      <p class="card-desc">{guide.fertilizer || '생장기(봄~가을) 동안 월 1회 액비 희석 공급'}</p>
    </div>

    <!-- 주의사항 & 독성 -->
    <div class="guide-card notes">
      <div class="card-top">
        <span class="card-icon">⚠️</span>
        <span class="card-label">주의사항 & 반려동물 (Notes)</span>
      </div>
      <p class="card-desc">{guide.notes || '반려동물에게 가벼운 독성이 있을 수 있으니 주의하세요'}</p>
    </div>
  </div>

  <!-- 보너스 케어 팁 배너 -->
  <div class="seasonal-tip">
    <span class="tip-badge">💡 식물 집사의 꿀팁</span>
    <span class="tip-text">
      잎 표면에 분무기로 자주 미온수를 뿌려주면 공중 습도를 유지하고 해충 발생을 예방할 수 있습니다.
    </span>
  </div>
</div>

<style>
  .care-guide-container {
    padding: 26px;
    background: #ffffff;
    border-radius: var(--radius-lg);
  }

  .guide-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 22px;
  }

  .title-row {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .icon {
    font-size: 1.6rem;
  }

  .guide-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-main);
  }

  .guide-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 16px;
  }

  .guide-card {
    padding: 18px;
    border-radius: var(--radius-md);
    background: #f8faf8;
    border: 1px solid #eef3ef;
    display: flex;
    flex-direction: column;
    gap: 10px;
    transition: transform 0.2s ease, border-color 0.2s ease;
  }

  .guide-card:hover {
    transform: translateY(-2px);
    border-color: #b7e4c7;
    background: #ffffff;
    box-shadow: 0 4px 12px rgba(45, 106, 79, 0.05);
  }

  .card-top {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .card-icon {
    font-size: 1.3rem;
  }

  .card-label {
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--text-muted);
    letter-spacing: 0.03em;
  }

  .card-desc {
    font-size: 0.92rem;
    color: var(--text-main);
    line-height: 1.5;
  }

  /* 개별 카드 포인트 */
  .guide-card.notes {
    background: #fffdf5;
    border-color: #fef3c7;
  }

  .guide-card.notes:hover {
    border-color: #fde68a;
  }

  .seasonal-tip {
    margin-top: 20px;
    background: #f0fdf4;
    border: 1px solid #dcfce7;
    border-radius: var(--radius-md);
    padding: 14px 18px;
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
  }

  .tip-badge {
    background: var(--primary);
    color: #fff;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 9999px;
  }

  .tip-text {
    font-size: 0.88rem;
    color: var(--primary-hover);
    font-weight: 500;
  }
</style>
