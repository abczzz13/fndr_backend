from flask import json
import pdb


def test_get_companies(client, init_testdb, insert_data_db):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/companies' page is requested (GET) to get all companies
    THEN check that the response is valid and particular data can be found
    """
    response = client.get("/api/companies")

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data[0]["city_name"] == "Rotterdam"
    assert data[1]["company_id"] == 1
