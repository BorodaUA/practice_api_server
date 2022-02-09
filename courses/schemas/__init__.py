from marshmallow import Schema, fields, validate

from common.constants.schemas import CourseSchemaConstants
from teachers.schemas import TeacherOutputSchema


class CourseBaseSchema(Schema):
    """Course Base schema for Course model."""

    title = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=CourseSchemaConstants.CHAR_SIZE_2.value,
                max=CourseSchemaConstants.CHAR_SIZE_256.value,
            ),
        ],
    )
    code = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=CourseSchemaConstants.CHAR_SIZE_2.value,
                max=CourseSchemaConstants.CHAR_SIZE_16.value,
            ),
        ],
    )
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)


class CourseInputSchema(CourseBaseSchema):
    """Course Input schema for Course model."""
    teacher_id = fields.UUID()


class CourseOutputSchema(CourseBaseSchema):
    """Course Output schema for Course model."""
    id = fields.UUID()
    teacher = fields.Nested(TeacherOutputSchema)
