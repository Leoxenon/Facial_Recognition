from flask import request, jsonify
from functools import wraps
import time
from collections import defaultdict

# 简单的内存存储，生产环境应使用 Redis
request_history = defaultdict(list)
RATE_LIMIT = 60  # 每分钟最大请求数
WINDOW_SIZE = 60  # 时间窗口（秒）

def rate_limit(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        ip = request.remote_addr
        now = time.time()
        
        # 清理过期的请求记录
        request_history[ip] = [t for t in request_history[ip] if now - t < WINDOW_SIZE]
        
        if len(request_history[ip]) >= RATE_LIMIT:
            return jsonify({'message': 'Too many requests'}), 429
            
        request_history[ip].append(now)
        return f(*args, **kwargs)
    return decorated 