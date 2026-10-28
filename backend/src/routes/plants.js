/**
 * Plants Collection CRUD Routes
 * 내 식물 목록 관리 API
 */
const express = require('express');
const { ObjectId } = require('mongodb');
const router = express.Router();
const { getDb } = require('../db/database');

function formatPlant(doc) {
  if (!doc) return null;
  const { _id, ...rest } = doc;
  return { ...rest, id: _id.toString() };
}

function toObjectId(value) {
  return ObjectId.isValid(value) ? new ObjectId(value) : null;
}

// GET /api/plants - 내 식물 목록 조회
router.get('/', async (req, res) => {
  try {
    const docs = await getDb().collection('plants').find().sort({ created_at: -1 }).toArray();
    return res.status(200).json({ success: true, plants: docs.map(formatPlant) });
  } catch (err) {
    return res.status(500).json({ success: false, message: err.message });
  }
});

// GET /api/plants/:id - 특정 식물 조회
router.get('/:id', async (req, res) => {
  try {
    const _id = toObjectId(req.params.id);
    const doc = _id && await getDb().collection('plants').findOne({ _id });
    if (!doc) {
      return res.status(404).json({ success: false, message: '식물을 찾을 수 없습니다.' });
    }
    return res.status(200).json({ success: true, plant: formatPlant(doc) });
  } catch (err) {
    return res.status(500).json({ success: false, message: err.message });
  }
});

// POST /api/plants - 컬렉션에 식물 추가
router.post('/', async (req, res) => {
  const { nickname, species, common_name, scientific_name, care_guide, image_path, identification_id } = req.body;

  if (!nickname || !species) {
    return res.status(400).json({
      success: false,
      message: '식물 닉네임과 종 이름은 필수입니다.'
    });
  }

  try {
    const now = new Date();
    const doc = {
      nickname,
      species,
      common_name: common_name || '',
      scientific_name: scientific_name || '',
      care_guide: care_guide && typeof care_guide === 'object' ? care_guide : null,
      image_path: image_path || '',
      created_at: now,
      updated_at: now
    };

    const database = getDb();
    const { insertedId } = await database.collection('plants').insertOne(doc);

    const identificationId = toObjectId(identification_id);
    if (identificationId) {
      await database.collection('identifications').updateOne(
        { _id: identificationId },
        { $set: { plant_id: insertedId } }
      );
    }

    return res.status(201).json({
      success: true,
      id: insertedId.toString(),
      plant: formatPlant({ _id: insertedId, ...doc }),
      message: '식물이 컬렉션에 등록되었습니다.'
    });
  } catch (err) {
    return res.status(500).json({ success: false, message: err.message });
  }
});

// DELETE /api/plants/:id - 컬렉션에서 식물 삭제
router.delete('/:id', async (req, res) => {
  try {
    const _id = toObjectId(req.params.id);
    const database = getDb();
    const result = _id && await database.collection('plants').deleteOne({ _id });
    if (!result || result.deletedCount === 0) {
      return res.status(404).json({ success: false, message: '삭제할 식물을 찾을 수 없습니다.' });
    }
    // 기존 FK ON DELETE SET NULL 동작 유지
    await database.collection('identifications').updateMany(
      { plant_id: _id },
      { $set: { plant_id: null } }
    );
    return res.status(200).json({ success: true, message: '식물이 삭제되었습니다.' });
  } catch (err) {
    return res.status(500).json({ success: false, message: err.message });
  }
});

module.exports = router;
