from functools import wraps
from flask import request, jsonify
from services.session_service import verify_session_token

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({
                'success': False,
                'message': 'No authorization token provided'
            }), 401
            
        try:
            token = auth_header.split(' ')[1]
            user_id = verify_session_token(token)
            
            if not user_id:
                return jsonify({
                    'success': False,
                    'message': 'Invalid or expired token'
                }), 401
                
            request.user_id = user_id
            return f(*args, **kwargs)
        except Exception:
            return jsonify({
                'success': False,
                'message': 'Invalid token format'
            }), 401
            
    return decorated 