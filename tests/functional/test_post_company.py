from flask import json


def test_post_valid_company(client, get_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to /api/v1/companies with a valid company
    THEN check that the response is valid and particular data can be found
    """
    data = {
        "branches": ["Nog niet bestaande branche"],
        "city_name": "Lutjebroek",
        "company_name": "Test company #999",
        "company_size": "11-50",
        "disciplines": [
            "Conceptontwikkeling",
            "Conversie-optimalisatie",
            "Strategie",
            "Nog niet bestaande discipline",
            "Nog niet bestaande discipline #2",
        ],
        "logo_image_src": "https://www.nos.nl/",
        "region": "Remote",
        "tags": ["Angular", "App-bouwer", "Nog niet bestaande tag", "Nog niet bestaande tag #2"],
        "website": "https://www.google.com/",
        "year": 1969,
    }

    response = client.post(
        "/api/v1/companies",
        data=json.dumps(data),
        headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(get_token)},
    )

    result = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201
    assert result["company_id"] == 21
    assert result["company_name"] == "Test company #999"
    assert result["city_name"] == "Lutjebroek"
    assert result["region"] == "Remote"
    assert result["company_size"] == "11-50"
    assert result["branches"][0] == "Nog Niet Bestaande Branche"
    assert result["website"] == "https://www.google.com/"
    assert result["year"] == 1969


def test_post_valid_company_optional_fields(client, get_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to /api/v1/companies with a valid company missing some optional fields
    THEN check that the response is valid and particular data can be found
    """
    data = {
        "city_name": "Hoorn",
        "company_name": "Test company #777",
        "company_size": "GT-100",
        "website": "https://testdetest.nl",
    }

    response = client.post(
        "/api/v1/companies",
        data=json.dumps(data),
        headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(get_token)},
    )

    result = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201
    assert result["company_id"] == 22
    assert result["company_name"] == "Test company #777"
    assert result["city_name"] == "Hoorn"
    assert result["company_size"] == "GT-100"
    assert result["website"] == "https://testdetest.nl"


def test_post_invalid_company_id(client, insert_data_db, get_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to /api/v1/companies including a company id
    THEN check that the response is invalid and particular error messages can be found
    """
    data = {
        "branches": ["Nog niet bestaande branche"],
        "city_name": "Lutjebroek",
        "company_id": 21,
        "company_name": "Test company #999",
        "company_size": "11-50",
        "disciplines": [
            "Conceptontwikkeling",
            "Conversie-optimalisatie",
            "Strategie",
            "Nog niet bestaande discipline",
            "Nog niet bestaande discipline #2",
        ],
        "logo_image_src": "https://www.nos.nl/",
        "region": "Remote",
        "tags": ["Angular", "App-bouwer", "Nog niet bestaande tag", "Nog niet bestaande tag #2"],
        "website": "https://www.google.com/",
        "year": 1969,
    }

    response = client.post(
        "/api/v1/companies",
        data=json.dumps(data),
        headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(get_token)},
    )

    result = json.loads(response.get_data(as_text=True))

    assert (
        result["message"]["_schema"][0]
        == "Create new company cannot include company_id. For modifying existing companies please use the PATCH method"
    )


def test_post_invalid_company_name(client, get_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to /api/v1/companies with an already existing company name
    THEN check that the response is invalid and particular error messages can be found
    """
    data = {
        "branches": ["Nog niet bestaande branche"],
        "city_name": "Lutjebroek",
        "company_name": "daily dialogues (Part of CANDID)",
        "company_size": "11-50",
        "disciplines": [
            "Conceptontwikkeling",
            "Conversie-optimalisatie",
            "Strategie",
            "Nog niet bestaande discipline",
            "Nog niet bestaande discipline #2",
        ],
        "logo_image_src": "https://www.nos.nl/",
        "region": "Remote",
        "tags": ["Angular", "App-bouwer", "Nog niet bestaande tag", "Nog niet bestaande tag #2"],
        "website": "https://www.google.com/",
        "year": 1969,
    }

    response = client.post(
        "/api/v1/companies",
        data=json.dumps(data),
        headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(get_token)},
    )

    result = json.loads(response.get_data(as_text=True))

    assert (
        result["message"]["_schema"][0]
        == "A company already exists with this company_name. Please use the PATCH method if you would like to modify this company or use a different company_name if you would like to add a different company."
    )


def test_post_invalid_company_required_fields(client, get_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to /api/v1/companies with a missing required fields
    THEN check that the response is invalid and particular error messages can be found
    """
    data = {
        "branches": ["Nog niet bestaande branche"],
        "disciplines": [
            "Conceptontwikkeling",
            "Conversie-optimalisatie",
            "Strategie",
            "Nog niet bestaande discipline",
            "Nog niet bestaande discipline #2",
        ],
        "logo_image_src": "https://www.nos.nl/",
        "region": "Remote",
        "tags": ["Angular", "App-bouwer", "Nog niet bestaande tag", "Nog niet bestaande tag #2"],
        "year": 1969,
    }

    response = client.post(
        "/api/v1/companies",
        data=json.dumps(data),
        headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(get_token)},
    )

    result = json.loads(response.get_data(as_text=True))

    assert result["message"]["city_name"][0] == "Missing data for required field."
    assert result["message"]["company_name"][0] == "Missing data for required field."
    assert result["message"]["company_size"][0] == "Missing data for required field."
    assert result["message"]["website"][0] == "Missing data for required field."
