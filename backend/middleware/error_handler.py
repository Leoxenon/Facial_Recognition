from flask import jsonify
from functools import wraps
from exceptions.auth_exceptions import AuthenticationError, FaceRecognitionError

def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except AuthenticationError as e:
            return jsonify({
                'success': False,
                'message': str(e),
                'error_type': 'AuthenticationError'
            }), 401
        except FaceRecognitionError as e:
            return jsonify({
                'success': False,
                'message': str(e),
                'error_type': 'FaceRecognitionError'
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Internal server error',
                'error_type': 'ServerError'
            }), 500
    return wrapper
