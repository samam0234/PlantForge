/**
 * SQLite -> MongoDB 1회성 데이터 이관 스크립트
 * 사용: npm run migrate:sqlite  (backend/.env 의 MONGODB_URI 필요)
 * legacy_id 기준 upsert 이므로 여러 번 실행해도 중복되지 않습니다.
 */
require('dotenv').config();
const path = require('path');
const sqlite3 = require('sqlite3');
const { connect, close } = require('../src/db/database');

const sqlitePath = process.env.DATABASE_PATH || path.join(__dirname, '../plantforge.db');

function all(sqliteDb, sql) {
  return new Promise((resolve, reject) => {
    sqliteDb.all(sql, [], (err, rows) => (err ? reject(err) : resolve(rows)));
  });
}

// SQLite CURRENT_TIMESTAMP 는 UTC 'YYYY-MM-DD HH:MM:SS'
function toDate(value) {
  return value ? new Date(`${value.replace(' ', 'T')}Z`) : new Date();
}

function parseJson(text) {
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}

async function main() {
  const sqliteDb = new sqlite3.Database(sqlitePath, sqlite3.OPEN_READONLY);
  const db = await connect();

  const plants = await all(sqliteDb, 'SELECT * FROM plants ORDER BY id');
  const idents = await all(sqliteDb, 'SELECT * FROM identifications ORDER BY id');

  const plantIdMap = new Map();
  for (const row of plants) {
    const doc = {
      nickname: row.nickname,
      species: row.species,
      common_name: row.common_name || '',
      scientific_name: row.scientific_name || '',
      care_guide: parseJson(row.care_guide),
      image_path: row.image_path || '',
      created_at: toDate(row.created_at),
      updated_at: toDate(row.updated_at)
    };
    const result = await db.collection('plants').findOneAndUpdate(
      { legacy_id: row.id },
      { $set: doc, $setOnInsert: { legacy_id: row.id } },
      { upsert: true, returnDocument: 'after' }
    );
    plantIdMap.set(row.id, result._id);
  }

  for (const row of idents) {
    const doc = {
      // 원본 plants 에 없는(이미 삭제된) 식물 참조는 null 처리
      plant_id: plantIdMap.get(row.plant_id) || null,
      confidence: row.confidence,
      raw_result: parseJson(row.raw_result),
      created_at: toDate(row.created_at)
    };
    await db.collection('identifications').updateOne(
      { legacy_id: row.id },
      { $set: doc, $setOnInsert: { legacy_id: row.id } },
      { upsert: true }
    );
  }

  console.log(`✅ 이관 완료: plants ${plants.length}건, identifications ${idents.length}건`);
  sqliteDb.close();
  await close();
}

main().catch((err) => {
  console.error('❌ 이관 실패:', err.message);
  process.exit(1);
});
