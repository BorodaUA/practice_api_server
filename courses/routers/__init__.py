from uuid import UUID

from flask import Blueprint, Response, g, jsonify, make_response, request

from flask_jwt_extended import jwt_required

from common.constants.http import HttpStatusCodeConstants
from common.schemas.response import ResponseBaseSchema
from courses.schemas import CourseInputSchema, CourseOutputSchema, CourseUpdateSchema
from courses.services import CourseService
from students.schemas import StudentBaseSchema, StudentOutputSchema

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
    course = CourseService(
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
            'data': course,
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


@courses_bp.put('/<uuid:id>')
@jwt_required()
def put_course(id: UUID) -> Response:
    """PUT '/courses/{id}' endpoint view function.

    Args:
        id: UUID of Course object.

    Returns:
    http response with json data: single updated Course model objects serialized with CourseOutputSchema.
    """
    course = CourseService(
        session=g.db_session,
        input_schema=CourseUpdateSchema(many=False),
        output_schema=CourseOutputSchema(many=False),
    ).update_course(id=id, data=request.get_json())
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


@courses_bp.delete('/<uuid:id>')
@jwt_required()
def delete_course(id: UUID) -> Response:
    """DELETE '/courses/{id}' endpoint view function.

    Args:
        id: UUID of Course object.

    Returns:
    http response with no data and 204 status code.
    """
    CourseService(session=g.db_session).delete_course(id=id)
    return make_response('', HttpStatusCodeConstants.HTTP_204_NO_CONTENT.value)


@courses_bp.get('/<uuid:id>/students')
def get_course_students(id: UUID) -> Response:
    """GET '/courses/{id}/students' endpoint view function.

    Returns:
    http response with json data: list of Course model Student objects serialized with StudentOutputSchema.
    """
    course_students = CourseService(
        session=g.db_session,
        output_schema=StudentOutputSchema(many=True),
    ).get_course_students(id)
    STATUS_CODE = HttpStatusCodeConstants.HTTP_200_OK.value
    response = ResponseBaseSchema().load(
        {
            'status': {
                'code': STATUS_CODE,
            },
            'data': course_students,
            'errors': [],
        }
    )
    return make_response(jsonify(response), STATUS_CODE)


@courses_bp.post('/<uuid:id>/students')
def post_course_students(id: UUID) -> Response:
    """POST '/courses/{id}/students' endpoint view function.

    Returns:
    http response with json data: Course model Student object serialized with StudentOutputSchema.
    """
    course_student = CourseService(
        session=g.db_session,
        input_schema=StudentBaseSchema(many=False),
        output_schema=StudentOutputSchema(many=False),
    ).add_course_student(id=id, data=request.get_json())
    STATUS_CODE = HttpStatusCodeConstants.HTTP_201_CREATED.value
    response = ResponseBaseSchema().load(
        {
            'status': {
                'code': STATUS_CODE,
            },
            'data': course_student,
            'errors': [],
        }
    )
    return make_response(jsonify(response), STATUS_CODE)


@courses_bp.get('/<uuid:id>/students/<uuid:student_id>')
def get_course_student(id: UUID, student_id: UUID) -> Response:
    """GET '/courses/{id}/students/{id}' endpoint view function.

    Returns:
    http response with json data: Course model Student object serialized with StudentOutputSchema.
    """
    course_student = CourseService(
        session=g.db_session,
        output_schema=StudentOutputSchema(many=False),
    ).get_course_student_by_id(id, student_id)
    STATUS_CODE = HttpStatusCodeConstants.HTTP_200_OK.value
    response = ResponseBaseSchema().load(
        {
            'status': {
                'code': STATUS_CODE,
            },
            'data': course_student,
            'errors': [],
        }
    )
    return make_response(jsonify(response), STATUS_CODE)
