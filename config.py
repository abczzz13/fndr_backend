import os


# Configuration Settings


class Config(object):
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"


# Configuration Settings for Production
class ProductionConfig(Config):
    pass


# Configuration Settings for Development
class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
