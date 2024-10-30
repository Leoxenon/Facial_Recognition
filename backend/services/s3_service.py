import boto3
from botocore.exceptions import ClientError
from config import settings
import uuid

class S3Service:
    def __init__(self):
        self.s3 = boto3.client('s3', 
                               aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                               aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                               region_name=settings.AWS_REGION)

    def upload_file(self, file_obj, object_name):
        try:
            self.s3.upload_fileobj(file_obj, settings.S3_BUCKET, object_name)
            return f"https://{settings.S3_BUCKET}.s3.amazonaws.com/{object_name}"
        except ClientError as e:
            print(f"Error uploading file to S3: {e}")
            raise

    def download_file(self, object_name, file_name):
        try:
            self.s3.download_file(settings.S3_BUCKET, object_name, file_name)
        except ClientError as e:
            print(f"Error downloading file from S3: {e}")
            raise

def upload_image_to_s3(image_data):
    filename = f"{uuid.uuid4()}.jpg"
    s3_client = boto3.client('s3', 
                             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                             region_name=settings.AWS_REGION)
    s3_client.put_object(Bucket=settings.S3_BUCKET, 
                         Key=filename, 
                         Body=image_data, 
                         ContentType='image/jpeg')
    return filename
