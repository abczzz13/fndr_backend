from flask import json


def test_get_cities(client, insert_data_db):
    '''
    GIVEN that there are mutiple cities in the DB
    WHEN the '/api/v1/cities' page is requested (GET)
    THEN the response will contain a list of all the cities and the count of companies in those cities
    '''
    response = client.get('/api/v1/cities')

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert len(data) == 11
    assert data[0][0] == 'Rotterdam'


def test_get_cities_city_like(client):
    '''
    GIVEN that Rotterdam and Amsterdam are in the cities DB 
    WHEN the '/api/v1/cities is requested with a city_like=Dam parameter
    THEN the response will contain 2 records and their associated data
    '''
    response = client.get('/api/v1/cities?city_like=Dam')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0][0] == 'Rotterdam'
    assert data[1][0] == 'Amsterdam'
