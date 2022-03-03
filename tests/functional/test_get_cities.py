from flask import json


def test_get_cities(client, init_testdb, insert_data_db):
    '''
    GIVEN that there are more than 15 companies in the DB
    WHEN the '/api/v1/cities' page is requested (GET)
    THEN the response will contain a dict of all the city records (key) and the count (value) of companies in those cities
    '''
    response = client.get('/api/v1/cities')

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert len(data) == 11
    assert isinstance(data['Amsterdam'], int)


def test_get_cities_city_like(client, init_testdb, insert_data_db):
    '''
    GIVEN that Rotterdam and Amsterdam are in the cities DB 
    WHEN the '/api/v1/cities is requested with a city_like=Dam parameter
    THEN the response will contain 2 records and their associated data
    '''
    response = client.get('/api/v1/cities?city_like=Dam')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert len(data) == 2
    assert isinstance(data['Amsterdam'], int)
    assert isinstance(data['Rotterdam'], int)
