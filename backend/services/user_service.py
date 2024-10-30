from werkzeug.security import generate_password_hash
from utils.db import get_table
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def get_user_by_face_id(face_id):
    try:
        table = get_table()
        response = table.get_item(Key={'FaceID': face_id})
        return response.get('Item')
    except Exception as e:
        logger.error(f"Error getting user: {str(e)}")
        return None

def check_user_exists(face_id):
    return get_user_by_face_id(face_id) is not None

def create_user(username, password, face_id, image_url):
    try:
        table = get_table()
        new_user = {
            'FaceID': face_id,
            'username': username,
            'password_hash': generate_password_hash(password),
            'ImageURL': image_url,
            'created_at': str(datetime.now())
        }
        table.put_item(Item=new_user)
        return True
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return False

def update_user_password(face_id, new_password):
    try:
        table = get_table()
        table.update_item(
            Key={'FaceID': face_id},
            UpdateExpression='SET password_hash = :new_hash',
            ExpressionAttributeValues={
                ':new_hash': generate_password_hash(new_password)
            }
        )
        return True
    except Exception as e:
        logger.error(f"Error updating password: {str(e)}")
        return False 