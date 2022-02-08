from uuid import UUID

from flask import Blueprint, Response, g, jsonify, make_response, request

from flask_jwt_extended import jwt_required

from common.constants.http import HttpStatusCodeConstants
from common.schemas.response import ResponseBaseSchema
from students.schemas import StudentInputSchema, StudentOutputSchema, StudentUpdateSchema
from students.services import StudentService

students_bp = Blueprint('students', __name__, url_prefix='/students')


@students_bp.get('/')
def get_students():
    """GET '/students' endpoint view function.

    Returns:
    http response with json data: list of Student model objects serialized with StudentOutputSchema.
    """
    students = StudentService(
        session=g.db_session,
        output_schema=StudentOutputSchema(many=True),
    ).get_students()
    STATUS_CODE = HttpStatusCodeConstants.HTTP_200_OK.value
    response = ResponseBaseSchema().load(
        {
            'status': {
                'code': STATUS_CODE,
            },
            'data': students,
            'errors': [],
        }
    )
    return make_response(jsonify(response), STATUS_CODE)


@students_bp.post('/')
def post_students() -> Response:
    """POST '/students' endpoint view function.

    Returns:
    http response with json data: newly created Student model object serialized with StudentOutputSchema.
    """
    student = StudentService(
        session=g.db_session,
        input_schema=StudentInputSchema(many=False),
        output_schema=StudentOutputSchema(many=False),
    ).add_student(request.get_json())
    STATUS_CODE = HttpStatusCodeConstants.HTTP_201_CREATED.value
    response = ResponseBaseSchema().load(
        {
            'status': {
                'code': STATUS_CODE,
            },
            'data': student,
            'errors': [],
        }
    )
    return make_response(jsonify(response), STATUS_CODE)


@students_bp.get('/<uuid:id>')
def get_student(id: UUID) -> Response:
    """GET '/students/{id}' endpoint view function.

    Args:
        id: UUID of Student object.

    Returns:
    http response with json data: single Student model objects serialized with StudentOutputSchema.
    """
    student = StudentService(
        session=g.db_session,
        output_schema=StudentOutputSchema(many=False),
    ).get_student_by_id(id=id)
    STATUS_CODE = HttpStatusCodeConstants.HTTP_200_OK.value
    response = ResponseBaseSchema().load(
        {
            'status': {
                'code': STATUS_CODE,
            },
            'data': student,
            'errors': [],
        }
    )
    return make_response(jsonify(response), STATUS_CODE)


@students_bp.delete('/<uuid:id>')
@jwt_required()
def delete_student(id: UUID) -> Response:
    """DELETE '/students/{id}' endpoint view function.

    Args:
        id: UUID of Student object.

    Returns:
    http response with no data and 204 status code.
    """
    StudentService(session=g.db_session).delete_student(id=id)
    return make_response('', HttpStatusCodeConstants.HTTP_204_NO_CONTENT.value)


@students_bp.put('/<uuid:id>')
@jwt_required()
def put_student(id: UUID) -> Response:
    """PUT '/students/{id}' endpoint view function.

    Args:
        id: UUID of Student object.

    Returns:
    http response with json data: single updated Student model objects serialized with StudentOutputSchema.
    """
    student = StudentService(
        session=g.db_session,
        input_schema=StudentUpdateSchema(many=False),
        output_schema=StudentOutputSchema(many=False),
    ).update_student(id=id, data=request.get_json())
    STATUS_CODE = HttpStatusCodeConstants.HTTP_200_OK.value
    response = ResponseBaseSchema().load(
        {
            'status': {
                'code': STATUS_CODE,
            },
            'data': student,
            'errors': [],
        }
    )
    return make_response(jsonify(response), STATUS_CODE)
