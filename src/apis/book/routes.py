from flask import request
from flask_accepts import accepts, responds
from flask_jwt_extended import jwt_required
from flask_restx import Resource, Namespace

from src.common.response import Responses
from src.schemas.Book.BookSchema import (
    BookCreateRequestSchema,
    BookCreateResponseSchema,
    BookFilterQuerySchema,
    BookFilterResponseSchema,
    BookGetResponseSchema,
)
from src.service.BookService import BookService

api = Namespace(
    "Book",
    description="Book related operations",
)


@api.route("/")
class Books(Resource):
    @jwt_required()
    @api.doc("Get list books by id")
    @accepts(query_params_schema=BookFilterQuerySchema, api=api)
    @responds(schema=BookFilterResponseSchema, api=api, status_code=200)
    def get(self):
        params = request.args.to_dict()
        response = BookService.get_list_book_by_search_params(params)
        return Responses.ok_response(response)

    @jwt_required()
    @api.doc("Create book")
    @accepts(schema=BookCreateRequestSchema, api=api)
    @responds(schema=BookCreateResponseSchema, api=api)
    def post(self):
        data = request.get_json()
        response_data = BookService.create_book(data)
        return Responses.ok_response(response_data)


@api.route("/<int:id>")
class BookDetail(Resource):
    @api.doc("Get detail book by id")
    @responds(schema=BookGetResponseSchema, api=api, status_code=200)
    def get(self, id: int):
        """
        Get job by jobId
        """
        response = BookService.get_book_by_id(id)
        return Responses.ok_response(response)

    @jwt_required()
    @api.doc("Update book by id")
    @accepts(schema=BookCreateRequestSchema, api=api)
    @responds(schema=BookCreateResponseSchema, api=api, status_code=200)
    def post(self, id: int):
        """
        Update the job
        """
        data = request.json
        response_data = BookService.update_book(data, id)
        return Responses.ok_response(response_data)

    @jwt_required()
    @api.doc("Delete book by id")
    def put(self, id: int):
        BookService.delete_book(id)
        return Responses.ok_response_without_data()
