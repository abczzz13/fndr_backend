from app import create_app
from app.import_data_v2 import import_data
from config import DevelopmentConfig

app = create_app(config_class=DevelopmentConfig)
app.app_context().push()

import_data('db_v2.json')
