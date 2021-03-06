from app.models import Users
from flask import json


def test_post_valid_user(client, get_token):
    '''
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to /auth/register with a valid user
    THEN check that the response is valid and particular data can be found
    '''
    data = {
        "username": "Test Gebruiker #323",
        "email": "test@test.com",
        "password": "abcdefgh"
    }

    response = client.post(
        '/auth/register',
        data=json.dumps(data),
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(get_token)},)

    result = json.loads(response.get_data(as_text=True))

    user = Users.query.filter_by(username=data['username']).first()

    assert response.status_code == 201
    assert result['id'] == 2
    assert result['username'] == 'Test Gebruiker #323'
    assert user.check_password(data['password'])
    assert not user.check_password('heelwatanders')


def test_post_invalid_username(client, get_token):
    '''
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to /auth/register with an already existing username
    THEN check that the response is invalid and particular error messages can be found
    '''
    data = {
        "username": "Test Gebruiker #323",
        "email": "testtest@test.com",
        "password": "abcdefgh"
    }

    response = client.post(
        '/auth/register',
        data=json.dumps(data),
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(get_token)},)

    result = json.loads(response.get_data(as_text=True))

    assert result['message']['_schema'][0] == "This username is already in use, please use a different username."


def test_post_invalid_email(client, get_token):
    '''
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to /auth/register with an already existing email address
    THEN check that the response is invalid and particular error messages can be found
    '''
    data = {
        "username": "Test Gebruiker #987",
        "email": "test@test.com",
        "password": "abcdefgh"
    }

    response = client.post(
        '/auth/register',
        data=json.dumps(data),
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(get_token)},)

    result = json.loads(response.get_data(as_text=True))

    assert result['message']['_schema'][0] == "This email address is already in use, please use a different email address."


def test_post_invalid_user(client, get_token):
    '''
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to /auth/register with a invalid user
    THEN check that the response is invalid and particular error messages can be found
    '''
    data1 = {
    }
    data2 = {
        "username": "x",
        "email": "x@x.x",
        "password": "abcd"
    }

    response1 = client.post(
        '/auth/register',
        data=json.dumps(data1),
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(get_token)},)

    response2 = client.post(
        '/auth/register',
        data=json.dumps(data2),
        headers={'Content-Type': 'application/json',
                 'Authorization': 'Bearer {}'.format(get_token)},)

    result1 = json.loads(response1.get_data(as_text=True))
    result2 = json.loads(response2.get_data(as_text=True))

    assert result1['message']['username'][0] == "Missing data for required field."
    assert result1['message']['email'][0] == "Missing data for required field."
    assert result1['message']['password'][0] == "Missing data for required field."
    assert result2['message']['username'][0] == "Length must be between 2 and 64."
    assert result2['message']['email'][0] == "Not a valid email address."
    assert result2['message']['password'][0] == "Length must be between 8 and 64."
