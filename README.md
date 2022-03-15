## FNDR: Find the nearest IT company looking for you

# Introduction

The idea of the FNDR app is to list all the agencies, working in the ...., who might be looking for junior developers. On this platform you can filter the agencies on mutiple parameters such as location, size, ... and find more details about the agencies that might interest you.

<fndr netlify link>

For this app, I created the backend. By means of an API, the frontend could GET information from the database and adjust the information by POST/PATCH/DELETE.

If you would like to know more about the frontend of the FNDR app, you can take a look over here. <fndr frontend link>

# Table of Contents

# Approach

-   Use version control (GIT) from the start of the project
-   Start working with Pull Requests, <once the project has some substance>
-   Collaboration with issues on Github
-   Use pytest
-   Github Actions
-   Implement CI / CD

# Features

-   API
-   DB migrations
-   Redis Cache
-   Auth with JWT's
-   Validation with Marshmallow
-   Testing with Pytest
-   File upload with AWS S3

# Docs: Using the API

api/v1/companies GET
query parameters:

api/v1/companies/<id> POST
api/v1/companies/<id> PATCH
api/v1/companies/<id> DELETE

api/v1/cities GET
query parameters:

# Docs: Running the project

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
-   REDIS_URL
-   CACHE_DEFAULT_TIMEOUT
-   GOOGLE_API_KEY

# Next steps:

-   Add a Google Maps feature
-   File Upload for logos, using AWS S3
-   Dockerize the project
