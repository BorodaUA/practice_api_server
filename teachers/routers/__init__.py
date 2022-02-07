from uuid import UUID

from flask import Blueprint, Response, g, jsonify, make_response, request

from flask_jwt_extended import jwt_required

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


@teachers_bp.get('/<uuid:id>')
def get_teacher(id: UUID) -> Response:
    """GET '/teachers/{id}' endpoint view function.

    Args:
        id: UUID of Teacher object.

    Returns:
    http response with json data: single Teacher model objects serialized with TeacherOutputSchema.
    """
    teacher = TeacherService(
        session=g.db_session,
        output_schema=TeacherOutputSchema(many=False),
    ).get_teacher_by_id(id=id)
    return make_response(jsonify(teacher), HttpStatusCodeConstants.HTTP_200_OK.value)


@teachers_bp.delete('/<uuid:id>')
@jwt_required()
def delete_teacher(id: UUID) -> Response:
    """DELETE '/teachers/{id}' endpoint view function.

    Args:
        id: UUID of Teacher object.

    Returns:
    http response with no data and 204 status code.
    """
    TeacherService(session=g.db_session).delete_teacher(id=id)
    return make_response('', HttpStatusCodeConstants.HTTP_204_NO_CONTENT.value)
