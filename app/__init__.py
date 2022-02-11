import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_seeder import FlaskSeeder
# from flask_restful import Resource, Api

app = Flask(__name__)
env_config = os.environ.get("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
 
seeder = FlaskSeeder()
seeder.init_app(app, db)


from app import routes, models