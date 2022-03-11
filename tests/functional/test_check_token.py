from flask import json


def test_check_token(client, get_token):
    '''
    GIVEN a Flask application configured for testing
    WHEN a GET request is made to /api/v1/check_token with a valid token
    THEN check that the particular credentials are returned
    '''

    response = client.get('/api/v1/check_token',
                          headers={'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(get_token)},)

    result = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert result['id'] == 1
    assert result['username'] == 'Test User'
