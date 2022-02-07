from flask import request


def teachers_token_verifier(jwt_header: dict, jwt_payload: dict) -> bool:
    """Checks if Teacher.id from JWT matches the id from request view args.

    Args:
        jwt_header: JWT headers dict.
        jwt_payload: JWT decoded payload dict.

    Returns:
    bool of comparison request view args and decoded jwt data.
    """
    if jwt_payload['sub'] == str(request.view_args['id']):
        return True
    return False
