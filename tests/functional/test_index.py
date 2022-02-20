def test_index(client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """

    response = client.get("/")
    assert response.status_code == 200
    assert b"<h1>Under Construction</h1>" in response.data
