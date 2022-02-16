from flask import json


def test_api_get_company(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/companies' page is requested (GET)
    THEN check that the response is valid and particular data can be found
    """

    response = client.get("/api/companies/1")
    # pdb.set_trace()
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data["city_name"] == "Rotterdam"
    assert data["company_id"] == 1
