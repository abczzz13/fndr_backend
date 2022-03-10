from app.models import Cities
from geocoding_v1 import get_coordinates, update_coordinates_db


def test_get_coordinates(client, insert_data_db):
    '''
    GIVEN a function to call on Google Geolocat API to get the coordinates
    WHEN this functions is called on with the city 'Amsterdam'
    THEN check that the returned coordinates are as expected and are stored in the DB
    '''
    city = 'Amsterdam'
    city_query = Cities.query.filter_by(city_name=city).first()
    coordinates = get_coordinates(city_query.city_name)
    result = update_coordinates_db(city_query, coordinates)
    query_from_db = Cities.query.filter_by(city_name=city).first()

    assert coordinates['lat'] == 52.3675734
    assert coordinates['lng'] == 4.9041389
    assert round(coordinates['lat'], 4) == round(result.city_lat, 4)
    assert round(coordinates['lng'], 4) == round(result.city_lng, 4)
    assert round(coordinates['lat'], 4) == round(query_from_db.city_lat, 4)
    assert round(coordinates['lng'], 4) == round(query_from_db.city_lng, 4)
