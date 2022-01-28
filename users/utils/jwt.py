from flask import request


def users_token_verifier(jwt_header: dict, jwt_payload: dict) -> bool:
    """Checks if User.id from JWT matches id from request view args."""
    if jwt_payload['sub'] == str(request.view_args['id']):
        return True
    return False
