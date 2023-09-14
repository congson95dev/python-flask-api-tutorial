import re

from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_restx import Resource, Namespace
from sqlalchemy import or_

from src.models.base import db
from src.models.user import User

from src.schemas.User.UserSchema import user_register_schema, user_update_schema

api = Namespace(
    "User",
    description="User related operations",
)


@api.route("/")
class Users(Resource):
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


def validate_email(email):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return True if re.match(regex, email) else False
