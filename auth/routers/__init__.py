from flask import Blueprint, Response, g, jsonify, make_response, request

from flask_jwt_extended import jwt_required

from auth.schemas import AuthUserInputSchema, AuthUserLogoutSchema, AuthUserOutputSchema
from auth.services import AuthService
from common.constants.http import HttpStatusCodeConstants
from users.schemas import UserOutputSchema

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.post('/login')
def login() -> Response:
    """POST '/login' endpoint view function."""
    response = AuthService(
        session=g.db_session,
        input_schema=AuthUserInputSchema(many=False),
        output_schema=AuthUserOutputSchema(many=False),
    ).login(request.get_json())
    return response, HttpStatusCodeConstants.HTTP_200_OK.value


@auth_bp.get('/me')
@jwt_required()
def me() -> Response:
    """GET '/me' endpoint view function."""
    user = AuthService(session=g.db_session, output_schema=UserOutputSchema(many=False)).me()
    return make_response(jsonify(user), HttpStatusCodeConstants.HTTP_200_OK.value)


@auth_bp.post('/logout')
@jwt_required()
def logout() -> Response:
    """POST '/logout' endpoint view function."""
    response = AuthService(session=g.db_session, output_schema=AuthUserLogoutSchema(many=False)).logout()
    return response, HttpStatusCodeConstants.HTTP_200_OK.value
