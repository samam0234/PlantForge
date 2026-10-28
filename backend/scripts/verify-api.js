/**
 * MongoDB 전환 후 API 스모크 테스트
 * 사용: npm run verify:api  (backend/.env 의 MONGODB_URI 필요)
 * 임시 식물/식별 기록을 만들고 모두 정리합니다. 기존 데이터는 건드리지 않습니다.
 */
process.env.NODE_ENV = 'test';
require('dotenv').config();
const assert = require('assert');
const app = require('../src/app');
const { connect, getDb, close } = require('../src/db/database');

async function main() {
  await connect();
  const server = app.listen(0);
  const base = `http://127.0.0.1:${server.address().port}`;
  const call = async (method, url, body) => {
    const res = await fetch(base + url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined
    });
    return { status: res.status, json: await res.json() };
  };

  try {
    const { insertedId } = await getDb().collection('identifications').insertOne({
      plant_id: null, confidence: 0.9, raw_result: { test: true }, created_at: new Date()
    });

    let r = await call('POST', '/api/plants', {
      nickname: '__verify__', species: 'Epipremnum aureum',
      care_guide: { water: 'weekly' }, identification_id: insertedId.toString()
    });
    assert.strictEqual(r.status, 201, 'POST 201');
    const id = r.json.id;
    assert.strictEqual(typeof id, 'string');
    assert.deepStrictEqual(r.json.plant.care_guide, { water: 'weekly' });
    console.log('✔ POST /api/plants');

    const linked = await getDb().collection('identifications').findOne({ _id: insertedId });
    assert.strictEqual(linked.plant_id.toString(), id, 'identification 연결');
    console.log('✔ identification ↔ plant 연결');

    r = await call('GET', '/api/plants');
    assert.ok(r.json.plants.some((p) => p.id === id), 'list 에 포함');
    console.log('✔ GET /api/plants');

    r = await call('GET', `/api/plants/${id}`);
    assert.strictEqual(r.status, 200);
    assert.strictEqual(r.json.plant.nickname, '__verify__');
    console.log('✔ GET /api/plants/:id');

    r = await call('GET', '/api/plants/not-an-id');
    assert.strictEqual(r.status, 404);
    console.log('✔ 잘못된 id → 404');

    r = await call('POST', '/api/plants', { nickname: 'x' });
    assert.strictEqual(r.status, 400);
    console.log('✔ 필수값 누락 → 400');

    r = await call('DELETE', `/api/plants/${id}`);
    assert.strictEqual(r.status, 200);
    const unlinked = await getDb().collection('identifications').findOne({ _id: insertedId });
    assert.strictEqual(unlinked.plant_id, null, '삭제 시 plant_id null');
    console.log('✔ DELETE /api/plants/:id (+ plant_id null)');

    r = await call('DELETE', `/api/plants/${id}`);
    assert.strictEqual(r.status, 404);
    console.log('✔ 재삭제 → 404');

    await getDb().collection('identifications').deleteOne({ _id: insertedId });
    console.log('🎉 API 검증 모두 통과');
  } finally {
    server.close();
  }
  await close();
}

main().catch((err) => {
  console.error('❌ 검증 실패:', err.message);
  process.exit(1);
});
