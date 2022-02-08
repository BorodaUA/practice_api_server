from uuid import UUID

from flask import Blueprint, Response, g, jsonify, make_response, request

from flask_jwt_extended import jwt_required

from common.constants.http import HttpStatusCodeConstants
from common.schemas.response import ResponseBaseSchema
from users.schemas import UserInputSchema, UserOutputSchema, UserUpdateSchema
from users.services import UserService

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.get('/')
def get_users() -> Response:
    """GET '/users' endpoint view function."""
    users = UserService(
        session=g.db_session,
        output_schema=UserOutputSchema(many=True),
    ).get_users()
    STATUS_CODE = HttpStatusCodeConstants.HTTP_200_OK.value
    response = ResponseBaseSchema().load(
        {
            'status': {
                'code': STATUS_CODE,
            },
            'data': users,
            'errors': [],
        }
    )
    return make_response(jsonify(response), STATUS_CODE)


@users_bp.post('/')
def post_users() -> Response:
    """POST '/users' endpoint view function."""
    user = UserService(
        session=g.db_session,
        input_schema=UserInputSchema(many=False),
        output_schema=UserOutputSchema(many=False),
    ).add_user(user=request.get_json())
    STATUS_CODE = HttpStatusCodeConstants.HTTP_201_CREATED.value
    response = ResponseBaseSchema().load(
        {
            'status': {
                'code': STATUS_CODE,
            },
            'data': user,
            'errors': [],
        }
    )
    return make_response(jsonify(response), STATUS_CODE)


@users_bp.delete('/<uuid:id>')
@jwt_required()
def delete_user(id: UUID) -> Response:
    """DELETE '/users/{id}' endpoint view function."""
    UserService(session=g.db_session).delete_user(id=id)
    return make_response('', HttpStatusCodeConstants.HTTP_204_NO_CONTENT.value)


@users_bp.get('/<uuid:id>')
def get_user(id: UUID) -> Response:
    """GET '/users/{id}' endpoint view function."""
    user = UserService(
        session=g.db_session,
        output_schema=UserOutputSchema(many=False),
    ).get_user_by_id(id=id)
    STATUS_CODE = HttpStatusCodeConstants.HTTP_200_OK.value
    response = ResponseBaseSchema().load(
        {
            'status': {
                'code': STATUS_CODE,
            },
            'data': user,
            'errors': [],
        }
    )
    return make_response(jsonify(response), STATUS_CODE)


@users_bp.put('/<uuid:id>')
@jwt_required()
def put_user(id: UUID) -> Response:
    """PUT '/users/{id}' endpoint view function."""
    user = UserService(
        session=g.db_session,
        input_schema=UserUpdateSchema(many=False),
        output_schema=UserOutputSchema(many=False),
    ).update_user(id=id, user=request.get_json())
    STATUS_CODE = HttpStatusCodeConstants.HTTP_200_OK.value
    response = ResponseBaseSchema().load(
        {
            'status': {
                'code': STATUS_CODE,
            },
            'data': user,
            'errors': [],
        }
    )
    return make_response(jsonify(response), STATUS_CODE)
