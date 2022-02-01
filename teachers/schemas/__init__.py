from marshmallow import Schema, fields, validate

from common.constants.schemas import TeacherSchemaConstants


class TeacherBaseSchema(Schema):
    """Teacher Base schema for Teacher model."""

    id = fields.UUID()
    qualification = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=TeacherSchemaConstants.CHAR_SIZE_2.value,
                max=TeacherSchemaConstants.CHAR_SIZE_64.value,
            ),
        ],
    )
    working_since = fields.Date()


class TeacherInputSchema(TeacherBaseSchema):
    """Teacher Input schema for Teacher model."""
    pass


class TeacherOutputSchema(TeacherBaseSchema):
    """Teacher Output schema for Teacher model."""

    card_id = fields.Str(
        required=False,
        validate=[
            validate.Length(
                min=TeacherSchemaConstants.CHAR_SIZE_2.value,
                max=TeacherSchemaConstants.CHAR_SIZE_64.value,
            ),
        ],
    )


class TeacherUpdateSchema(TeacherBaseSchema):
    """Teacher Update schema for Teacher model."""
    qualification = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=TeacherSchemaConstants.CHAR_SIZE_2.value,
                max=TeacherSchemaConstants.CHAR_SIZE_64.value,
            ),
        ],
    )
    working_since = fields.Date()
