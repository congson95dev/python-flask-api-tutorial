import logging
import os

from flask import Flask, request
from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt_extended import JWTManager
from src.models.base import db
from src.Config import Config
import datetime
from datetime import datetime as dt
from src.common.handle_exception import handle_exception
from flask_cors import CORS

# add coverage before init Flask will prevent issue of coverage
# which is doesn't cover some class, method .. and the total percent is not get 100%
COV = None
if os.getenv("FLASK_COVERAGE") == "1":
    import coverage

    COV = coverage.coverage(config_file=".coveragerc")
    COV.start()

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
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# config for refresh token
# docs: https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens/
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(days=30)

app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
# set this so when we return jsonify in api, it will not sort the result by alphabelt
app.config["JSON_SORT_KEYS"] = False

# cors allow all
app.config["CORS_HEADERS"] = "Content-Type"
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# add handle exception
handle_exception(app)

# assign app to db
# we use this instead of db = SQLAlchemy(app)
db.init_app(app)

# add migrate to handle database changed data
#
# to use migrate feature, we need to call this 2 line of code,
# also we need to run this 3 command:
# flask db init
# flask db migrate -m "Initial migration."
# flask db upgrade
#
# docs: https://flask-migrate.readthedocs.io/en/latest/
migrate = Migrate()
migrate.init_app(app, db)

# init flask_jwt_extended
# to use this jwt, you need to call /auth/login
# with body = username and password of user to get access token
#
# then you call to /auth/protected to check user info,
# need to transfer to the header:
# key: Authorization
# value: Bearer + ' ' + your access token
#
# from now on, if you want your api to set token before call,
# you need to add @jwt_required() before function
jwt = JWTManager(app)

# init api from flask_restx
api = Api(app)

# init logger
# now we can import and use this without re-init it
# check src/apis/auth/routes.py to see the demo
logger = logging.getLogger()


# log every API call to logs file
# it will print in log file something like this:
# [October 06, 2023 09:36:01 +07] [INFO | __init__:87] 127.0.0.1 [GET]
# /user/ http http://127.0.0.1:5000/user?search=@gmail PostmanRuntime/7.33.0
@app.before_request
def before_request():
    """Logging before every request."""
    logger.info(
        "%s [%s] %s %s %s %s",
        request.remote_addr,
        request.method,
        request.path,
        request.scheme,
        request.referrer,
        request.user_agent,
    )


# we import this files at the end of the file because in those file,
# we call some variable of this __init__.py file inside it
# such as variable "api"
import src.apis.base
