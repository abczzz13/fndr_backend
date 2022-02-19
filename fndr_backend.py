#from app import app, db
from app import create_app, db
from app.models import Companies, Cities, Meta, Users, companies_meta
import pdb
import os
import config

config_variables = config.DevelopmentConfig
if os.environ.get("FLASK_ENV") == "production":
    config_variables = config.ProductionConfig
# pdb.set_trace()
app = create_app(config_class=config_variables)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Companies': Companies, 'Cities': Cities, 'Meta': Meta, 'companies_meta': companies_meta, 'Users': Users}
