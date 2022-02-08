import os
basedir = os.path.abspath(os.path.dirname(__file__))


# Configuration Settings
# https://realpython.com/flask-by-example-part-1-project-setup/
# How to set up the environment variables (APP_SETTINGS / SECRET_KEY) in the above link


class Config():
    DEBUG = False
    DEVELOPMENT = False
    # ?
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Configuration Settings for Production
class ProductionConfig(Config):
    pass


# Configuration Settings for Development
class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
