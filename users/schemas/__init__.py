from marshmallow import Schema, fields, validate

from common.constants.users import UserSchemaConstants


class UserBaseSchema(Schema):
    """User Base schema for User model."""

    first_name = fields.Str(
        required=False,
        validate=[
            validate.Length(
                min=UserSchemaConstants.CHAR_SIZE_2.value,
                max=UserSchemaConstants.CHAR_SIZE_64.value,
            ),
        ],
    )
    last_name = fields.Str(
        required=False,
        validate=[
            validate.Length(
                min=UserSchemaConstants.CHAR_SIZE_2.value,
                max=UserSchemaConstants.CHAR_SIZE_64.value,
            ),
        ],
    )
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=UserSchemaConstants.CHAR_SIZE_2.value,
                max=UserSchemaConstants.CHAR_SIZE_64.value,
            ),
        ],
    )
    email = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=UserSchemaConstants.CHAR_SIZE_2.value,
                max=UserSchemaConstants.CHAR_SIZE_256.value,
            ),
            validate.Regexp(regex=UserSchemaConstants.EMAIL_REGEX.value),
        ],
    )
    phone_number = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=UserSchemaConstants.CHAR_SIZE_2.value,
                max=UserSchemaConstants.CHAR_SIZE_64.value,
            ),
        ],
    )


class UserInputSchema(UserBaseSchema):
    """User Input schema for User model."""

    password = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=UserSchemaConstants.CHAR_SIZE_6.value,
                max=UserSchemaConstants.CHAR_SIZE_256.value,
            ),
        ],
    )


class UserOutputSchema(UserBaseSchema):
    """User Output schema for User model."""

    id = fields.UUID()
    is_activated = fields.Boolean()
    created_at = fields.DateTime()
