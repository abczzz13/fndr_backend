from flask import json


def test_get_company(client, init_testdb, insert_data_db):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/companies' page is requested (GET) to get a specific company
    THEN check that the response is valid and particular data can be found
    """
    response = client.get("/api/v1/companies/1")

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data["city_name"] == "Rotterdam"
    assert data["company_id"] == 1
