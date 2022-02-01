def auth_token_verifier(jwt_header: dict, jwt_payload: dict) -> bool:
    """Return bool of jwt_payload presence."""
    if jwt_payload:
        return True
    return False
