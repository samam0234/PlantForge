/**
 * Database Module (MongoDB)
 * 식물 컬렉션 및 식별 기록 영속화
 */
const { MongoClient } = require('mongodb');

const uri = process.env.MONGODB_URI || 'mongodb://localhost:27017';
const dbName = process.env.MONGODB_DB || 'plantforge';

// mongodb+srv SRV 조회(querySrv ECONNREFUSED)가 막힌 환경에서 쓸 DNS 지정 (예: 8.8.8.8,1.1.1.1)
if (process.env.DNS_SERVERS) {
  require('dns').setServers(process.env.DNS_SERVERS.split(',').map((s) => s.trim()));
}

const client = new MongoClient(uri);
let db = null;

async function connect() {
  if (db) return db;
  await client.connect();
  db = client.db(dbName);
  await db.collection('plants').createIndex({ created_at: -1 });
  await db.collection('identifications').createIndex({ plant_id: 1 });
  console.log(`📦 MongoDB 연결 성공 (db: ${dbName})`);
  return db;
}

function getDb() {
  if (!db) {
    throw new Error('MongoDB가 아직 연결되지 않았습니다.');
  }
  return db;
}

async function close() {
  await client.close();
  db = null;
}

module.exports = { connect, getDb, close };
