import boto3
from config import Config
import uuid
import logging

logger = logging.getLogger(__name__)

s3_client = boto3.client('s3', 
                         aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
                         region_name=Config.AWS_REGION)

def upload_image_to_s3(image_data):
    try:
        filename = f"{uuid.uuid4()}.jpg"
        s3_client.put_object(
            Bucket=Config.S3_BUCKET, 
            Key=filename, 
            Body=image_data, 
            ContentType='image/jpeg'
        )
        return filename
    except Exception as e:
        logger.error(f"Failed to upload image to S3: {str(e)}")
        raise

