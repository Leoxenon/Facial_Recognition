import boto3
from config import Config

dynamodb = boto3.resource('dynamodb',
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    region_name=Config.AWS_REGION
)

table = dynamodb.Table(Config.DYNAMODB_TABLE)

def get_table():
    return table
