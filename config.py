import os
basedir = os.path.abspath(os.path.dirname(__file__))


# Configuration Settings
# https://realpython.com/flask-by-example-part-1-project-setup/
# How to set up the environment variables (APP_SETTINGS / SECRET_KEY) in the above link


class Config():
    DEBUG = False
    DEVELOPMENT = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Configuration Settings for Production
class ProductionConfig(Config):
    pass


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
