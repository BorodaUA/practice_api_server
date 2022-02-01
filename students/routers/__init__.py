from flask import Blueprint, Response, g, jsonify, make_response, request

from common.constants.http import HttpStatusCodeConstants
from students.models import Student
from students.schemas import StudentInputSchema, StudentOutputSchema
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
    return make_response(jsonify(students), HttpStatusCodeConstants.HTTP_200_OK.value)


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
    return make_response(jsonify(student), HttpStatusCodeConstants.HTTP_201_CREATED.value)
