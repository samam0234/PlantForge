/**
 * Identify API Route
 * 이미지 업로드 및 Flask AI 분석 요청
 */
const express = require('express');
const fs = require('fs');
const router = express.Router();
const upload = require('../middleware/upload');
const aiClient = require('../services/aiClient');
const db = require('../db/database');

function receiveImage(req, res, next) {
  upload.single('image')(req, res, (err) => {
    if (!err) {
      next();
      return;
    }
    const message = err.code === 'LIMIT_FILE_SIZE'
      ? '이미지 용량은 10MB 이하여야 합니다.'
      : (err.message || '이미지를 업로드하지 못했습니다.');
    res.status(400).json({ success: false, message });
  });
}

// POST /api/identify
router.post('/', receiveImage, async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        success: false,
        message: '식물 사진 파일을 업로드해 주세요.'
      });
    }

    const { path: filePath, originalname, filename } = req.file;
    const aiResult = await aiClient.identifyPlant(filePath, originalname);
    const sql = `
      INSERT INTO identifications (confidence, raw_result)
      VALUES (?, ?)
    `;

    db.run(sql, [aiResult.confidence || 0, JSON.stringify(aiResult)], function (err) {
      if (err) {
        console.warn('식별 로그 저장 실패:', err.message);
      }
      return res.status(200).json({
        success: true,
        imageUrl: `/uploads/${filename}`,
        identificationId: err ? null : this.lastID,
        data: aiResult
      });
    });
  } catch (error) {
    console.error('식물 식별 중 오류 발생:', error.message);
    if (req.file?.path) {
      fs.unlink(req.file.path, () => {});
    }
    return res.status(error.status || 500).json({
      success: false,
      message: error.message || '식물 식별 처리 중 오류가 발생했습니다.'
    });
  }
});

module.exports = router;
