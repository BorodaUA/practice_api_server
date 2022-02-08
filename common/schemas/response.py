from marshmallow import Schema, fields


class ResponseBaseSchema(Schema):
    """Base schema for all http responses."""

    status = fields.Raw()
    data = fields.Raw()
    errors = fields.Raw()
