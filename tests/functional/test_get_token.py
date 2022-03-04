from flask import json


def test_get_token(client, new_user):
    '''
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to /api/v1/companies with a valid company
    THEN check that the response is valid and particular data can be found
    '''

    data = {
        "username": "Test User",
        "password": "testtest"
    }

    response = client.post("/api/v1/token", data=json.dumps(data),
                           headers={"Content-Type": "application/json"},)

    result = json.loads(response.get_data(as_text=True))
    print(result)
    assert response.status_code == 200
    assert result['token'] is not None
