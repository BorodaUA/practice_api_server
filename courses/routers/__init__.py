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
def post_teachers() -> Response:
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
