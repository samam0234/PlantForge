/**
 * AI Server Client Service
 * Express -> Flask 통신 오케스트레이션
 */
const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');

const AI_SERVER_URL = process.env.AI_SERVER_URL || 'http://localhost:5000';

class AIClient {
  constructor(baseURL = AI_SERVER_URL) {
    this.client = axios.create({
      baseURL,
      timeout: 30000 // AI 모델 응답 대기 (30초)
    });
  }

  /**
   * AI Server 헬스 체크
   */
  async checkHealth() {
    try {
      const response = await this.client.get('/health');
      return response.data;
    } catch (error) {
      console.warn(`[AIClient] AI 서버에 연결할 수 없습니다 (${AI_SERVER_URL}):`, error.message);
      return { status: 'offline', error: error.message };
    }
  }

  /**
   * 식물 사진 식별 및 가이드 요청
   * @param {string} filePath - 로컬 이미지 파일 경로
   * @param {string} originalName - 원본 파일명
   */
  async identifyPlant(filePath, originalName) {
    try {
      const formData = new FormData();
      formData.append('image', fs.createReadStream(filePath), originalName);

      const response = await this.client.post('/identify', formData, {
        headers: {
          ...formData.getHeaders()
        }
      });

      return response.data;
    } catch (error) {
      console.error('[AIClient] 식별 요청 실패:', error.message);
      
      // AI 서버 미실행 시 개발 편의를 위한 Fallback 목업 반환
      return {
        status: 'mock_fallback',
        species: 'Monstera Deliciosa',
        common_name: '몬스테라 델리시오사',
        scientific_name: 'Monstera deliciosa',
        confidence: 0.95,
        candidates: [
          { species: 'Monstera Deliciosa', common_name: '몬스테라', scientific_name: 'Monstera deliciosa', confidence: 0.95 },
          { species: 'Epipremnum aureum', common_name: '스킨답서스', scientific_name: 'Epipremnum aureum', confidence: 0.81 }
        ],
        care_guide: {
          watering: '겉흙이 마르면 충분히 관수 (주 1~2회)',
          light: '밝은 간접광',
          temperature: '18~27°C',
          soil: '배수가 잘 되는 관엽식물용 흙',
          fertilizer: '생장기 월 1회 액비',
          notes: '과습에 유의하고 잎을 주기적으로 닦아주세요'
        }
      };
    }
  }
}

module.exports = new AIClient();
