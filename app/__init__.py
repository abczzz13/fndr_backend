import os
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
# from logging.handlers import RotatingFileHandler
import pdb
# from flask_restful import Resource, Api


# The Application Factory way:
db = SQLAlchemy()
migrate = Migrate()


# Create the App
def create_app(config_class=Config):
    app = Flask(__name__)

    # Loading the Config
    app.config.from_object(config_class)

    # Initializing
    db.init_app(app)
    migrate.init_app(app, db)

    # Registering the Blueprints
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        from app import models

        return app
