from flask import json


def test_get_companies(client, insert_data_db):
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


def test_get_companies_pagination(client, insert_data_db):
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


def test_get_companies_city_like(client, insert_data_db):
    '''
    GIVEN that there are 5 companies in the DB with city 'Rotterdam' and 2 companies with city 'Groningen'
    WHEN the '/api/companies' is requested with a city_like=Ro parameter
    THEN the response will contain 7 records and their associated data
    '''
    response = client.get('/api/v1/companies?city_like=Ro')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert len(data['items']) == 7


def test_get_companies_size(client, insert_data_db):
    '''
    GIVEN that there are 19 companies in the DB with size of '11-50'
    WHEN the '/api/companies' is requested with a size=11-50 parameter
    THEN the response will contain 19 records and their associated data
    '''
    response = client.get('/api/v1/companies?company_size=11-50&per_page=20')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert len(data['items']) == 19


def test_get_companies_multiple_parameters(client, insert_data_db):
    '''
    GIVEN that there is 1 company in the DB with size of 'GT-100' with city 'Rotterdam'
    WHEN the '/api/companies' is requested with a company_size=GT-100 and city_name=Rotterdam parameters
    THEN the response will contain 1 records and their associated data
    '''
    response = client.get(
        '/api/v1/companies?company_size=GT-100&city_name=Rijnsburg')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert len(data['items']) == 1
