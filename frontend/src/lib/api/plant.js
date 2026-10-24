/**
 * PlantForge Frontend API Client
 * 백엔드 Express 오케스트레이터와의 통신
 */

export const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:3000';

export function resolveImageUrl(path) {
  if (!path) return '';
  if (path.startsWith('http') || path.startsWith('data:') || path.startsWith('blob:')) {
    return path;
  }
  return `${API_BASE}${path.startsWith('/') ? '' : '/'}${path}`;
}

async function parseResponse(response, fallbackMessage) {
  let body = null;
  try {
    body = await response.json();
  } catch {
    body = null;
  }
  if (!response.ok || body?.success === false) {
    throw new Error(body?.message || fallbackMessage);
  }
  return body;
}

/**
 * 식물 사진 업로드 및 식별 요청
 * @param {File} file
 */
export async function getHealthApi() {
  const response = await fetch(`${API_BASE}/health`);
  if (!response.ok) {
    throw new Error('백엔드 상태를 확인하지 못했습니다.');
  }
  return response.json();
}

export async function identifyPlantApi(file) {
  const formData = new FormData();
  formData.append('image', file);

  const response = await fetch(`${API_BASE}/api/identify`, {
    method: 'POST',
    body: formData
  });

  return parseResponse(response, '식물 식별 요청에 실패했습니다.');
}

/**
 * 내 식물 컬렉션 목록 조회
 */
export async function getPlantsApi() {
  const response = await fetch(`${API_BASE}/api/plants`);
  return parseResponse(response, '식물 목록을 불러오지 못했습니다.');
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

  return parseResponse(response, '식물을 컬렉션에 추가하지 못했습니다.');
}

/**
 * 식물 컬렉션에서 삭제
 * @param {number} id
 */
export async function deletePlantApi(id) {
  const response = await fetch(`${API_BASE}/api/plants/${id}`, {
    method: 'DELETE'
  });

  return parseResponse(response, '식물을 삭제하지 못했습니다.');
}
