from functools import wraps
from flask import request, jsonify

def validate_auth_request(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        required_fields = ['username', 'password', 'faceImage']
        
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
            
        return f(*args, **kwargs)
    return wrapper
