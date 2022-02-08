from uuid import UUID

from flask import Blueprint, Response, g, jsonify, make_response, request

from flask_jwt_extended import jwt_required

from common.constants.http import HttpStatusCodeConstants
from common.schemas.response import ResponseBaseSchema
from teachers.schemas import TeacherInputSchema, TeacherOutputSchema, TeacherUpdateSchema
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
    STATUS_CODE = HttpStatusCodeConstants.HTTP_200_OK.value
    response = ResponseBaseSchema().load(
        {
            'status': {
                'code': STATUS_CODE,
            },
            'data': teachers,
            'errors': [],
        }
    )
    return make_response(jsonify(response), STATUS_CODE)


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
    STATUS_CODE = HttpStatusCodeConstants.HTTP_200_OK.value
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


@teachers_bp.put('/<uuid:id>')
@jwt_required()
def put_teacher(id: UUID) -> Response:
    """PUT '/teachers/{id}' endpoint view function.

    Args:
        id: UUID of Teacher object.

    Returns:
    http response with json data: single updated Teacher model objects serialized with TeacherOutputSchema.
    """
    teacher = TeacherService(
        session=g.db_session,
        input_schema=TeacherUpdateSchema(many=False),
        output_schema=TeacherOutputSchema(many=False),
    ).update_teacher(id=id, data=request.get_json())
    STATUS_CODE = HttpStatusCodeConstants.HTTP_200_OK.value
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
