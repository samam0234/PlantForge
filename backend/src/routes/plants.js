/**
 * Plants Collection CRUD Routes
 * 내 식물 목록 관리 API
 */
const express = require('express');
const router = express.Router();
const db = require('../db/database');

// GET /api/plants - 내 식물 목록 조회
router.get('/', (req, res) => {
  const sql = `SELECT * FROM plants ORDER BY created_at DESC`;
  db.all(sql, [], (err, rows) => {
    if (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
    const formatted = rows.map(row => ({
      ...row,
      care_guide: row.care_guide ? JSON.parse(row.care_guide) : null
    }));
    return res.status(200).json({ success: true, plants: formatted });
  });
});

// GET /api/plants/:id - 특정 식물 조회
router.get('/:id', (req, res) => {
  const { id } = req.params;
  const sql = `SELECT * FROM plants WHERE id = ?`;
  db.get(sql, [id], (err, row) => {
    if (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
    if (!row) {
      return res.status(404).json({ success: false, message: '식물을 찾을 수 없습니다.' });
    }
    return res.status(200).json({
      success: true,
      plant: {
        ...row,
        care_guide: row.care_guide ? JSON.parse(row.care_guide) : null
      }
    });
  });
});

// POST /api/plants - 컬렉션에 식물 추가
router.post('/', (req, res) => {
  const { nickname, species, scientific_name, care_guide, image_path } = req.body;

  if (!nickname || !species) {
    return res.status(400).json({
      success: false,
      message: '식물 닉네임과 종 이름은 필수입니다.'
    });
  }

  const sql = `
    INSERT INTO plants (nickname, species, scientific_name, care_guide, image_path)
    VALUES (?, ?, ?, ?, ?)
  `;
  const guideJson = typeof care_guide === 'object' ? JSON.stringify(care_guide) : care_guide;

  db.run(sql, [nickname, species, scientific_name || '', guideJson, image_path || ''], function (err) {
    if (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
    return res.status(201).json({
      success: true,
      id: this.lastID,
      message: '식물이 컬렉션에 성공적으로 등록되었습니다.'
    });
  });
});

// DELETE /api/plants/:id - 컬렉션에서 식물 삭제
router.delete('/:id', (req, res) => {
  const { id } = req.params;
  const sql = `DELETE FROM plants WHERE id = ?`;
  db.run(sql, [id], function (err) {
    if (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
    if (this.changes === 0) {
      return res.status(404).json({ success: false, message: '삭제할 식물을 찾을 수 없습니다.' });
    }
    return res.status(200).json({ success: true, message: '식물이 삭제되었습니다.' });
  });
});

module.exports = router;
