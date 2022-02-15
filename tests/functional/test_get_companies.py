from flask import json


def test_companies_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/companies' page is requested (GET)
    THEN check that the response is valid and particular data can be found
    """
    response = test_client.get("/companies")

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data[0]["city_name"] == "Rotterdam"
    assert data[692]["company_id"] == 693
