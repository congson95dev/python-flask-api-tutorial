import re

from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_restx import Resource, Namespace
from sqlalchemy import or_

from src.models.base import db
from src.models.user import User

# this have to import below the api variable,
# because api variable is called in this UserSchema file
from src.schemas.User.UserSchema import user_register_schema, user_update_schema

# we use flask_restx to handle api instead of Flask itself
# in this flask_restx, the function is named by the HTTP method,
# such as get() = GET, post() = POST
# also, it will show api detail in browser, so we don't need to use postman to test API
# we can test API directly on browser

# add namespace for api, when we run in browser,
# we will see this in the title of each api block
api = Namespace(
    "User",
    description="User related operations",
)


# when we add prefix to api and assign it to namespace, it will now used as a new api
# so you have to use it like @user_api.route, but not @api.route as normal


@api.route("/")
class Users(Resource):
    # @jwt_required used to make user must set token before call api
    @jwt_required()
    def get(self):
        # handle search
        search_params = request.args.get("search")
        if search_params:
            search = "%{}%".format(search_params)
            # multiple search, using or_
            users = User.query.filter(
                or_(User.username.like(search), User.email.like(search))
            ).all()
        else:
            users = User.query.with_entities(User.email, User.username)

        result = []
        for user in users:
            user_data = {}
            user_data["email"] = user.email
            user_data["username"] = user.username

            result.append(user_data)
        if not result:
            return {
                "message": "we can't find any user that's matched your request",
            }, 200
        return {
            "users": result,
        }, 200

    # this expect is called to schema,
    # and this schema is like a validate to this function
    # also, it will allow us to edit the value of api in browser
    @api.expect(user_register_schema, validate=True)
    def post(self):
        data = request.get_json()
        if not validate_email(data.get("email")):
            return {
                "message": "Invalid Email",
            }, 500
        try:
            user = User(data.get("email"), data.get("username"), data.get("password"))
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            return {
                "message": "An Exception Occurred. Detail: %s" % str(e),
            }, 500
        return {"message": "User created", "user_id": user.id}, 200


@api.route("/<int:user_id>")
class UserDetail(Resource):
    def get(self, user_id):
        user = (
            User.query.filter_by(id=user_id)
            .with_entities(User.email, User.username)
            .first()
        )
        if not user:
            return jsonify({"message": "user with id %s does not exist" % user_id})
        result = {"id": user_id, "email": user.email, "username": user.username}
        return {
            "user": result,
        }, 200

    # this expect is called to schema,
    # and this schema is like a validate to this function
    # also, it will allow us to edit the value of api in browser
    @api.expect(user_update_schema, validate=True)
    def put(self, user_id):
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return jsonify({"message": "user with id %s does not exist" % user_id})
            try:
                data = request.get_json()
                if data.get("password"):
                    user.password = data.get("password")
                db.session.commit()
            except Exception as e:
                return {
                    "message": "An Exception Occurred. Detail: %s" % str(e),
                }, 500
            return {
                "message": "User %s's password updated, new password: %s"
                % (
                    user.username,
                    data.get("password"),
                )
            }, 200

    def delete(self, user_id):
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return jsonify({"message": "user with id %s does not exist" % user_id})
            try:
                db.session.delete(user)
                db.session.commit()
            except Exception as e:
                return {
                    "message": "An Exception Occurred. Detail: %s" % str(e),
                }, 500
            return {
                "message": "User deleted",
            }, 200


# validate email so it will be in the format like test@gmail.com
def validate_email(email):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return True if re.match(regex, email) else False
