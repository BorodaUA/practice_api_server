from uuid import UUID

from flask import Blueprint, g, jsonify, make_response, request

from common.constants.http import HttpStatusCodeConstants
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
    return make_response(jsonify(user), HttpStatusCodeConstants.HTTP_201_CREATED.value)


@users_bp.delete('/<uuid:id>')
def delete_user(id: UUID):
    """DELETE '/users/{id}' endpoint view function."""
    UserService(session=g.db_session).delete_user(id)
    return make_response('', HttpStatusCodeConstants.HTTP_204_NO_CONTENT.value)
