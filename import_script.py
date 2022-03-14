import os
from app import create_app
from app.import_data_v2 import import_data

app = create_app(config_class=os.environ.get('APP_SETTINGS'))
app.app_context().push()

import_data('db_v2.json')
