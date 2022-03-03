def test_cors(client):
    '''
    GIVEN that there are more than 15 companies in the DB
    WHEN the '/api/companies' page is requested (GET)
    THEN the response will contain the first 15 records and their associated data
    '''
    response = client.get('/', headers={'Origin': 'http://www.example.com'})

    assert response.status_code == 200
    assert response.headers['Access-Control-Allow-Origin'] == 'http://www.example.com'
