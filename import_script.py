from app.import_data_v2 import import_data
import json
from app import db
from app.models import Companies, Cities, Meta, companies_meta
from app import create_app
app = create_app()
app.app_context().push()


import_data('db.json')
