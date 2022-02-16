import os
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import pdb
# from flask_restful import Resource, Api


# The Application Factory way:
db = SQLAlchemy()
migrate = Migrate()


# Create the App
def create_app(config_class=Config):
    app = Flask(__name__)

    # Defining the Config from the environment
    env_config = os.environ.get("APP_SETTINGS") or "config.DevelopmentConfig"
    # env_config = "config.TestConfig"
    app.config.from_object(env_config)
    # pdb.set_trace()

    # Initializing
    db.init_app(app)
    migrate.init_app(app, db)

    # Registering the Blueprints
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        from app import routes, models, errors
        # pdb.set_trace()
        return app
