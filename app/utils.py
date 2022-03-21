""" This module provides custom utility functions for the Flask application."""
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from config import Config


def get_coordinates(city: str) -> dict:
    """ Get the lat/lng for a city from the Google Maps Geolocate API.

    Parameters:
    city (string): The string for which the API will be queried.

    Returns:
    dict: {'lat': '...', 'lng': '...'}
    """
    params = urllib.parse.urlencode({
        'address': f"{city},+{Config.GEOLOCATE_COUNTRY}",
        'key': Config.GOOGLE_API_KEY,
    })
    url = f"{Config.GEOLOCATE_BASE_URL}?{params}"
    print(url)
    current_delay = 0.1
    max_delay = 5

    # Maybe look into using the request libary? As we have been doin with the testing
    # https://www.nylas.com/blog/use-python-requests-module-rest-apis/

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
