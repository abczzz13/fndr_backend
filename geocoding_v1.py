""" This module provides functions to get the lat/lng for cities."""
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from app import db, create_app
from app.models import Cities
from config import Config, DevelopmentConfig


# Declaring Variables
COUNTRY = "Netherlands"
GOOGLE_API_KEY = Config.GOOGLE_API_KEY
GEOLOCATE_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"


def get_coordinates(city):
    """ Get the lat/lng for a city from the Google Maps Geolocate API.

    Parameters:
    city (string): The string for which the API will be queried.

    Returns:
    dict: {'lat': '...', 'lng': '...'}
    """
    params = urllib.parse.urlencode({
        'address': f"{city},+{COUNTRY}",
        'key': GOOGLE_API_KEY,
    })
    url = f"{GEOLOCATE_BASE_URL}?{params}"
    print(url)
    current_delay = 0.1
    max_delay = 5

    while True:
        try:
            # Get the API response:
            response = urllib.request.urlopen(url)
        except urllib.error.URLError:
            pass
        else:
            result = json.load(response)
            print(result)
            if result['status'] == "OK":
                return result['results'][0]['geometry']['location']
            elif result['status'] == "ZERO_RESULTS":
                return {'lat': '', 'lng': ''}
            elif result['status'] != "UNKNOWN ERROR":
                raise Exception(result['error_message'])

        if current_delay > max_delay:
            raise Exception("Too many retry attempts")

        print('Waiting', current_delay, 'seconds before trying')

        time.sleep(current_delay)
        current_delay *= 2


def update_coordinates_db(city, coordinates):
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
    app = create_app(config_class=DevelopmentConfig)
    app.app_context().push()

    # geolocate()
    # geolocate_update()


if __name__ == '__main__':
    main()
