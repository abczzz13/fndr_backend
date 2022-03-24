# FNDR: Find the nearest IT company looking for you

## Introduction

The idea of the FNDR app is to list all the agencies, who might be looking for junior developers. On this platform you can filter the agencies on mutiple parameters such as location, size, etc. and find more details about the agencies that might interest you.

[Here you can find a working version of the app](https://fndr.netlify.app/)

For this app, I created the backend in Flask. By means of an API, the frontend could GET information from the PostgresSQL database and adjust the information by POST/PATCH/DELETE.

If you would like to know more about the frontend of the FNDR app, you can take a look over [here](https://github.com/jodelajo/fndr).

## Table of Contents

* [Approach](#Approach)
* [Features](#Features)
* [Docs: Using the API](#API)
* [Docs: Running the project](#Running)
* [Next steps](#Next)
* [Credits](#Credits)


## Approach

-   Use version control (GIT) from the start of the project
-   Start working with Pull Requests, after the initial setup phase
-   Collaboration with issues on Github
-   Use pytest
-   Github Actions
-   Implement CI / CD Pipeline on Heroku

## Features

-   RESTful API
-   DB migrations with Alembic
-   Redis Cache
-   Auth with JWT's
-   Validation with Marshmallow
-   Testing with Pytest
-   File upload with AWS S3

## Docs: Using the API<a name="API"></a>

You can find the documentation for API below:
[![Overview of the API endpoints](https://fndr.s3.eu-central-1.amazonaws.com/API.png)](https://app.swaggerhub.com/apis-docs/thomas30/FNDRbackend/1.0.0#/)

## Docs: Running the project<a name="running"></a>

The app was setup using a virtual environment with python 3.10. The dependencies can be found in requirements.txt.

Run the following commands to setup the virtual environment and install all the dependecies.

-   pip install virtualenv
-   python -m venv venv
-   source venv/bin/activate
-   pip install -r requirements.txt

To run this project locally, you will be need to following enviroment variables:

-   FLASK_APP
-   FLASK_ENV
-   APP_SETTINGS
-   SECRET_KEY
-   JWT_SECRET_KEY
-   POSTGRES_USER
-   POSTGRES_PW
-   POSTGRES_DB
-   POSTGRES_URL
-   TEST_POSTGRES_USER
-   TEST_POSTGRES_PW
-   TEST_POSTGRES_DB
-   TEST_POSTGRES_URL
-   CACHE_TYPE
-   CACHE_REDIS_HOST
-   CACHE_REDIS_PORT
-   CACHE_REDIS_DB
-   CACHE_DEFAULT_TIMEOUT
-   REDIS_URL
-   GOOGLE_API_KEY

## Next steps:<a name="next"></a>

-   Add a Google Maps feature
-   File Upload for logos, using AWS S3
-   Dockerize the project

## Credits:

I would like to thank Joanneke and Daria for their extensive work on the frontend. And of course, Rein, for all the feedback, guidance and help during this project.
