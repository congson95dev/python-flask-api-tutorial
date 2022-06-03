from src.models.user import User

# authenticate and identity is get from the flask_jwt docs, don't need to care about it
# docs: https://pythonhosted.org/Flask-JWT/


def authenticate(username, password):
    user = User.query.filter(User.username == username).first()
    if user and user.verify_password(password):
        return user

# authenticate and identity is get from the flask_jwt docs, don't need to care about it
# docs: https://pythonhosted.org/Flask-JWT/


def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)
