from functools import wraps

from flask import request
from flask_jwt_extended import current_user

from src import db
from src.common.common import ROLE
from src.models import Book
from src.models.user import User


def authenticate(username, password):
    user = User.query.filter(User.username == username).first()
    if user and user.verify_password(password):
        return user


def validate_role_itself_or_admin():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # if current user role is admin, allow it to pass
            if current_user.role == ROLE.get("admin"):
                return fn(*args, **kwargs)
            else:
                # if current user role is operator, only allow to see record of itself
                id = request.path.rsplit("/", 1)[-1]
                author_id = [
                    value[0]
                    for value in db.session.query(Book)
                    .filter(Book.id == id)
                    .with_entities(Book.author_id)
                ]
                if len(author_id) == 0:
                    return fn(*args, **kwargs)

                if current_user.id == author_id[0]:
                    return fn(*args, **kwargs)
                return {"message": "You are not authorized to access this data."}, 403

        return wrapper

    return decorator


def validate_assign_author_itself():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # if current user role is admin, allow it to pass
            if current_user.role == ROLE.get("admin"):
                return fn(*args, **kwargs)
            else:
                # if current user role is operator,
                # only allow to assign itself to the record
                data = request.get_json()
                if (
                    data.get("author_id") is None
                    or data.get("author_id") is current_user.id
                ):
                    return fn(*args, **kwargs)
                return {
                    "message": "You are not authorized to assign "
                    "other than yourself to this data."
                }, 403

        return wrapper

    return decorator
