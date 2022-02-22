from app.import_data_v2 import import_data
from flask import app
from app import create_app, db
from fndr_backend.config import DevelopmentConfig
from app.models import Companies, Cities, Meta, companies_meta

app = create_app(config_class=DevelopmentConfig)
app.app_context().push()


import_data('db.json')
