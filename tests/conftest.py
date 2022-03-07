from app import create_app, db
from app.import_data_v2 import import_data
from app.models import Users
from config import TestConfig
from flask import json
from flask_login import login_user
import pytest


@pytest.fixture(scope='module')
def client():

    flask_app = create_app(config_class=TestConfig)

    # Create a test client
    with flask_app.test_client() as test_client:

        # Establish the application context
        with flask_app.app_context():

            yield test_client


@pytest.fixture(scope='module')
def init_testdb():
    # To make sure to start with a clean slate:
    db.drop_all()

    # Create the database
    db.create_all()

    # Return the DB
    yield db

    # Drop the DB after testing
    db.session.close()
    db.drop_all()


@pytest.fixture(scope='module')
def insert_data_db(init_testdb):
    import_data('test_db.json')


@pytest.fixture(scope='module')
def new_user(init_testdb):
    new_user = Users(username='Test User', email='test@fnder-backend.com')
    new_user.set_password('testtest')

    db.session.add(new_user)
    db.session.commit()

    return new_user


@pytest.fixture(scope='module')
def get_token(client, init_testdb, new_user):

    data = {
        "username": "Test User",
        "password": "testtest"
    }

    response = client.post("/api/v1/token", data=json.dumps(data),
                           headers={"Content-Type": "application/json"},)

    result = json.loads(response.get_data(as_text=True))

    token = result['token']

    return token


@pytest.fixture(scope='module')
def login_users(client, init_testdb, new_user):

    with client.test_request_context():

        username = 'Test User'
        password = 'testtest'

        user = Users.query.filter_by(username=username).first()

        if user is not None and user.check_password(password):

            yield login_user(new_user, remember=False)
