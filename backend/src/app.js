/**
 * PlantForge Backend Orchestrator (Express.js)
 */
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');

const identifyRouter = require('./routes/identify');
const plantsRouter = require('./routes/plants');
const aiClient = require('./services/aiClient');

const app = express();
const PORT = process.env.PORT || 3000;

// 미들웨어 설정
app.use(cors({
  origin: process.env.CORS_ORIGIN || '*',
  credentials: true
}));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 업로드된 이미지 정적 제공
app.use('/uploads', express.static(path.join(__dirname, '../uploads')));

// 헬스 체크 엔드포인트
app.get('/health', async (req, res) => {
  const aiHealth = await aiClient.checkHealth();
  res.status(200).json({
    service: 'PlantForge Backend Orchestrator',
    status: 'online',
    port: PORT,
    aiServer: aiHealth
  });
});

// API 라우트 마운트
app.use('/api/identify', identifyRouter);
app.use('/api/plants', plantsRouter);

// 404 핸들러
app.use((req, res, next) => {
  res.status(404).json({ success: false, message: '요청한 엔드포인트를 찾을 수 없습니다.' });
});

// 전역 에러 핸들러
app.use((err, req, res, next) => {
  console.error('서버 에러:', err.message);
  res.status(err.status || 500).json({
    success: false,
    message: err.message || '서버 내부 오류가 발생했습니다.'
  });
});

// 서버 실행
if (process.env.NODE_ENV !== 'test') {
  app.listen(PORT, () => {
    console.log(`🌿 PlantForge Backend running on http://localhost:${PORT}`);
  });
}

module.exports = app;
