def test_cors(client):
    '''
    GIVEN that the the flask application accepts CORS headers
    WHEN the '/' page is requested (GET) with a Origin header
    THEN the application will return a valid response and a Access-Control-Allow-Origin header
    '''
    response = client.get(
        'api/v1/companies',
        headers={'Origin': 'http://www.example.com'})

    assert response.status_code == 200
    assert response.headers['Access-Control-Allow-Origin'] == 'http://www.example.com'
