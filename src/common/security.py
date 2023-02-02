from src.models.user import User


def authenticate(username, password):
    user = User.query.filter(User.username == username).first()
    if user and user.verify_password(password):
        return user
