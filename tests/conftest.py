import os
from app import create_app, db
from app.utils_import import import_data
from app.models import Users
from config import TestConfig
from flask import json
import pytest


@pytest.fixture(scope="session")
def client():

    flask_app = create_app(config_class=TestConfig)

    # Create a test client
    with flask_app.test_client() as test_client:

        # Establish the application context
        with flask_app.app_context():

            yield test_client


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
def insert_data_db(init_testdb):
    file = os.path.join(TestConfig.APP_ROOT, "tests", "test_db.json")
    import_data(file)


@pytest.fixture(scope="session")
def new_user(init_testdb):
    new_user = Users(username="Test User", email="test@fnder-backend.com")
    new_user.set_password("testtest")

    db.session.add(new_user)
    db.session.commit()

    return new_user


@pytest.fixture(scope="session")
def get_token(client, new_user):

    data = {"username": "Test User", "password": "testtest"}

    response = client.post(
        "/auth/token",
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )

    result = json.loads(response.get_data(as_text=True))

    token = result["token"]

    return token
