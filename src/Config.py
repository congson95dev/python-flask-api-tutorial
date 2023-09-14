import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQL_ALCHEMY_DATABASE_URI = os.environ.get("SQL_ALCHEMY_DATABASE_URI")
    API_PREFIX = os.environ.get("API_PREFIX")
    VERSION = os.environ.get("VERSION")
    TITLE = os.environ.get("TITLE")
    JWT_COOKIE_SECURE = os.environ.get("JWT_COOKIE_SECURE")
    JWT_TOKEN_LOCATION = os.environ.get("JWT_TOKEN_LOCATION")
    JWT_ACCESS_TOKEN_EXPIRES = os.environ.get("JWT_ACCESS_TOKEN_EXPIRES")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    ALLOWED_AUDS = os.environ.get("ALLOWED_AUDS")
    DB_URL = os.environ.get("DB_URL")
    DB_HOST = os.environ.get("DB_HOST")
    DB_DATABASE = os.environ.get("DB_DATABASE")
    DB_USERNAME = os.environ.get("DB_USERNAME")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
