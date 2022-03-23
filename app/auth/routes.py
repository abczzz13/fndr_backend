"""
This module provides all the endpoints for cities API:

POST    /token          Creates token if valid credentials
DELETE  /token          Revokes token (not implemented yet)     
GET     /check_token    Returns id/username of logged-in user
POST    /register       Creates new user

"""
from app import db
from app.errors.handlers import bad_request, error_response
from app.auth import bp
from app.models import Users, NewAdminSchema
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, current_user
from marshmallow import ValidationError


@bp.route('token', methods=['POST'])
def create_token():
    """POST    /token          Creates token if valid credentials"""
    # Get User credentials from POST
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Lookup user in DB and check credentials, return error if not valid
    user = Users.query.filter_by(username=username).one_or_none()
    if not user or not user.check_password(password):
        return error_response(401, "Invalid user credentials")

    # Create and return token if credentials are valid
    access_token = create_access_token(identity=user)
    return jsonify({'token': access_token, 'user_id': user.id, 'username': user.username})


@bp.route('token', methods=['DELETE'])
@jwt_required()
def revoke_token():
    """DELETE  /token          Revokes token (not implemented yet) """
    # TODO: Revoke token
    pass


@bp.route("check_token", methods=["GET"])
@jwt_required()
def check_token():
    """GET     /check_token    Returns id/username of logged-in user"""
    return jsonify(
        id=current_user.id,
        username=current_user.username)


@bp.route('register', methods=['POST'])
@jwt_required()
def register_admin():
    """POST    /register       Creates new user"""
    data = request.get_json() or {}

    # Validate submitted data
    try:
        validated_data = NewAdminSchema().load(data)
    except ValidationError as err:
        return bad_request(err.messages)

    # Make a new user
    new_admin = Users(
        username=validated_data['username'],
        email=validated_data['email'])
    new_admin.set_password(validated_data['password'])

    # Update DB
    db.session.add(new_admin)
    db.session.commit()

    # Prepare response
    response = jsonify(new_admin.to_dict())
    response.status_code = 201

    return response


if __name__ == "__main__":
    pass
