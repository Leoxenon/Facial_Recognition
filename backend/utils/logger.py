import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger():
    logger = logging.getLogger('facial_auth')
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 文件处理器
    file_handler = RotatingFileHandler(
        'logs/app.log', 
        maxBytes=1024 * 1024,
        backupCount=10
    )
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    return logger
