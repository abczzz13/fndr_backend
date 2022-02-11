from app import app, db
from app.models import Companies, Cities, Meta, companies_meta


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Companies': Companies, 'Cities': Cities, 'Meta': Meta, 'companies_meta': companies_meta}
