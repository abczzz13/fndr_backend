from flask import json


def test_get_token(client, new_user):
    '''
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to /api/v1/token with valid user credentials
    THEN check that a token is returned
    '''

    data = {
        "username": "Test User",
        "password": "testtest"
    }

    response = client.post("/api/v1/token", data=json.dumps(data),
                           headers={"Content-Type": "application/json"},)

    result = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert result['token'] is not None


def test_get_token_invalid(client, new_user):
    '''
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to /api/v1/token with invalid user credentials
    THEN check that the response is unauthorized and correct error message is shown
    '''

    data = {
        "username": "Not existing User",
        "password": "testtest"
    }

    response = client.post("/api/v1/token", data=json.dumps(data),
                           headers={"Content-Type": "application/json"},)

    result = json.loads(response.get_data(as_text=True))

    assert response.status_code == 401
    assert result['message'] == 'Invalid user credentials'
