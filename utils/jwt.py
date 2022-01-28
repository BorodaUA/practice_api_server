from flask import request

from auth.routers import auth_bp
from auth.utils.jwt import auth_token_verifier
from users.routers import users_bp
from users.utils.jwt import users_token_verifier

JWT_VERIFIERS = {
    users_bp.name: users_token_verifier,
    auth_bp.name: auth_token_verifier,
}


def generic_token_verifier(jwt_header: dict, jwt_payload: dict) -> bool:
    """Generic JWT token verifier return result of token verification for blueprint's verifier function."""
    return JWT_VERIFIERS[request.blueprint](jwt_header, jwt_payload)
