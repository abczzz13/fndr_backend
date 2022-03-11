import os
import re
from datetime import timedelta
from dotenv import load_dotenv


# Load local .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


def get_env_variable(name):
    try:
        return os.environ.get(name)
    except KeyError:
        message = f"Expected environment variable {name} not set."
        raise Exception(message)


def create_db_url(user, pw, url, db):
    return f"postgresql://{user}:{pw}@{url}/{db}"


def get_env_db_url(env_setting):
    if env_setting == 'development':
        POSTGRES_URL = get_env_variable('POSTGRES_URL')
        POSTGRES_USER = get_env_variable('POSTGRES_USER')
        POSTGRES_PW = get_env_variable('POSTGRES_PW')
        POSTGRES_DB = get_env_variable('POSTGRES_DB')
    elif env_setting == 'staging':
        POSTGRES_URL = get_env_variable('POSTGRES_URL')
        POSTGRES_USER = get_env_variable('POSTGRES_USER')
        POSTGRES_PW = get_env_variable('POSTGRES_PW')
        POSTGRES_DB = get_env_variable('POSTGRES_DB')
    elif env_setting == 'production':
        POSTGRES_URL = get_env_variable('POSTGRES_URL')
        POSTGRES_USER = get_env_variable('POSTGRES_USER')
        POSTGRES_PW = get_env_variable('POSTGRES_PW')
        POSTGRES_DB = get_env_variable('POSTGRES_DB')
    elif env_setting == 'local':
        POSTGRES_URL = get_env_variable('POSTGRES_URL')
        POSTGRES_USER = get_env_variable('POSTGRES_USER')
        POSTGRES_PW = get_env_variable('POSTGRES_PW')
        POSTGRES_DB = get_env_variable('POSTGRES_DB')
    elif env_setting == 'testing':
        POSTGRES_URL = get_env_variable('TEST_POSTGRES_URL')
        POSTGRES_USER = get_env_variable('TEST_POSTGRES_USER')
        POSTGRES_PW = get_env_variable('TEST_POSTGRES_PW')
        POSTGRES_DB = get_env_variable('TEST_POSTGRES_DB')

    return create_db_url(POSTGRES_USER, POSTGRES_PW, POSTGRES_URL, POSTGRES_DB)


# DB URLS for each environment
LOCAL_DB_URL = get_env_db_url('local')
DEV_DB_URL = get_env_db_url('development')
TESTING_DB_URL = get_env_db_url('testing')
STAGING_DB_URL = get_env_db_url('staging')
PROD_DB_URL = get_env_db_url('production')


# Redis caching expiry time
ACCESS_EXPIRES = timedelta(hours=1)


class Config():
    DEBUG = False
    DEVELOPMENT = False
    TESTING = False

    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    MAX_CONTENT_LENGTH = 1024 * 1024
    UPLOAD_EXTENSIONS = set(['.jpg', '.png', '.gif'])
    S3_BUCKET_NAME = 'fndr'  # or also store in environment?
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_ACCESS_SECRET = os.environ.get('AWS_ACCESS_KEY')
    S3_LOCATION = 'https://{}.s3.amazonaws.com/'.format(S3_BUCKET_NAME)


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = DEV_DB_URL
    SQLALCHEMY_ECHO = True

    # Cache Redis DB settings
    CACHE_TYPE = os.environ['CACHE_TYPE']
    CACHE_REDIS_URL = os.environ['REDIS_URL']
    CACHE_DEFAULT_TIMEOUT = os.environ['CACHE_DEFAULT_TIMEOUT']


class LocalConfig(DevelopmentConfig):

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = LOCAL_DB_URL


class StagingConfig(Config):
    DEBUG = False
    DEVELOPMENT = False
    TESTING = False

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = STAGING_DB_URL
    SQLALCHEMY_ECHO = False

    # Cache Redis DB settings
    CACHE_TYPE = os.environ['CACHE_TYPE']
    CACHE_REDIS_URL = os.environ['REDIS_URL']
    CACHE_DEFAULT_TIMEOUT = os.environ['CACHE_DEFAULT_TIMEOUT']


class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False
    TESTING = False

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = PROD_DB_URL
    SQLALCHEMY_ECHO = False

    # Cache Redis DB settings
    CACHE_TYPE = os.environ['CACHE_TYPE']
    CACHE_REDIS_URL = os.environ['REDIS_URL']
    CACHE_DEFAULT_TIMEOUT = os.environ['CACHE_DEFAULT_TIMEOUT']


class TestConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    TESTING = True

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = TESTING_DB_URL
    SQLALCHEMY_ECHO = False

    # Cache Redis DB settings
    CACHE_TYPE = os.environ['CACHE_TYPE']
    CACHE_REDIS_URL = os.environ['REDIS_URL']
    CACHE_DEFAULT_TIMEOUT = os.environ['CACHE_DEFAULT_TIMEOUT']
