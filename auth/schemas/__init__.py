from marshmallow import Schema, fields, validate

from common.constants.schemas import UserSchemaConstants


class AuthBaseSchema(Schema):
    """Auth Base schema for User model."""

    username = fields.Str(
        required=False,
        validate=[
            validate.Length(
                min=UserSchemaConstants.CHAR_SIZE_2.value,
                max=UserSchemaConstants.CHAR_SIZE_64.value,
            ),
        ],
    )
    password = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=UserSchemaConstants.CHAR_SIZE_6.value,
                max=UserSchemaConstants.CHAR_SIZE_256.value,
            ),
        ],
    )


class AuthUserInputSchema(AuthBaseSchema):
    """Auth Input schema for User model."""
    pass


class AuthUserOutputSchema(Schema):
    """Auth Output schema for access and refresh tokens."""
    access_token = fields.Str()
    refresh_token: fields.Str()


class AuthUserLogoutSchema(Schema):
    """Auth Logout schema for logout message."""
    message = fields.Str()
