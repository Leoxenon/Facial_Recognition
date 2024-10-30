import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION')
    S3_BUCKET = os.getenv('S3_BUCKET')
    COLLECTION_ID = os.getenv('COLLECTION_ID')
    DYNAMODB_TABLE = os.getenv('DYNAMODB_TABLE')
    
    FACE_MATCH_THRESHOLD = 95.0
    MAX_FACES = 1
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
