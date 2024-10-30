import boto3
from config import settings

dynamodb = boto3.resource('dynamodb',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

table = dynamodb.Table(settings.DYNAMODB_TABLE)

def get_table():
    return table
