"""
This module provides all the error responses
"""
from app import db
from app.errors import bp
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code: int, message=None):
    """Creates a specific error response with specific status_code and message

    Parameters:
    status_code (int): The status_code which will be returned
    message (str): The error message that will be returned

    Returns:
    response: returns response with status_code and message

    """
    payload = {"error": HTTP_STATUS_CODES.get(status_code, "Unknown error")}
    if message:
        payload["message"] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    """Creates a 400 - bad request response with a specific message"""
    return error_response(400, message)


@bp.app_errorhandler(404)
def not_found_error(error):
    """Response 404 Not Found in .json if navigating to not existing URL"""
    return jsonify({"error_code": "404", "message": "Not Found"})


@bp.app_errorhandler(500)
def internal_error(error):
    """Response 500 Internal Server Error if something is not working properly"""
    db.session.rollback()
    jsonify({"error_code": "500", "message": "Internal Server Error"})
