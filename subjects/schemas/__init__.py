from marshmallow import Schema, fields, validate

from common.constants.schemas import SubjectSchemaConstants


class SubjectBaseSchema(Schema):
    """Subject Base schema for Subject model."""

    title = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=SubjectSchemaConstants.CHAR_SIZE_2.value,
                max=SubjectSchemaConstants.CHAR_SIZE_256.value,
            ),
        ],
    )
    code = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=SubjectSchemaConstants.CHAR_SIZE_2.value,
                max=SubjectSchemaConstants.CHAR_SIZE_16.value,
            ),
        ],
    )


class SubjectInputSchema(SubjectBaseSchema):
    """Subject Input schema for Subject model."""
    pass


class SubjectOutputSchema(SubjectBaseSchema):
    """Subject Output schema for Subject model."""
    id = fields.UUID()


class SubjectUpdateSchema(SubjectBaseSchema):
    """Subject Update schema for Subject model."""
    pass
