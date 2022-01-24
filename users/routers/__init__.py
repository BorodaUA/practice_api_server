from flask import Blueprint, g, jsonify, make_response, request

from users.services import UserService

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.get('/')
def get_users():
    """GET '/users' endpoint view function."""
    users = UserService(session=g.db_session).get_users()
    return make_response(jsonify(users))


@users_bp.post('/')
def post_users():
    """POST '/users' endpoint view function."""
    user = UserService(session=g.db_session).add_user(request.get_json())
    return make_response(jsonify(user))
