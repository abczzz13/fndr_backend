import os
import re
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


# Configuration Settings
# https://realpython.com/flask-by-example-part-1-project-setup/
# How to set up the environment variables (APP_SETTINGS / SECRET_KEY) in the above link


class Config():
    DEBUG = False
    DEVELOPMENT = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Configuration Settings for Production
class ProductionConfig(Config):

    # Adjust DB URI for sqlalchemy to work with Heroku
    if os.environ.get("DATABASE_URL") is not None:
        uri = os.environ.get("DATABASE_URL")
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)

        SQLALCHEMY_DATABASE_URI = uri


# Configuration Settings for Development
class DevelopmentConfig(Config):

    # Creating the Database URI
    POSTGRES_URL = os.environ.get("POSTGRES_URL")
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PW = os.environ.get("POSTGRES_PW")
    POSTGRES_DB = os.environ.get("POSTGRES_DB")
    DB_URL = "postgresql+psycopg2://{user}:{pw}@{url}/{db}".format(
        user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)

    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_ECHO = True
