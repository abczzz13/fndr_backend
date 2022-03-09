from app import db, create_app
from app.models import Cities
from config import Config, DevelopmentConfig
import json
import time
import urllib.error
import urllib.parse
import urllib.request


# Declaring Variables
country = "Netherlands"
google_api_key = Config.GOOGLE_API_KEY
geolocate_base_url = "https://maps.googleapis.com/maps/api/geocode/json"


def get_coordinates(city):
    params = urllib.parse.urlencode({
        'address': f"{city},+{country}",
        'key': google_api_key,
    })
    url = f"{geolocate_base_url}?{params}"
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
                pass
            elif result['status'] != "UNKNOWN ERROR":
                raise Exception(result['error_message'])

        if current_delay > max_delay:
            raise Exception("Too many retry attempts")

        print('Waiting', current_delay, 'seconds before trying')

        time.sleep(current_delay)
        current_delay *= 2


def update_coordinates_db(city, coordinates):
    if isinstance(coordinates['lat'], float):
        city.city_lat = coordinates['lat']
    if isinstance(coordinates['lng'], float):
        city.city_lng = coordinates['lng']
    db.session.add(city)
    db.session.commit()
    return city


def geolocate():
    print("Start updating all the cities with Latitude/Longtitude information")

    # Iterate over all the cities:
    cities = Cities.query.all()
    for city in cities:
        coordinates = get_coordinates(city.city_name)
        update_coordinates_db(city, coordinates)

    print("Updated all cities with the Latitude/Longtitude information")
    return


def geolocate_update():
    print("Start updating all the cities with Latitude/Longtitude information")

    # Iterate over all the cities without prior lat/lng records:
    cities = Cities.query.filter(Cities.city_lat == None).all()
    for city in cities:
        coordinates = get_coordinates(city.city_name)
        update_coordinates_db(city, coordinates)

    print("Updated all cities with the Latitude/Longtitude information")
    return


def main():
    # Create app
    app = create_app(config_class=DevelopmentConfig)
    app.app_context().push()

    # geolocate()
    # geolocate_update()
    '''
    # Test variables
    city = 'Amsterdam'
    # Test setup
    coordinates = get_coordinates(city)
    # coordinates = {'lat': 52.3675734, 'lng': 4.9041389}
    print(coordinates)
    cls_city = Cities.query.filter_by(city_name=city).first()
    update_db = update_coordinates_db(cls_city, coordinates)
    print(update_db)
    '''


if __name__ == '__main__':
    main()
