from services import rekognition_service
import base64
from services.user_service import get_user_by_face_id
from exceptions.auth_exceptions import AuthenticationError, FaceRecognitionError

def validate_face_image(face_image):
    try:
        # 解码 base64 图像
        image_data = base64.b64decode(face_image.split(',')[1])
        
        # 检测人脸
        faces = rekognition_service.detect_faces(image_data)
        if not faces or len(faces) != 1:
            return None, 'Image must contain one clear face'
            
        return image_data, faces[0]
    except Exception as e:
        return None, str(e)

def verify_face_identity(face_image, username=None):
    try:
        # 验证人脸图像
        image_data, face_info = validate_face_image(face_image)
        if not image_data:
            raise FaceRecognitionError(face_info)
            
        # 验证面部图像并获取 face_id
        face_matches = rekognition_service.search_faces_by_image(image_data)
        if not face_matches:
            raise FaceRecognitionError('Face not recognized')

        face_id = face_matches[0]['Face']['FaceId']
        
        # 如果提供了用户名，验证用户名匹配
        if username:
            user = get_user_by_face_id(face_id)
            if not user:
                raise AuthenticationError('User not found')
            if user['username'] != username:
                raise AuthenticationError('Username does not match face')
                
        return face_id, image_data
    except Exception as e:
        raise FaceRecognitionError(str(e))
