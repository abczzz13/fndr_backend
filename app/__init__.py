import os
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
# from flask_restful import Resource, Api

'''
The Application Factory way:

db = SQLAlchemy()
migrate = Migrate()


def create app(config_class=Config):
    app = Flask(__name__)
    env_config = os.environ.get("APP_SETTINGS") or "config.DevelopmentConfig"
    app.config.from_object(env_config)

    db.init_app(app)
    migrate.init_app(app, db)

    return app


'''

app = Flask(__name__)
env_config = os.environ.get("APP_SETTINGS") or "config.DevelopmentConfig"
app.config.from_object(env_config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes, models