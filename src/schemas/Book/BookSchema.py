from flask_restx import fields

from src import api

# look like this schema feature is come from flask_restx as well
# this schema is used as a validate for model


book_add_schema = api.model('BookAddSchema', {
    'title': fields.String(required=True),
    'author_id': fields.Integer(required=True)
})

book_update_schema = api.model('BookUpdateSchema', {
    'password': fields.String(required=True)
})