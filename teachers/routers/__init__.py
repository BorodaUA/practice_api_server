from flask import Blueprint, Response, g, jsonify, make_response, request

from common.constants.http import HttpStatusCodeConstants
from teachers.schemas import TeacherInputSchema, TeacherOutputSchema
from teachers.services import TeacherService

teachers_bp = Blueprint('teachers', __name__, url_prefix='/teachers')


@teachers_bp.get('/')
def get_teachers() -> Response:
    """GET '/teachers' endpoint view function.

    Returns:
    http response with json data: list of Teacher model objects serialized with TeacherOutputSchema.
    """
    teachers = TeacherService(
        session=g.db_session,
        output_schema=TeacherOutputSchema(many=True),
    ).get_teachers()
    return make_response(jsonify(teachers), HttpStatusCodeConstants.HTTP_200_OK.value)


@teachers_bp.post('/')
def post_teachers() -> Response:
    """POST '/teachers' endpoint view function.

    Returns:
    http response with json data: newly created Teacher model object serialized with TeacherOutputSchema.
    """
    teacher = TeacherService(
        session=g.db_session,
        input_schema=TeacherInputSchema(many=False),
        output_schema=TeacherOutputSchema(many=False),
    ).add_teacher(data=request.get_json())
    return make_response(jsonify(teacher), HttpStatusCodeConstants.HTTP_201_CREATED.value)
