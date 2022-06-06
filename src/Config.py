import os
from dotenv import load_dotenv

load_dotenv()

# read config from .env file by using dotenv library
# syntax: os.environ.get('variable in .env file')


class Config:
    SQL_ALCHEMY_DATABASE_URI = os.environ.get('SQL_ALCHEMY_DATABASE_URI')
    API_PREFIX = os.environ.get('API_PREFIX')
    VERSION = os.environ.get('VERSION')
    TITLE = os.environ.get('TITLE')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
