""" This module provides custom utility functions for the Flask application."""
import boto3
import imghdr
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from config import Config


# Creating boto3 client for providing access to AWS S3
s3 = boto3.client("s3", aws_access_key_id=Config.AWS_ACCESS_KEY, aws_secret_access_key=Config.AWS_ACCESS_SECRET)


def upload_file_to_s3(file, bucket_name, acl="public-read"):
    """Uploads the file to AWS S3

    Parameters:
    file (object): the file as object that will be uploaded
    bucket_name (str): the bucket in S3 where the file will be saved
    acl (str): access control list of AWS, with default value of 'public-read', which grants everyone READ access

    Returns:
    file location (str): if the file has succesfully been uploaded, else it returns the error message
    """

    try:
        s3.generate_presigned_post(bucket_name, file.filename, ExpiresIn=3600)

    except Exception as e:
        print("Something happened: ", e)
        return e

    return "{}{}".format(Config.S3_LOCATION, file.filename)


def get_coordinates(city: str) -> dict:
    """Get the lat/lng for a city from the Google Maps Geolocate API.

    Parameters:
    city (string): The string for which the API will be queried.

    Returns:
    dict: {'lat': '...', 'lng': '...'}
    """
    params = urllib.parse.urlencode(
        {
            "address": f"{city},+{Config.GEOLOCATE_COUNTRY}",
            "key": Config.GOOGLE_API_KEY,
        }
    )
    url = f"{Config.GEOLOCATE_BASE_URL}?{params}"

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
            if result["status"] == "OK":
                return result["results"][0]["geometry"]["location"]
            elif result["status"] == "ZERO_RESULTS":
                return {"lat": "", "lng": ""}
            elif result["status"] != "UNKNOWN ERROR":
                raise Exception(result["error_message"])

        if current_delay > max_delay:
            raise Exception("Too many retry attempts")

        print("Waiting", current_delay, "seconds before trying")

        time.sleep(current_delay)
        current_delay *= 2


def validate_image(stream):
    """Returns the file extension by reading the first 512 bytes to validate if the file is indeed an image
    * With thanks to Miquel Grinberg (https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask)

    Parameters:
    file (stream): stream of the file

    Returns:
    extension (str): returns file extension
    """
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)

    if not format:
        return None

    return "." + (format if format != "jpeg" else "jpg")


if __name__ == "__main__":
    pass
