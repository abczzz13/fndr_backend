"""
This module provides the functionality for uploading files to AWS S3
With thanks to Jelmer de Jong (https://github.com/jelmerdejong/simple-flask-s3-uploader)
And Miquel Grinberg (https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask)
"""
import boto3
import imghdr
from config import Config
from flask import jsonify

# s3 = boto3.client('s3')
s3 = boto3.client('s3', aws_access_key_id=Config.AWS_ACCESS_KEY,
                  aws_secret_access_key=Config.AWS_ACCESS_SECRET)


def validate_image(stream):
    """ Returns the file extension by reading the first 512 bytes to validate if the file is indeed an image

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

    return '.' + (format if format != 'jpeg' else 'jpg')


def upload_file_to_s3(file, bucket_name, acl='public-read'):
    """ Uploads the file to AWS S3

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

    return '{}{}'.format(Config.S3_LOCATION, file.filename)


if __name__ == '__main__':
    pass
