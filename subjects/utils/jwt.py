from flask import g, request

from subjects.services import SubjectService


def subject_token_verifier(jwt_header: dict, jwt_payload: dict) -> bool:
    """Checks if Subject.course.teacher_id from JWT matches the id from jwt_payload.

    Args:
        jwt_header: JWT headers dict.
        jwt_payload: JWT decoded payload dict.

    Returns:
    bool of comparison Subject.course.teacher_id and decoded jwt data.
    """
    subject = SubjectService(session=g.db_session)._get_subject(column='id', value=str(request.view_args['id']))
    if jwt_payload['sub'] == str(subject.course.teacher_id):
        return True
    return False
