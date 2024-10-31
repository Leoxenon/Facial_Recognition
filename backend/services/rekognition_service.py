import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError
import logging
from config import Config

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 验证环境变量
required_env_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]

if missing_vars:
    raise Exception(f"Missing required environment variables: {', '.join(missing_vars)}")

logger.info(f"Using AWS region: {os.getenv('AWS_REGION')}")

rekognition_client = boto3.client('rekognition',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

# 测试连接
try:
    rekognition_client.describe_collection(CollectionId='test')
    logger.info("Successfully connected to AWS Rekognition")
except ClientError as e:
    if e.response['Error']['Code'] == 'ResourceNotFoundException':
        logger.info("Test collection not found, but connection successful")
    else:
        logger.error(f"Failed to connect to AWS Rekognition: {str(e)}")
        raise e

def index_face(image_url):
    try:
        response = rekognition_client.index_faces(
            CollectionId=Config.COLLECTION_ID,
            Image={'S3Object': {'Bucket': Config.S3_BUCKET, 'Name': image_url}},
            MaxFaces=1,
            QualityFilter="AUTO",
            DetectionAttributes=['ALL']
        )
        if response['FaceRecords']:
            return response['FaceRecords'][0]['Face']['FaceId']
        return None
    except ClientError as e:
        print(f"Error indexing face: {e}")
        return None

def verify_face(image_bytes, face_id):
    try:
        response = rekognition_client.search_faces_by_image(
            CollectionId=Config.COLLECTION_ID,
            Image={'Bytes': image_bytes},
            MaxFaces=1,
            FaceMatchThreshold=95
        )
        if response['FaceMatches'] and response['FaceMatches'][0]['Face']['FaceId'] == face_id:
            return True
        return False
    except ClientError as e:
        print(f"Error verifying face: {e}")
        return False

def create_collection(collection_id=Config.COLLECTION_ID):
    try:
        rekognition_client.create_collection(CollectionId=collection_id)
        print(f"Collection {collection_id} created.")
    except rekognition_client.exceptions.ResourceAlreadyExistsException:
        print(f"Collection {collection_id} already exists.")
    except ClientError as e:
        print(f"Error creating collection: {e}")

def detect_faces(image_bytes):
    try:
        response = rekognition_client.detect_faces(
            Image={'Bytes': image_bytes},
            Attributes=['ALL']
        )
        return response['FaceDetails']
    except ClientError as e:
        print(f"Error detecting faces: {e}")
        return None

def compare_faces(source_image, target_image):
    response = rekognition_client.compare_faces(
        SourceImage={'Bytes': source_image},
        TargetImage={'Bytes': target_image},
        SimilarityThreshold=80
    )
    return response['FaceMatches']
