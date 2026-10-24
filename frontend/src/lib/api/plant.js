/**
 * PlantForge Frontend API Client
 * 백엔드 Express 오케스트레이터와의 통신
 */

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:3000';

/**
 * 식물 사진 업로드 및 식별 요청
 * @param {File} file
 */
export async function identifyPlantApi(file) {
  const formData = new FormData();
  formData.append('image', file);

  const response = await fetch(`${API_BASE}/api/identify`, {
    method: 'POST',
    body: formData
  });

  if (!response.ok) {
    throw new Error(`식별 요청 실패: ${response.statusText}`);
  }

  return await response.json();
}

/**
 * 내 식물 컬렉션 목록 조회
 */
export async function getPlantsApi() {
  const response = await fetch(`${API_BASE}/api/plants`);
  if (!response.ok) {
    throw new Error(`식물 목록 조회 실패: ${response.statusText}`);
  }
  return await response.json();
}

/**
 * 식물 컬렉션에 추가
 * @param {Object} plantData
 */
export async function addPlantApi(plantData) {
  const response = await fetch(`${API_BASE}/api/plants`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(plantData)
  });

  if (!response.ok) {
    throw new Error(`식물 추가 실패: ${response.statusText}`);
  }

  return await response.json();
}

/**
 * 식물 컬렉션에서 삭제
 * @param {number} id
 */
export async function deletePlantApi(id) {
  const response = await fetch(`${API_BASE}/api/plants/${id}`, {
    method: 'DELETE'
  });

  if (!response.ok) {
    throw new Error(`식물 삭제 실패: ${response.statusText}`);
  }

  return await response.json();
}
