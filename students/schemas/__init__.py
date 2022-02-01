from marshmallow import Schema, fields, validate

from common.constants.schemas import StudentSchemaConstants


class StudentBaseSchema(Schema):
    """Student Base schema for Student model."""

    id = fields.UUID()
    student_since = fields.Date()


class StudentInputSchema(StudentBaseSchema):
    """Student Input schema for Student model."""
    pass


class StudentOutputSchema(StudentBaseSchema):
    """Student Output schema for Student model."""

    card_id = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=StudentSchemaConstants.CHAR_SIZE_2.value,
                max=StudentSchemaConstants.CHAR_SIZE_64.value,
            ),
        ],
    )


class StudentUpdateSchema(StudentBaseSchema):
    """Teacher Update schema for Teacher model."""

    student_since = fields.Date()
