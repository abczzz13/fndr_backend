"""
This module provides all the endpoints for cities API:

GET     /v1/cities       Returns all cities with counts as a list

"""
from app import db, cache
from app.api import bp
from flask import jsonify, request


@bp.route('/v1/cities')
@cache.cached(timeout=30, query_string=True)
def get_cities():
    """GET     /v1/cities       Returns all cities with counts as a list"""

    # Get the parameters from request
    param_dict = request.args.to_dict()

    # Check if city_like parameter is in GET request
    if 'city_like' in param_dict:
        city_like = '%' + param_dict['city_like'] + '%'

        # Raw SQL query to get a selection of cities which fit the city_like parameter
        query = db.session.execute(
            "SELECT cities.city_name, COUNT(cities.city_id) AS city_count FROM COMPANIES JOIN CITIES ON companies.city_id=cities.city_id WHERE lower(cities.city_name) LIKE lower(:city_like) GROUP BY companies.city_id, cities.city_name ORDER BY city_count DESC", {"city_like": city_like})
    else:
        # Raw SQL query to get all cities with company count
        query = db.session.execute(
            "SELECT cities.city_name, COUNT(cities.city_id) AS city_count FROM COMPANIES JOIN CITIES ON companies.city_id=cities.city_id GROUP BY companies.city_id, cities.city_name ORDER BY city_count DESC")

    # Put the query results in a sorted list
    sorted_list = list((x, y) for x, y in query.fetchall())

    return jsonify(sorted_list)
