from uuid import UUID

from flask import Blueprint, Response, g, jsonify, make_response, request

from common.constants.http import HttpStatusCodeConstants
from common.schemas.response import ResponseBaseSchema
from courses.schemas import CourseInputSchema, CourseOutputSchema
from courses.services import CourseService

courses_bp = Blueprint('courses', __name__, url_prefix='/courses')


@courses_bp.get('/')
def get_courses() -> Response:
    """GET '/courses' endpoint view function.

    Returns:
    http response with json data: list of Course model objects serialized with CourseOutputSchema.
    """
    courses = CourseService(
        session=g.db_session,
        output_schema=CourseOutputSchema(many=True),
    ).get_courses()
    STATUS_CODE = HttpStatusCodeConstants.HTTP_200_OK.value
    response = ResponseBaseSchema().load(
        {
            'status': {
                'code': STATUS_CODE,
            },
            'data': courses,
            'errors': [],
        }
    )
    return make_response(jsonify(response), STATUS_CODE)


@courses_bp.post('/')
def post_courses() -> Response:
    """POST '/courses' endpoint view function.

    Returns:
    http response with json data: newly created Course model object serialized with CourseOutputSchema.
    """
    teacher = CourseService(
        session=g.db_session,
        input_schema=CourseInputSchema(many=False),
        output_schema=CourseOutputSchema(many=False),
    ).add_course(data=request.get_json())
    STATUS_CODE = HttpStatusCodeConstants.HTTP_201_CREATED.value
    response = ResponseBaseSchema().load(
        {
            'status': {
                'code': STATUS_CODE,
            },
            'data': teacher,
            'errors': [],
        }
    )
    return make_response(jsonify(response), STATUS_CODE)


@courses_bp.get('/<uuid:id>')
def get_course(id: UUID) -> Response:
    """GET '/courses/{id}' endpoint view function.

    Args:
        id: UUID of Course object.

    Returns:
    http response with json data: single Course model objects serialized with CourseOutputSchema.
    """
    course = CourseService(
        session=g.db_session,
        output_schema=CourseOutputSchema(many=False),
    ).get_course_by_id(id=id)
    STATUS_CODE = HttpStatusCodeConstants.HTTP_200_OK.value
    response = ResponseBaseSchema().load(
        {
            'status': {
                'code': STATUS_CODE,
            },
            'data': course,
            'errors': [],
        }
    )
    return make_response(jsonify(response), STATUS_CODE)
