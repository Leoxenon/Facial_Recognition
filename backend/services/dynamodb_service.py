import boto3
from botocore.exceptions import ClientError
from config import Config
import os
from botocore.config import Config as BotoConfig
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

boto3.set_stream_logger('botocore', logging.DEBUG)

class DynamoDBService:
    def __init__(self):
        logger.debug(f"AWS_ACCESS_KEY_ID: {os.getenv('AWS_ACCESS_KEY_ID')[:5]}...")
        logger.debug(f"AWS_SECRET_ACCESS_KEY: {os.getenv('AWS_SECRET_ACCESS_KEY')[:5]}...")
        logger.debug(f"AWS_REGION: {os.getenv('AWS_REGION')}")
        self.dynamodb = boto3.resource('dynamodb', 
                                       aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                       aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                                       region_name=os.getenv('AWS_REGION'),
                                       config=BotoConfig(signature_version='v4')
                                       )
        self.table = self.dynamodb.Table(Config.DYNAMODB_TABLE)

    def add_entry(self, item):
        try:
            response = self.table.put_item(Item=item)
            return response
        except ClientError as e:
            print(f"Error adding entry to DynamoDB: {e}")
            raise

    def get_entry(self, key):
        try:
            response = self.table.get_item(Key=key)
            return response.get('Item')
        except ClientError as e:
            print(f"Error getting entry from DynamoDB: {e}")
            raise

    def update_entry(self, key, update_expression, expression_values):
        try:
            response = self.table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ReturnValues="ALL_NEW"
            )
            return response.get('Attributes')
        except ClientError as e:
            print(f"Error updating entry in DynamoDB: {e}")
            raise

    def create_table_if_not_exists(self):
        try:
            self.dynamodb.create_table(
                TableName=Config.DYNAMODB_TABLE,
                KeySchema=[
                    {
                        'AttributeName': 'FaceID',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'FaceID',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            print(f"Table {Config.DYNAMODB_TABLE} created successfully.")
        except self.dynamodb.meta.client.exceptions.ResourceInUseException:
            print(f"Table {Config.DYNAMODB_TABLE} already exists.")
