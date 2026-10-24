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
      timeout: 60000
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
        },
        maxBodyLength: Infinity,
        maxContentLength: Infinity
      });

      if (response.data?.status === 'error') {
        const err = new Error(response.data.message || 'AI 서버가 식별에 실패했습니다.');
        err.status = 502;
        throw err;
      }

      return response.data;
    } catch (error) {
      if (error.response) {
        const message = error.response.data?.message || 'AI 서버가 식별 요청을 처리하지 못했습니다.';
        const err = new Error(message);
        err.status = error.response.status || 502;
        throw err;
      }
      if (!error.status) {
        const err = new Error('AI 서버에 연결할 수 없습니다. Flask 서버(포트 5000)가 실행 중인지 확인해 주세요.');
        err.status = 502;
        throw err;
      }
      throw error;
    }
  }
}

module.exports = new AIClient();
