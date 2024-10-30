from flask import Blueprint

bp = Blueprint('user', __name__, url_prefix='/api/user')

@bp.route('/', methods=['GET'])
def get_user():
    return {"message": "User route"}
