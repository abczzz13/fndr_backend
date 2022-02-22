import os
import logging
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from config import Config
from logging.handlers import RotatingFileHandler


# The Application Factory way:
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
login = LoginManager()
cache = Cache()
login.login_view = 'auth.login'
login.login_message = ("Please log in to access this page.")


# Create the App
def create_app(config_class=Config):
    app = Flask(__name__)

    # Loading the Config
    app.config.from_object(config_class)

    # Initializing
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)

    # Registering the Blueprints
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Logging to file:
    if not app.debug and not app.testing:

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/fndr_backend.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('FNDR startup')

    # Returning app with context
    with app.app_context():
        from app import models

        return app
