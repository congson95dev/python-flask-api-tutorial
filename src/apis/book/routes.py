import re

from flask import jsonify, request
from flask_jwt import jwt_required
from flask_restx import Resource, Namespace
from sqlalchemy import or_

from flask_accepts import accepts, responds

from src import api
from src.models.base import db
from src.models.book import Book
# this have to import below the api variable, because api variable is called in this UserSchema file
from src.schemas.User.UserSchema import user_register_schema, user_update_schema

# we use flask_restx to handle api instead of Flask itself
# in this flask_restx, the function is named by the HTTP method, such as get() = GET, post() = POST
# also, it will show api detail in browser, so we don't need to use postman to test API
# we can test API directly on browser

# add namespace for api, when we run in browser, we will see this in the title of each api block
book_api = Namespace('Book', description='Book related operations', )
# assign namespace to url prefix
# with this, we will have url prefix = /book
api.add_namespace(book_api, path='/book')


# when we add prefix to api and assign it to namespace, it will now used as a new api
# so you have to use it like @user_api.route, but not @api.route as normal


@book_api.route('/')
class Books(Resource):
    # def get(self):
    #     # handle search
    #     search_params = request.args.get('search')
    #     if search_params:
    #         search = "%{}%".format(search_params)
    #         # multiple search, using or_
    #         books = Book.query.filter(
    #             Book.title.like(search)
    #         ).all()
    #     else:
    #         books = Book.query.all()
    #
    #     result = []
    #     for book in books:
    #         book_data = {}
    #         book_data['title'] = book.title
    #         book_data['username'] = book.username
    #
    #         result.append(book_data)
    #     if not result:
    #         return {
    #                "message": "we can't find any book that's matched your request",
    #            }, 200
    #     return {
    #                "users": result,
    #            }, 200

    # this expect is called to schema, and this schema is like a validate to this function
    # also, it will allow us to edit the value of api in browser
    # @book_api.expect(user_register_schema, validate=True)
    def post(self):
        data = request.get_json()
        try:
            book = Book(
                title=data.get('title'),
                author_id=data.get('author_id'),
                pages_num=data.get('pages_num'),
                review=data.get('review'),
                created_by=data.get('pages_num')
            )
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            return {
                       "message": "An Exception Occurred. Detail: %s" % str(e),
                   }, 500
        return {
                   "message": "User created",
                   "user_id": book.id
               }, 200
#
#
# @user_api.route('/<int:user_id>')
# class UserDetail(Resource):
#     def get(self, user_id):
#         user = User.query.filter_by(id=user_id).with_entities(User.email, User.username).first()
#         if not user:
#             return jsonify({'message': 'user with id %s does not exist' % user_id})
#         result = {
#             'id': user_id,
#             'email': user.email,
#             'username': user.username
#         }
#         return {
#                    "user": result,
#                }, 200
#
#     # this expect is called to schema, and this schema is like a validate to this function
#     # also, it will allow us to edit the value of api in browser
#     @user_api.expect(user_update_schema, validate=True)
#     def put(self, user_id):
#         if user_id:
#             user = User.query.filter_by(id=user_id).first()
#             if not user:
#                 return jsonify({'message': 'user with id %s does not exist' % user_id})
#             try:
#                 data = request.get_json()
#                 if data.get('password'):
#                     user.password = data.get('password')
#                 db.session.commit()
#             except Exception as e:
#                 return {
#                            "message": "An Exception Occurred. Detail: %s" % str(e),
#                        }, 500
#             return {
#                        "message": "User %s's password updated, new password: %s" % (user.username, data.get('password'))
#                    }, 200
#
#     # @jwt_required used to make user must set token before call api
#     @jwt_required()
#     def delete(self, user_id):
#         if user_id:
#             user = User.query.filter_by(id=user_id).first()
#             if not user:
#                 return jsonify({'message': 'user with id %s does not exist' % user_id})
#             try:
#                 db.session.delete(user)
#                 db.session.commit()
#             except Exception as e:
#                 return {
#                            "message": "An Exception Occurred. Detail: %s" % str(e),
#                        }, 500
#             return {
#                        "message": "User deleted",
#                    }, 200
#
#
# # validate email so it will be in the format like test@gmail.com
# def validate_email(email):
#     regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
#     return True if re.match(regex, email) else False