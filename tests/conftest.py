from app.models import Users
import pytest
from app import create_app, db
from app.import_data_v2 import import_data
from flask_login import login_user
from config import TestConfig
import pdb


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
    pdb.set_trace()
    import_data('test_db.json')


@pytest.fixture(scope='module')
def new_user(client, init_testdb):
    new_user = Users(username='Test User', email='test@fnder-backend.com')
    new_user.set_password('testtest')

    db.session.add(new_user)
    db.session.commit()

    return new_user


@pytest.fixture(scope='module')
def login_users(client, init_testdb, new_user):

    with client.test_request_context():

        username = 'Test User'
        password = 'testtest'

        user = Users.query.filter_by(username=username).first()

        if user is not None and user.check_password(password):

            yield login_user(new_user, remember=False)
