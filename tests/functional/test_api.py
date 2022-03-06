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
    assert data[0][0] == 'Rotterdam'
    assert data[1][0] == 'Amsterdam'


def test_get_companies(client, init_testdb, insert_data_db):
    '''
    GIVEN that there are more than 15 companies in the DB
    WHEN the '/api/companies' page is requested (GET)
    THEN the response will contain the first 15 records and their associated data
    '''
    response = client.get('/api/v1/companies')

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert len(data['items']) == 15
    assert isinstance(data['items'][0]['city_name'], str)
    assert isinstance(data['items'][0]['company_id'], int)


def test_get_companies_pagination(client, init_testdb, insert_data_db):
    '''
    GIVEN that there are more than 15 companies in the DB
    WHEN the '/api/companies' is requested with page=2 as a url parameter
    THEN the response will contain the 16-30 records and their associated data
    '''
    response1 = client.get('/api/v1/companies')
    response2 = client.get('/api/v1/companies?page=2')

    data1 = json.loads(response1.get_data(as_text=True))
    data2 = json.loads(response2.get_data(as_text=True))

    assert response2.status_code == 200
    assert len(data2['items']) == 5
    assert data1['items'][0]['company_id'] != data2['items'][0]['company_id']
    assert data1['items'][0]['company_id'] == 1  # 20?
    assert data2['items'][0]['company_id'] == 16  # 10?


def test_get_companies_city_like(client, init_testdb, insert_data_db):
    '''
    GIVEN that there are 5 companies in the DB with city 'Rotterdam' and 2 companies with city 'Groningen'
    WHEN the '/api/companies' is requested with a city_like=Ro parameter
    THEN the response will contain 7 records and their associated data
    '''
    response = client.get('/api/v1/companies?city_like=Ro')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert len(data['items']) == 7


def test_get_companies_size(client, init_testdb, insert_data_db):
    '''
    GIVEN that there are 19 companies in the DB with size of '11-50'
    WHEN the '/api/companies' is requested with a size=11-50 parameter
    THEN the response will contain 19 records and their associated data
    '''
    response = client.get('/api/v1/companies?size=11-50&per_page=20')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert len(data['items']) == 19


def test_get_multiple_parameters(client, init_testdb, insert_data_db):
    '''
    GIVEN that there are 2 companies in the DB with size of '11-50' with city 'Rotterdam'
    WHEN the '/api/companies' is requested with a size=11-50 and city=Rotterdam parameters
    THEN the response will contain 2 records and their associated data
    '''
    response = client.get('/api/v1/companies?size=GT-100&city=Rijnsburg')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert len(data['items']) == 1


def test_get_company(client, init_testdb, insert_data_db):
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/companies' page is requested (GET) to get a specific company
    THEN check that the response is valid and particular data can be found
    '''
    response = client.get('/api/v1/companies/1')

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['city_name'] == 'Rotterdam'
    assert data['company_id'] == 1
