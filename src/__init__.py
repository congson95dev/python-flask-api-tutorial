from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt_extended import JWTManager
from src.models.base import db
from src.Config import Config
import datetime
from src.common.handle_exception import handle_exception


app = Flask(__name__)

# connect to postgres db
DB_URL = "postgresql+psycopg2://{user}:{pw}@{url}/{db}".format(
    user=Config.DB_USERNAME,
    pw=Config.DB_PASSWORD,
    url=Config.DB_URL,
    db=Config.DB_DATABASE,
)

# config
# to create new db, just need to set db name in SQLALCHEMY_DATABASE_URI,
# and run "flask db upgrade", so it will create new db for you
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# config for refresh token
# docs: https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens/
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(days=30)

app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
# set this so when we return jsonify in api, it will not sort the result by alphabelt
app.config['JSON_SORT_KEYS'] = False

# add handle exception
handle_exception(app)

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

# init flask_jwt_extended
# to use this jwt, you need to call /auth/login with body = username and password of user to get access token
#
# then you call to /auth/protected to check user info,
# need to transfer to the header:
# key: Authorization
# value: Bearer + ' ' + your access token
#
# from now on, if you want your api to set token before call, you need to add @jwt_required() before function
jwt = JWTManager(app)


# init api from flask_restx
api = Api(app)

# we import this files at the end of the file because in those file,
# we call some variable of this __init__.py file inside it
# such as variable "api"
import src.apis.base

