/**
 * 로컬 mongod 기동 스크립트
 * 사용: npm run db:start
 * MONGOD_PATH 가 없으면 ~/mongodb-local/bin/mongod.exe 를 사용합니다.
 * 이미 27017 포트가 열려 있으면 아무것도 하지 않습니다.
 */
require('dotenv').config();
const net = require('net');
const os = require('os');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

const mongod = process.env.MONGOD_PATH || path.join(os.homedir(), 'mongodb-local', 'bin', 'mongod.exe');
const dataDir = path.join(__dirname, '../data/mongo');
const logPath = path.join(__dirname, '../data/mongod.log');

function isOpen(port) {
  return new Promise((resolve) => {
    const socket = net.connect(port, '127.0.0.1');
    socket.once('connect', () => { socket.destroy(); resolve(true); });
    socket.once('error', () => resolve(false));
  });
}

async function main() {
  if (await isOpen(27017)) {
    console.log('✅ mongod 가 이미 27017 에서 실행 중입니다.');
    return;
  }
  if (!fs.existsSync(mongod)) {
    console.error(`❌ mongod 실행 파일이 없습니다: ${mongod} (MONGOD_PATH 로 지정하세요)`);
    process.exit(1);
  }
  fs.mkdirSync(dataDir, { recursive: true });
  const child = spawn(
    mongod,
    ['--dbpath', dataDir, '--bind_ip', '127.0.0.1', '--port', '27017', '--logpath', logPath, '--logappend'],
    { detached: true, stdio: 'ignore' }
  );
  child.unref();
  for (let i = 0; i < 20; i += 1) {
    await new Promise((r) => setTimeout(r, 500));
    if (await isOpen(27017)) {
      console.log('✅ mongod 기동 완료 (127.0.0.1:27017)');
      return;
    }
  }
  console.error(`❌ mongod 기동 확인 실패. 로그: ${logPath}`);
  process.exit(1);
}

main();
