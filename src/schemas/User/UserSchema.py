from flask_restx import fields

from src import api


user_register_schema = api.model(
    "UserRegisterSchema",
    {
        "email": fields.String(required=True),
        "username": fields.String(required=True),
        "password": fields.String(required=True),
    },
)

user_update_schema = api.model(
    "UserUpdateSchema", {"password": fields.String(required=True)}
)
