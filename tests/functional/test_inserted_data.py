from flask import json


def test_inserted_data(client, init_testdb, insert_data_db):
    """
    GIVEN a Flask application with a test DB configured for testing
    WHEN the specific data is inserted in the test DB and /companies is called
    THEN check that the specifid data can be found
    """

    response = client.get("/companies")

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data[0]["company_name"] == "Testing Company #1"
    assert data[1]["city_name"] == "Rotterdam"
    assert data[0]["tag"] == "Python"
    assert data[1]["company_id"] == "2"
