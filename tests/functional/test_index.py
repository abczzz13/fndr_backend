import pdb
from flask import json


def test_index(client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    # pdb.set_trace()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Under construction" in response.data


def test_companies_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/companies' page is requested (GET)
    THEN check that the response is valid and particular data can be found
    """

    response = client.get("/companies")
    # pdb.set_trace()
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data[0]["city_name"] == "Rotterdam"
    # assert data[692]["company_id"] == 693
