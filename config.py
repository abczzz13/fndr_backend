import os
import re
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

ACCESS_EXPIRES = timedelta(hours=1)
# TODO: Cleanup the config profiles


# Configuration Settings
class Config():
    DEBUG = False
    DEVELOPMENT = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')


# Configuration Settings for Production
class ProductionConfig(Config):

    # Adjust DB URI for sqlalchemy to work with Heroku
    if os.environ.get('DATABASE_URL') is not None:
        uri = os.environ.get('DATABASE_URL')
        if uri.startswith('postgres://'):
            uri = uri.replace('postgres://', 'postgresql://', 1)

        SQLALCHEMY_DATABASE_URI = uri

    # Heroku Redis DB
    # CACHE_REDIS_URL = os.environ['REDIS_TLS_URL'] or os.environ['REDIS_URL']


# Configuration Settings for Development
class DevelopmentConfig(Config):

    # Creating the Postgres Database URI
    POSTGRES_URL = os.environ.get('POSTGRES_URL')
    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PW = os.environ.get('POSTGRES_PW')
    POSTGRES_DB = os.environ.get('POSTGRES_DB')
    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)

    # Cache Redis DB settings
    CACHE_TYPE = os.environ['CACHE_TYPE']
    # CACHE_REDIS_HOST = os.environ['CACHE_REDIS_HOST']
    # CACHE_REDIS_PORT = os.environ['CACHE_REDIS_PORT']
    # CACHE_REDIS_DB = os.environ['CACHE_REDIS_DB']
    CACHE_REDIS_URL = os.environ['REDIS_URL']
    CACHE_DEFAULT_TIMEOUT = os.environ['CACHE_DEFAULT_TIMEOUT']

    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_ECHO = True


class TestConfig(Config):

    # Creating the Postgres Database URI
    POSTGRES_URL = os.environ.get('POSTGRES_URL')
    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PW = os.environ.get('POSTGRES_PW')
    POSTGRES_DB = 'fndr_backend_test'
    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)

    # Cache Redis DB settings
    CACHE_TYPE = os.environ['CACHE_TYPE']
    # CACHE_REDIS_HOST = os.environ['CACHE_REDIS_HOST']
    # CACHE_REDIS_PORT = os.environ['CACHE_REDIS_PORT']
    # CACHE_REDIS_DB = os.environ['CACHE_REDIS_DB']
    CACHE_REDIS_URL = os.environ['REDIS_URL']
    CACHE_DEFAULT_TIMEOUT = os.environ['CACHE_DEFAULT_TIMEOUT']

    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_ECHO = True

    TESTING = True
