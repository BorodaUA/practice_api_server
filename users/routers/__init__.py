from uuid import UUID

from flask import Blueprint, Response, g, jsonify, make_response, request

from common.constants.http import HttpStatusCodeConstants
from users.services import UserService

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.get('/')
def get_users() -> Response:
    """GET '/users' endpoint view function."""
    users = UserService(session=g.db_session, method=request.method).get_users()
    return make_response(jsonify(users))


@users_bp.post('/')
def post_users() -> Response:
    """POST '/users' endpoint view function."""
    user = UserService(session=g.db_session, method=request.method).add_user(user=request.get_json())
    return make_response(jsonify(user), HttpStatusCodeConstants.HTTP_201_CREATED.value)


@users_bp.delete('/<uuid:id>')
def delete_user(id: UUID) -> Response:
    """DELETE '/users/{id}' endpoint view function."""
    UserService(session=g.db_session, method=request.method).delete_user(id)
    return make_response('', HttpStatusCodeConstants.HTTP_204_NO_CONTENT.value)


@users_bp.get('/<uuid:id>')
def get_user(id: UUID) -> Response:
    """GET '/users/{id}' endpoint view function."""
    user = UserService(session=g.db_session, method=request.method).get_user_by_id(id=id)
    return make_response(jsonify(user), HttpStatusCodeConstants.HTTP_200_OK.value)


@users_bp.put('/<uuid:id>')
def put_user(id: UUID) -> Response:
    """PUT '/users/{id}' endpoint view function."""
    user = UserService(session=g.db_session, method=request.method).update_user(id=id, user=request.get_json())
    return make_response(jsonify(user), HttpStatusCodeConstants.HTTP_200_OK.value)
