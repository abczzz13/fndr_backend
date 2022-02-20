import pytest
from app import create_app, db
from app.import_data_v2 import import_data
from config import TestConfig


@pytest.fixture(scope='module')
def client():

    flask_app = create_app(config_class=TestConfig)

    # Create a test client
    with flask_app.test_client() as test_client:

        # Establish the application context
        with flask_app.app_context():

            yield test_client


@pytest.fixture(scope='module')
def init_testdb(client):
    # Create the database
    db.create_all()

    # Return the DB
    yield db

    # Drop the DB after testing
    db.session.close()
    db.drop_all()


@pytest.fixture(scope='module')
def insert_data_db(client, init_testdb):
    import_data('test_db.json')
