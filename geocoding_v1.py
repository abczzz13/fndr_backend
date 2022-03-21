""" This module provides functions to get the lat/lng for cities."""
import os
from app import db, create_app
from app.models import Cities
from app.utils import get_coordinates


def update_coordinates_db(city: dict, coordinates: dict) -> dict:
    """ Update the city record in the DB with the given coordinates.

    Parameters:
    city (object): The city object which will be updated in the DB with the coordinates.
    coordinates (dict): The dictionary with the lat/lng information

    Returns:
    object: The new object with the updated coordinates
    """
    if isinstance(coordinates['lat'], float):
        city.city_lat = coordinates['lat']
    if isinstance(coordinates['lng'], float):
        city.city_lng = coordinates['lng']
    db.session.add(city)
    db.session.commit()
    return city


def geolocate():
    """ Update all the cities in the DB with the related coordinates.

    Parameters:

    Returns:
    """
    print("Start updating all the cities with Latitude/Longtitude information")

    # Iterate over all the cities:
    cities = Cities.query.all()
    for city in cities:
        coordinates = get_coordinates(city.city_name)
        update_coordinates_db(city, coordinates)

    print("Updated all cities with the Latitude/Longtitude information")


def geolocate_update():
    """ Update all the cities in the DB, which do not have any coordinates yet,
        with the related coordinates.

    Parameters:

    Returns:
    """
    print("Start updating all the cities with Latitude/Longtitude information")

    # Iterate over all the cities without prior lat/lng records:
    cities = Cities.query.filter(Cities.city_lat == None).all()
    for city in cities:
        coordinates = get_coordinates(city.city_name)
        update_coordinates_db(city, coordinates)

    print("Updated all cities with the Latitude/Longtitude information")


def main():
    """ Main: Everything that will be run when running this file

    Parameters:

    Returns:
    """
    # Create app
    app = create_app(config_class=os.environ.get('APP_SETTINGS'))
    app.app_context().push()


if __name__ == '__main__':
    main()
