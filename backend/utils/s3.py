import boto3
from config import settings
import uuid

s3_client = boto3.client('s3', 
                         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                         region_name=settings.AWS_REGION)

def upload_image_to_s3(image_data):
    filename = f"{uuid.uuid4()}.jpg"
    s3_client.put_object(Bucket=Config.S3_BUCKET, 
                         Key=filename, 
                         Body=image_data, 
                         ContentType='image/jpeg')
    return filename

