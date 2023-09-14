from flask_restx import ValidationError
from marshmallow import Schema, fields, validates_schema, validate
from marshmallow.fields import DateTime

from src.common.common import DATE_TIME_FORMAT
from src.common.response import BaseResponseSchema


class BookFilterQuerySchema(Schema):
    search = fields.String()
    page = fields.Integer()
    size = fields.Integer()


class BookFilterInSchema(Schema):
    id = fields.Integer(required=True)
    title = fields.String(required=True)
    author_name = fields.String(required=True)
    pages_num = fields.Integer(required=True)
    review = fields.String(required=False)
    rate = fields.Integer(required=False)
    title_author = fields.String(required=True)


class BookFilterDataSchema(Schema):
    items = fields.List(fields.Nested(BookFilterInSchema))
    total = fields.Integer(required=True)
    page_size = fields.Integer(required=True)
    page = fields.Integer(required=True)
    last_update = DateTime(required=True, format=DATE_TIME_FORMAT)


class BookFilterResponseSchema(BaseResponseSchema):
    data = fields.Nested(BookFilterDataSchema)


class BookCreateRequestSchema(Schema):
    title = fields.String(required=True)
    author_id = fields.Integer(required=True)
    pages_num = fields.Integer(required=True)
    review = fields.String(required=False)
    rate = fields.Integer(required=False, validate=validate.OneOf([1, 2, 3, 4, 5]))

    @validates_schema
    def validate_rate_review(self, data, **kwargs):
        if (data.get("rate") and not data.get("review")) or (
            data.get("review") and not data.get("rate")
        ):
            raise ValidationError("rate or review is required")


class BookCreateInSchema(BookCreateRequestSchema):
    id = fields.Integer(required=True)


class BookCreateResponseSchema(BaseResponseSchema):
    data = fields.Nested(BookCreateInSchema)


class BookGetResponseSchema(BaseResponseSchema):
    data = fields.Nested(BookFilterInSchema)
