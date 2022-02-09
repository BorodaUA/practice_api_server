from flask import g, request

from courses.services import CourseService


def course_token_verifier(jwt_header: dict, jwt_payload: dict) -> bool:
    """Checks if Course.teacher_id from JWT matches the id from jwt_payload.

    Args:
        jwt_header: JWT headers dict.
        jwt_payload: JWT decoded payload dict.

    Returns:
    bool of comparison Course.teacher_id and decoded jwt data.
    """
    course = CourseService(session=g.db_session)._get_course(column='id', value=str(request.view_args['id']))
    if jwt_payload['sub'] == str(course.teacher_id):
        return True
    return False
