from flask import json


def test_post_valid_company(client, get_token):
    '''
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to /api/v1/companies with a valid company
    THEN check that the response is valid and particular data can be found
    '''
    data = {
        "branches": [
            "Nog niet bestaande branche"
        ],
        "city_name": "Lutjebroek",
        "company_name": "Test company #999",
        "company_size": "11-50",
        "disciplines": [
            "Conceptontwikkeling",
            "Conversie-optimalisatie",
            "Strategie",
            "Nog niet bestaande discipline",
            "Nog niet bestaande discipline #2"
        ],
        "logo_image_src": "https://www.nos.nl/",
        "region": "Remote",
        "tags": [
            "Angular",
            "App-bouwer",
            "Nog niet bestaande tag",
            "Nog niet bestaande tag #2"
        ],
        "website": "https://www.google.com/",
        "year": 1969
    }

    response = client.post('/api/v1/companies', data=json.dumps(data),
                           headers={'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(get_token)},)

    result = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201
    assert result['company_id'] == 1
    assert result['company_name'] == 'Test company #999'
    assert result['city_name'] == 'Lutjebroek'
    assert result['region'] == 'Remote'
    assert result['company_size'] == '11-50'
    assert result['branches'][0] == 'Nog niet bestaande branche'
    assert result['website'] == 'https://www.google.com/'
    assert result['year'] == 1969


def test_post_invalid_company(client, insert_data_db, get_token):
    '''
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to /api/v1/companies with a invalid company
    THEN check that the response is invalid and particular error messages can be found
    '''
    data = {
        "branches": [
            "Nog niet bestaande branche"
        ],
        "city_name": "Lutjebroek",
        "company_name": "Test company #999",
        "company_size": "11-50",
        "disciplines": [
            "Conceptontwikkeling",
            "Conversie-optimalisatie",
            "Strategie",
            "Nog niet bestaande discipline",
            "Nog niet bestaande discipline #2"
        ],
        "logo_image_src": "https://www.nos.nl/",
        "region": "Remote",
        "tags": [
            "Angular",
            "App-bouwer",
            "Nog niet bestaande tag",
            "Nog niet bestaande tag #2"
        ],
        "website": "https://www.google.com/",
        "year": 1969
    }

    # Create dictionary with invalid company including company_id
    data1 = data.copy()
    data1['company_id'] = 21

    response1 = client.post('/api/v1/companies', data=json.dumps(data1),
                            headers={'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(get_token)},)
    result1 = json.loads(response1.get_data(as_text=True))

    # Create dictionary with invalid company with company_name already in DB
    data2 = data.copy()
    data2['company_name'] = 'daily dialogues (Part of CANDID)'

    response2 = client.post('/api/v1/companies', data=json.dumps(data2),
                            headers={'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(get_token)},)
    result2 = json.loads(response2.get_data(as_text=True))

    # Create dictionary with invalid company missing required fields:
    data3 = data.copy()
    for x in ['company_size', 'website', 'company_name', 'city_name']:
        data3.pop(x)

    response3 = client.post('/api/v1/companies', data=json.dumps(data3),
                            headers={'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(get_token)},)
    result3 = json.loads(response3.get_data(as_text=True))

    assert result1['message']['_schema'][0] == "Create new company cannot include company_id. For modifying existing companies please use the PATCH method"
    assert result2['message']['_schema'][0] == "A company already exists with this company_name. Please use the PATCH method if you would like to modify this company or use a different company_name if you would like to add a different company."
    assert result3['message']['city_name'][0] == "Missing data for required field."
    assert result3['message']['company_name'][0] == "Missing data for required field."
    assert result3['message']['company_size'][0] == "Missing data for required field."
    assert result3['message']['website'][0] == "Missing data for required field."