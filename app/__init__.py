import os
from flask import Flask

app = Flask(__name__)
env_config = os.environ.get("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)

from app import routes
