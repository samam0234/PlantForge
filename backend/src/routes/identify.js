/**
 * Identify API Route
 * 이미지 업로드 및 Flask AI 분석 요청
 */
const express = require('express');
const router = express.Router();
const upload = require('../middleware/upload');
const aiClient = require('../services/aiClient');
const db = require('../db/database');

// POST /api/identify
router.post('/', upload.single('image'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        success: false,
        message: '식물 사진 파일을 업로드해주세요.'
      });
    }

    const { path: filePath, originalname, filename } = req.file;

    // AI Server 호출
    const aiResult = await aiClient.identifyPlant(filePath, originalname);

    // 식별 로그 기록 (identifications 테이블)
    const sql = `
      INSERT INTO identifications (confidence, raw_result)
      VALUES (?, ?)
    `;
    db.run(sql, [aiResult.confidence || 0, JSON.stringify(aiResult)], function (err) {
      if (err) {
        console.warn('식별 로그 저장 실패:', err.message);
      }
    });

    return res.status(200).json({
      success: true,
      imageUrl: `/uploads/${filename}`,
      data: aiResult
    });
  } catch (error) {
    console.error('식물 식별 중 오류 발생:', error);
    return res.status(500).json({
      success: false,
      message: '식물 식별 처리 중 오류가 발생했습니다.',
      error: error.message
    });
  }
});

module.exports = router;
