import os
from dotenv import load_dotenv

load_dotenv()

# read config from .env file by using dotenv library
# syntax: os.environ.get('variable in .env file')


class Config:
    API_PREFIX = os.environ.get("API_PREFIX")
    VERSION = os.environ.get("VERSION")
    TITLE = os.environ.get("TITLE")
    JWT_COOKIE_SECURE = os.environ.get("JWT_COOKIE_SECURE")
    JWT_TOKEN_LOCATION = os.environ.get("JWT_TOKEN_LOCATION")
    JWT_ACCESS_TOKEN_EXPIRES = os.environ.get("JWT_ACCESS_TOKEN_EXPIRES")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    ALLOWED_AUDS = os.environ.get("ALLOWED_AUDS")
    DB_URL = os.environ.get("DB_URL")
    DB_DATABASE = os.environ.get("DB_DATABASE")
    DB_USERNAME = os.environ.get("DB_USERNAME")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")


class TestConfiguration(Config):
    DB_URL = os.environ.get("DB_TEST_URL")
    DB_DATABASE = os.environ.get("DB_TEST_DATABASE")
    DB_USERNAME = os.environ.get("DB_TEST_USERNAME")
    DB_PASSWORD = os.environ.get("DB_TEST_PASSWORD")
