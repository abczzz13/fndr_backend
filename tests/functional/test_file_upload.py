from flask import json
from io import BytesIO


def test_upload_valid_file(client, get_token):
    '''
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to /api/v1/upload with a valid image
    THEN check that the response is valid and particular data can be found
    '''
    data = {}
    data['file'] = (BytesIO(b"abcdef"), 'test.jpg')

    response = client.post('/api/v1/file_upload', data=data,
                           headers={'Content-Type': 'multipart/form-data', 'Authorization': 'Bearer {}'.format(get_token)},)

    result = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201
    assert result['url'] == "https://fndr.s3.amazonaws.com/test.jpg"


def test_upload_no_file(client, get_token):
    '''
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to /api/v1/upload without a file selected
    THEN check that the response is valid and particular data can be found
    '''
    data = {}

    response = client.post('/api/v1/file_upload', data=data,
                           headers={'Content-Type': 'multipart/form-data', 'Authorization': 'Bearer {}'.format(get_token)},)

    result = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert result['message'] == "No file key in request.files"


def test_upload_no_file_selected(client, get_token):
    '''
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to /api/v1/upload without a file selected
    THEN check that the response is valid and particular data can be found
    '''
    data = {'file': ''}

    response = client.post('/api/v1/file_upload', data=data,
                           headers={'Content-Type': 'multipart/form-data', 'Authorization': 'Bearer {}'.format(get_token)},)

    result = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert result['message'] == "Please select a file"


def test_upload_no_image(client, get_token):
    '''
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to /api/v1/upload without a file selected
    THEN check that the response is valid and particular data can be found
    '''
    data = {}
    data['file'] = (BytesIO(b"abcdef"), 'test.txt')

    response = client.post('/api/v1/file_upload', data=data,
                           headers={'Content-Type': 'multipart/form-data', 'Authorization': 'Bearer {}'.format(get_token)},)

    result = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert result['message'] == "Invalid file extension, please use ..."
