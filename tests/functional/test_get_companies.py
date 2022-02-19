from flask import json
import pdb


def test_get_companies(client, init_testdb, insert_data_db):
    """
    GIVEN that there are more than 15 companies in the DB
    WHEN the '/api/companies' page is requested (GET)
    THEN the response will contain the first 15 records and their associated data
    """
    response = client.get("/api/companies")

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    # assert len(data) == 15
    assert isinstance(data[0]["city_name"], str)
    assert isinstance(data[0]["company_id"], int)


def test_get_companies_pagination(client, init_testdb, insert_data_db):
    """
    GIVEN that there are more than 15 companies in the DB
    WHEN the '/api/companies' is requested with page=2 as a url parameter
    THEN the response will contain the 16-30 records and their associated data
    """
    response1 = client.get("/api/companies")
    response2 = client.get("/api/companies?page=2")
    data1 = json.loads(response1.get_data(as_text=True))
    data2 = json.loads(response2.get_data(as_text=True))

    assert response2.status_code == 200
    assert len(data2) == 15
    assert data1[0]['company_id'] != data2[0]['company_id']
    assert data1[0]['company_id'] == 1
    assert data2[0]['company_id'] == 16


def test_get_companies_pagination(client, init_testdb, insert_data_db):
    """
    GIVEN that there are 5 companies in the DB with city 'Rotterdam' and 2 companies with city "Groningen"
    WHEN the '/api/companies' is requested with a city_like=Ro parameter
    THEN the response will contain 7 records and their associated data
    """
    response = client.get("/api/companies?city_like=Ro")
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert len(data) == 7


def test_get_companies_size(client, init_testdb, insert_data_db):
    """
    GIVEN that there are 5 companies in the DB with size of "11-50"
    WHEN the '/api/companies' is requested with a size=11-50 parameter
    THEN the response will contain 5 records and their associated data
    """
    response = client.get("/api/companies?size=11-50")
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert len(data) == 5


def test_get_multiple_parameters(client, init_testdb, insert_data_db):
    """
    GIVEN that there are 2 companies in the DB with size of "11-50" with city "Rotterdam"
    WHEN the '/api/companies' is requested with a size=11-50 and city=Rotterdam parameters
    THEN the response will contain 2 records and their associated data
    """
    response = client.get("/api/companies?size=11-50&city=Rotterdam")
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert len(data) == 2
