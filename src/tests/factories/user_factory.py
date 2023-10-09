import factory.fuzzy

from src.models.base import db
from src.models.user import User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"

    email = factory.fuzzy.FuzzyText(length=10)
    username = factory.fuzzy.FuzzyText(length=10)
    password = factory.fuzzy.FuzzyText(length=10)
