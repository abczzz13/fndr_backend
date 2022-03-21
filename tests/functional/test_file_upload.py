from flask import json
from io import BytesIO


def test_post_valid_user(client, get_token):
    '''
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to /api/v1/register with a valid user
    THEN check that the response is valid and particular data can be found
    '''
    data = {}
    data['file'] = (BytesIO(b"abcdef"), 'test.jpg')

    response = client.post('/api/v1/file_upload', data=data,
                           headers={'Content-Type': 'multipart/form-data', 'Authorization': 'Bearer {}'.format(get_token)},)

    result = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201
    assert result['url'] == "https://fndr.s3.amazonaws.com/test.jpg"
