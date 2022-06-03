from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt import JWT
from src.models.user import db
from src.models.user import User
from src.common.security import authenticate, identity

app = Flask(__name__)

# config
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/ncson1/project/flask-project/flask-api-tutorial/src/bookstore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_SECRET_KEY'] = '21321321421415151'

# assign app to db
# we use this instead of db = SQLAlchemy(app)
db.init_app(app)

# add migrate to handle database changed data
#
# to use migrate feature, we need to call this 2 line of code, also we need to run this 3 command:
# flask db init
# flask db migrate -m "Initial migration."
# flask db upgrade
#
# docs: https://flask-migrate.readthedocs.io/en/latest/
migrate = Migrate()
migrate.init_app(app, db)

# init flask_jwt
# authenticate and identity is get from the flask_jwt docs, don't need to care about it
# to use this jwt, you need to call /auth with body = username and password of user to get access token
#
# then you call to /auth/protected to check access token,
# need to transfer header = Authorization: JWT + ' ' + your access token
#
# from now on, if you want your api to set token before call, you need to add @jwt_required() before function
jwt = JWT(app, authenticate, identity)


# init api from flask_restx
api = Api(app)

# we import this files at the end of the file because in those file,
# we call some variable of this __init__.py file inside it
# such as variable "api"
import src.apis.auth.routes
import src.apis.user.routes

