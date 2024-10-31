import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 启动 Flask 后端
const startBackend = () => {
  console.log('正在启动后端服务器...');
  const pythonPath = join(__dirname, 'venv', 'Scripts', 'python.exe');
  const appPath = join(__dirname, 'backend', 'app.py');
  
  console.log('Python路径:', pythonPath);
  console.log('应用路径:', appPath);
  
  const backend = spawn(pythonPath, [appPath], {
    stdio: 'inherit',
    shell: true,
    env: { 
      ...process.env, 
      FLASK_APP: 'app.py',
      FLASK_ENV: 'development',
      PYTHONPATH: join(__dirname, 'backend')
    }
  });

  return new Promise((resolve, reject) => {
    backend.on('error', (err) => {
      console.error('后端启动失败:', err);
      reject(err);
    });

    backend.on('exit', (code) => {
      if (code !== 0) {
        console.error(`后端进程异常退出，退出码: ${code}`);
        reject(new Error(`Backend exited with code ${code}`));
      }
    });

    setTimeout(() => {
      console.log('后端服务器已启动');
      resolve(backend);
    }, 5000);
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
