from flask_restx import ValidationError
from marshmallow import Schema, fields, validates_schema, validate
from marshmallow.fields import DateTime

from src.common.common import DATE_TIME_FORMAT
from src.common.response import BaseResponseSchema


# request for get all api
class BookFilterQuerySchema(Schema):
    search = fields.String()
    page = fields.Integer()
    size = fields.Integer()


# response for get all api
class BookFilterInSchema(Schema):
    id = fields.Integer(required=True)
    title = fields.String(required=True)
    author_name = fields.String(required=True)
    pages_num = fields.Integer(required=True)
    review = fields.String(required=False)
    rate = fields.Integer(required=False)
    title_author = fields.String(required=True)


# response for get all api
class BookFilterDataSchema(Schema):
    items = fields.List(fields.Nested(BookFilterInSchema))
    total = fields.Integer(required=True)
    page_size = fields.Integer(required=True)
    page = fields.Integer(required=True)
    last_update = DateTime(required=True, format=DATE_TIME_FORMAT)


# response for get all api
class BookFilterResponseSchema(BaseResponseSchema):
    data = fields.Nested(BookFilterDataSchema)


# request for create api and update by id api
class BookCreateRequestSchema(Schema):
    title = fields.String(required=True)
    author_id = fields.Integer(required=True)
    pages_num = fields.Integer(required=True)
    review = fields.String(required=False)
    rate = fields.Integer(required=False, validate=validate.OneOf([1, 2, 3, 4, 5]))

    # this @validates_schema is trigger automatically when the api is calling
    # it helped us to check and custom validator
    # in this example, we will set "rate" and "review" as required
    # even if in the previous code, we've set these 2 fields as required=False
    @validates_schema
    def validate_rate_review(self, data, **kwargs):
        if (data.get('rate') and not data.get('review')) or (data.get('review') and not data.get('rate')):
            raise ValidationError("rate or review is required")


# response for create api
class BookCreateInSchema(BookCreateRequestSchema):
    id = fields.Integer(required=True)


# response for create api
class BookCreateResponseSchema(BaseResponseSchema):
    data = fields.Nested(BookCreateInSchema)


# response for get by id api
class BookGetResponseSchema(BaseResponseSchema):
    data = fields.Nested(BookFilterInSchema)


