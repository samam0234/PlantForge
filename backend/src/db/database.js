/**
 * Database Module (SQLite)
 * 식물 컬렉션 및 식별 기록 영속화
 */
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

const dbPath = process.env.DATABASE_PATH || path.join(__dirname, '../../plantforge.db');

// DB 디렉터리 확인
const dbDir = path.dirname(dbPath);
if (!fs.existsSync(dbDir)) {
  fs.mkdirSync(dbDir, { recursive: true });
}

const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('❌ SQLite 연결 실패:', err.message);
  } else {
    console.log(`📦 SQLite 연결 성공 (${dbPath})`);
  }
});

// 테이블 스키마 초기화
db.serialize(() => {
  // 1. plants 테이블 (내 식물 컬렉션)
  db.run(`
    CREATE TABLE IF NOT EXISTS plants (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nickname TEXT NOT NULL,
      species TEXT NOT NULL,
      common_name TEXT,
      scientific_name TEXT,
      care_guide TEXT,
      image_path TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // 2. identifications 테이블 (식별 기록 로그)
  db.run(`
    CREATE TABLE IF NOT EXISTS identifications (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      plant_id INTEGER,
      confidence REAL,
      raw_result TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY(plant_id) REFERENCES plants(id) ON DELETE SET NULL
    )
  `);

  db.all(`PRAGMA table_info(plants)`, (err, columns) => {
    if (err) {
      console.warn('plants 스키마 확인 실패:', err.message);
      return;
    }
    const names = columns.map((column) => column.name);
    if (!names.includes('common_name')) {
      db.run(`ALTER TABLE plants ADD COLUMN common_name TEXT`);
    }
  });
});

module.exports = db;
