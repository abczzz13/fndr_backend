from app.models import Cities
from app.utils import get_coordinates


def test_get_coordinates(client, insert_data_db):
    """
    GIVEN a function to call on Google Geolocat API to get the coordinates
    WHEN this functions is called on with the city 'Amsterdam'
    THEN check that the returned coordinates are as expected and are stored in the DB
    """
    city = "Amsterdam"
    coordinates = get_coordinates(city)

    query = Cities.query.filter_by(city_name=city).first()

    assert coordinates["lat"] == 52.3675734
    assert coordinates["lng"] == 4.9041389
    assert round(coordinates["lat"], 4) == round(query.city_lat, 4)
    assert round(coordinates["lng"], 4) == round(query.city_lng, 4)
