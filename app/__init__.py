import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
env_config = os.environ.get("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
db = SQLAlchemy(app)

from app import routes, models, manage
