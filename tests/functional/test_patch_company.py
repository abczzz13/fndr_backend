from flask import json


def test_patch_valid_company(client, get_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a PATCH request is made to /api/v1/companies/1 with a valid patch information
    THEN check that the response is valid and particular data can be found
    """
    data = {
        "branches": ["Nog niet bestaande branche", "Nog niet bestaande branche #3"],
        "city_name": "Lutjebroek",
        "company_name": "Test company #1000",
        "company_size": "GT-100",
        "disciplines": ["Nog niet bestaande discipline", "Nog niet bestaande discipline #2"],
        "logo_image_src": "https://www.nos.nl/",
        "tags": ["Nog niet bestaande tag", "Nog niet bestaande tag #2"],
        "website": "https://www.google.com/",
        "year": 1969,
    }

    response = client.patch(
        "/api/v1/companies/1",
        data=json.dumps(data),
        headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(get_token)},
    )

    result = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert result["company_id"] == 1
    assert result["company_name"] == "Test company #1000"
    assert result["city_name"] == "Lutjebroek"
    assert result["region"] == "Remote"
    assert result["company_size"] == "GT-100"
    assert result["branches"][0] == "Nog Niet Bestaande Branche"
    assert result["disciplines"][0] == "Nog Niet Bestaande Discipline"
    assert result["tags"][0] == "Nog Niet Bestaande Tag"
    assert result["website"] == "https://www.google.com/"
    assert result["year"] == 1969


def test_patch_invalid_company_name(client, get_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a PATCH request is made to /api/v1/companies/2 with an already existing company_name
    THEN check that the response is invalid and particular error messages can be found
    """
    # Create dict for invalid patch request with an already existing company_name
    data = {"company_name": "H1 Webdevelopment"}

    response = client.patch(
        "/api/v1/companies/2",
        data=json.dumps(data),
        headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(get_token)},
    )

    result = json.loads(response.get_data(as_text=True))

    assert (
        result["message"]["_schema"][0]
        == "A company already exists with this company_name. Please use a different company_name."
    )


def test_patch_invalid_company_fields(client, get_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a PATCH request is made to /api/v1/companies/2 with a company_id and region field
    THEN check that the response is invalid and particular error messages can be found
    """
    data = {"region": "Friesland", "company_id": 22}

    response = client.patch(
        "/api/v1/companies/2",
        data=json.dumps(data),
        headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(get_token)},
    )

    result = json.loads(response.get_data(as_text=True))

    assert result["message"]["region"][0] == "Unknown field."
    assert result["message"]["company_id"][0] == "Unknown field."


def test_patch_company_name_unchanged(client, get_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a PATCH request is made to /api/v1/companies/2 with an unchanged company_name field and valid other field
    THEN check that the response is valid and specific data can be found
    """
    data = {"company_name": "Test company #1000", "year": 2000}

    response = client.patch(
        "/api/v1/companies/1",
        data=json.dumps(data),
        headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(get_token)},
    )

    result = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert result["company_id"] == 1
    assert result["company_name"] == "Test company #1000"
    assert result["year"] == 2000
