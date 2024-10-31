from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from utils.db import get_table
from services import rekognition_service
from utils.s3 import upload_image_to_s3
import logging
import base64
import uuid
from services.face_utils import validate_face_image, verify_face_identity
from exceptions.auth_exceptions import AuthenticationError, FaceRecognitionError
from services.session_service import create_session_token, refresh_token as refresh_session_token
from services.user_service import get_user_by_face_id, check_user_exists, create_user, update_user_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_user(username, password, face_image):
    try:
        table = get_table()
        
        # 验证人脸图像
        image_data, face_info = validate_face_image(face_image)
        if not image_data:
            raise FaceRecognitionError(face_info)
            
        # 上传图像到 S3
        image_url = upload_image_to_s3(image_data)
        face_id = rekognition_service.index_face(image_url)
        
        if not face_id:
            raise FaceRecognitionError('Face recognition failed')
            
        # 检查用户是否已存在
        if check_user_exists(face_id):
            raise AuthenticationError('Face already registered')
            
        # 创建新用户
        create_user(username, password, face_id, image_url)
        
        return {'success': True, 'message': 'Registration successful'}
    except (AuthenticationError, FaceRecognitionError) as e:
        logger.error(f"Registration error: {str(e)}")
        return {'success': False, 'message': str(e)}

def authenticate_user(username, password, face_image):
    try:
        face_id, _ = verify_face_identity(face_image, username)
        user = get_user_by_face_id(face_id)
        
        if not check_password_hash(user['password_hash'], password):
            raise AuthenticationError('Incorrect password')

        token = create_session_token(face_id)
        return {
            'success': True, 
            'message': 'Login successful',
            'face_verified': True,
            'token': token
        }
    except (AuthenticationError, FaceRecognitionError) as e:
        logger.error(f"Authentication error: {str(e)}")
        return {'success': False, 'message': str(e)}

def recover_password(username, face_image, new_password):
    try:
        face_id, _ = verify_face_identity(face_image, username)
        
        # 验证新密码强度
        password_error = validate_password(new_password)
        if password_error:
            raise AuthenticationError(password_error)

        update_user_password(face_id, new_password)
        return {'success': True, 'message': 'Password reset successful'}
    except (AuthenticationError, FaceRecognitionError) as e:
        logger.error(f"Password recovery error: {str(e)}")
        return {'success': False, 'message': str(e)}

def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long"
    if not any(c.isupper() for c in password):
        return "Password must contain at least one uppercase letter"
    if not any(c.islower() for c in password):
        return "Password must contain at least one lowercase letter"
    if not any(c.isdigit() for c in password):
        return "Password must contain at least one number"
    return None
