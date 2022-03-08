from uuid import UUID

from flask import Blueprint, Response, g, jsonify, make_response, request

from flask_jwt_extended import jwt_required

from common.constants.http import HttpStatusCodeConstants
from common.schemas.response import ResponseBaseSchema
from subjects.schemas import SubjectInputSchema, SubjectOutputSchema, SubjectUpdateSchema
from subjects.services import SubjectService

subjects_bp = Blueprint('subjects', __name__, url_prefix='/subjects')


@subjects_bp.get('/')
def get_subjects() -> Response:
    """GET '/subjects' endpoint view function.

    Returns:
    http response with json data: list of Subject model objects serialized with SubjectOutputSchema.
    """
    subjects = SubjectService(
        session=g.db_session,
        output_schema=SubjectOutputSchema(many=True),
    ).get_subjects()
    STATUS_CODE = HttpStatusCodeConstants.HTTP_200_OK.value
    response = ResponseBaseSchema().load(
        {
            'status': {
                'code': STATUS_CODE,
            },
            'data': subjects,
            'errors': [],
        }
    )
    return make_response(jsonify(response), STATUS_CODE)


@subjects_bp.post('/')
def post_subject() -> Response:
    """POST '/subjects' endpoint view function.

    Returns:
    http response with json data: newly created Subject model object serialized with SubjectOutputSchema.
    """
    subject = SubjectService(
        session=g.db_session,
        input_schema=SubjectInputSchema(many=False),
        output_schema=SubjectOutputSchema(many=False),
    ).add_subject(data=request.get_json())
    STATUS_CODE = HttpStatusCodeConstants.HTTP_201_CREATED.value
    response = ResponseBaseSchema().load(
        {
            'status': {
                'code': STATUS_CODE,
            },
            'data': subject,
            'errors': [],
        }
    )
    return make_response(jsonify(response), STATUS_CODE)


@subjects_bp.get('/<uuid:id>')
def get_subject(id: UUID) -> Response:
    """GET '/subjects/{id}' endpoint view function.

    Args:
        id: UUID of Subject object.

    Returns:
    http response with json data: single Subject model objects serialized with SubjectOutputSchema.
    """
    subject = SubjectService(
        session=g.db_session,
        output_schema=SubjectOutputSchema(many=False),
    ).get_subject_by_id(id=id)
    STATUS_CODE = HttpStatusCodeConstants.HTTP_200_OK.value
    response = ResponseBaseSchema().load(
        {
            'status': {
                'code': STATUS_CODE,
            },
            'data': subject,
            'errors': [],
        }
    )
    return make_response(jsonify(response), STATUS_CODE)


@subjects_bp.put('/<uuid:id>')
@jwt_required()
def put_subject(id: UUID) -> Response:
    """PUT '/subjects/{id}' endpoint view function.

    Args:
        id: UUID of Subject object.

    Returns:
    http response with json data: single updated Subject model object serialized with SubjectOutputSchema.
    """
    subject = SubjectService(
        session=g.db_session,
        input_schema=SubjectUpdateSchema(many=False),
        output_schema=SubjectOutputSchema(many=False),
    ).update_subject(id=id, data=request.get_json())
    STATUS_CODE = HttpStatusCodeConstants.HTTP_200_OK.value
    response = ResponseBaseSchema().load(
        {
            'status': {
                'code': STATUS_CODE,
            },
            'data': subject,
            'errors': [],
        }
    )
    return make_response(jsonify(response), STATUS_CODE)


@subjects_bp.delete('/<uuid:id>')
@jwt_required()
def delete_subject(id: UUID) -> Response:
    """DELETE '/subjects/{id}' endpoint view function.

    Args:
        id: UUID of Subject object.

    Returns:
    http response with no data and 204 status code.
    """
    SubjectService(session=g.db_session).delete_subject(id=id)
    return make_response('', HttpStatusCodeConstants.HTTP_204_NO_CONTENT.value)
