from datetime import datetime, timedelta
import jwt
from config import Config

def create_session_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

def verify_session_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def refresh_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        if datetime.fromtimestamp(payload['exp']) - datetime.utcnow() < timedelta(hours=1):
            return create_session_token(payload['user_id'])
        return token
    except:
        return None 