import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 启动 Flask 后端
const startBackend = () => {
  console.log('正在启动后端服务器...');
  const backend = spawn('python', ['backend/app.py'], {
    stdio: 'inherit',
    shell: true,
    env: { 
      ...process.env, 
      FLASK_APP: 'app.py',
      FLASK_ENV: 'development',
      PYTHONPATH: dirname(__filename) + '/backend'
    }
  });

  return new Promise((resolve, reject) => {
    backend.on('error', (err) => {
      console.error('后端启动失败:', err);
      reject(err);
    });

    // 等待一段时间确保后端启动
    setTimeout(() => {
      console.log('后端服务器已启动');
      resolve(backend);
    }, 2000);
  });
};

// 启动 React 前端
const startFrontend = () => {
  console.log('正在启动前端服务器...');
  const frontend = spawn('react-scripts', ['start'], {
    stdio: 'inherit',
    shell: true,
    env: { ...process.env }
  });

  return new Promise((resolve, reject) => {
    frontend.on('error', (err) => {
      console.error('前端启动失败:', err);
      reject(err);
    });

    setTimeout(() => {
      console.log('前端服务器已启动');
      resolve(frontend);
    }, 3000);
  });
};

// 按顺序启动服务
const startServers = async () => {
  try {
    const backend = await startBackend();
    const frontend = await startFrontend();

    process.on('SIGINT', () => {
      console.log('正在关闭服务器...');
      backend.kill();
      frontend.kill();
      process.exit();
    });
  } catch (error) {
    console.error('启动服务器时出错:', error);
    process.exit(1);
  }
};

startServers();
