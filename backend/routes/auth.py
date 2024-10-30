from flask import Blueprint, request, jsonify
from services import auth_service
from middleware.validators import validate_auth_request
from middleware.error_handler import handle_errors
from middleware.rate_limit import rate_limit

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
@validate_auth_request
@handle_errors
@rate_limit
def register():
    data = request.json
    result = auth_service.register_user(
        data['username'], 
        data['password'], 
        data['faceImage']
    )
    return jsonify(result)

@bp.route('/login', methods=['POST'])
@validate_auth_request
@handle_errors
@rate_limit
def login():
    data = request.json
    result = auth_service.authenticate_user(
        data['username'],
        data['password'],
        data['faceImage']
    )
    return jsonify(result)

@bp.route('/recover-password', methods=['POST'])
@validate_auth_request
@handle_errors
@rate_limit
def recover_password():
    data = request.json
    result = auth_service.recover_password(
        data['username'],
        data['faceImage'],
        data['newPassword']
    )
    return jsonify(result)

@bp.route('/refresh-token', methods=['POST'])
@handle_errors
@rate_limit
def refresh_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'success': False, 'message': 'Missing token'}), 401
    
    token = auth_header.split(' ')[1]
    new_token = auth_service.refresh_session_token(token)
    
    if not new_token:
        return jsonify({'success': False, 'message': 'Invalid token'}), 401
        
    return jsonify({
        'success': True,
        'token': new_token
    })
