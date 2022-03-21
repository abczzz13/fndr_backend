
import os
from app import db, cache, jwt
from app.api import bp
from app.api.errors import bad_request, error_response
from app.models import Companies, Cities, Meta, companies_meta, Users, CompaniesValidationSchema, CompaniesPatchSchema, NewAdminSchema
from app.import_data_v2 import insert_meta, insert_city
from app.upload import upload_file_to_s3, validate_image
from config import Config
from flask import jsonify, request, url_for
from flask_jwt_extended import create_access_token, jwt_required, current_user
from marshmallow import ValidationError
from werkzeug.utils import secure_filename


# TODO: Looking into errors, validation and bad requests


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Users.query.filter_by(id=identity).one_or_none()


@bp.route('/v1/token', methods=['POST'])
def create_token():
    # Get User credentials from POST
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Lookup user from DB and check credentials, return error if not valid
    user = Users.query.filter_by(username=username).one_or_none()
    if not user or not user.check_password(password):
        return error_response(401, "Invalid user credentials")

    # Create and return token if credentials are valid
    access_token = create_access_token(identity=user)
    return jsonify({'token': access_token, 'user_id': user.id, 'username': user.username})


@bp.route('v1/token', methods=['DELETE'])
@jwt_required()
def revoke_token():
    # TODO: Revoke token
    pass


@bp.route("v1/check_token", methods=["GET"])
@jwt_required()
def check_token():

    return jsonify(
        id=current_user.id,
        username=current_user.username,
    )


@bp.route('v1/register', methods=['POST'])
@jwt_required()
def register_admin():
    data = request.get_json() or {}

    try:
        validated_data = NewAdminSchema().load(data)
    except ValidationError as err:
        return bad_request(err.messages)

    new_admin = Users(
        username=validated_data['username'], email=validated_data['email'])
    new_admin.set_password(validated_data['password'])

    db.session.add(new_admin)
    db.session.commit()

    response = jsonify(new_admin.to_dict())
    response.status_code = 201

    return response


@bp.route('/v1/cities')
def get_cities():

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


@ bp.route('/v1/companies/all', methods=['GET'])
def get_companies_all():
    all_companies = Companies.query.order_by(Companies.company_id.asc()).all()
    return jsonify([company.to_dict() for company in all_companies])


@ bp.route('/v1/companies', methods=['GET'])
@ cache.cached(timeout=30, query_string=True)
def get_companies():
    # Get the parameters from request
    param_dict = request.args.to_dict()

    # Variables
    query = Companies.query.join(Cities)
    parameters = ['company', 'company_like', 'city', 'city_id', 'city_like', 'region',
                  'size', 'year', 'tag', 'branch', 'discipline', 'filter_by', 'page', 'per_page']

    # Iterate through all the parameters and adjust the query based on the parameters
    for parameter in param_dict:
        # Return error 400 if a unkown parameter has been found
        if parameter not in parameters:
            return error_response(400, "The parameter(s) you have used are unknown. Please use one or multiple of the following parameters: {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}".format(*parameters))
        if parameter == 'company':
            query = query.filter(Companies.company_name ==
                                 param_dict[parameter])
        if parameter == 'company_like':
            query = query.filter(Companies.company_name.ilike(
                '%' + param_dict[parameter] + '%'))
        if parameter == 'city':
            query = query.filter(Cities.city_name == param_dict[parameter])
        if parameter == 'city_id':
            query = query.filter(Cities.city_id == param_dict[parameter])
        if parameter == 'city_like':
            query = query.filter(Cities.city_name.ilike(
                '%' + param_dict[parameter] + '%'))
        if parameter == 'region':
            query = query.filter(Cities.region == param_dict[parameter])
        if parameter == 'size':
            query = query.filter(Companies.company_size ==
                                 str(param_dict[parameter]))
        if parameter == 'year':
            query = query.filter(Companies.year ==
                                 param_dict[parameter])
        if parameter == 'discipline':
            query = query.join(companies_meta).join(Meta).filter(Meta.type == 'disciplines').filter(
                Meta.meta_string.ilike(param_dict[parameter]))
        if parameter == 'branch':
            query = query.join(companies_meta).join(Meta).filter(Meta.type == 'branches').filter(
                Meta.meta_string.ilike(param_dict[parameter]))
        if parameter == 'tag':
            query = query.join(companies_meta).join(Meta).filter(Meta.type == "tags").filter(
                Meta.meta_string.ilike(param_dict[parameter]))
        if parameter == 'order_by':
            # query = query.order_by(....asc())
            # TODO: implement order by
            pass

    # Default values for pagination
    page = 1
    per_page = 15

    # Extract user specified pagination
    if 'page' in param_dict:
        page = int(param_dict.pop('page'))
    if 'per_page' in param_dict:
        per_page = int(param_dict.pop('per_page'))

    # Create dictionary output, including pagination and meta info
    companies = Companies.to_collection_dict(
        query.order_by(Companies.company_id.asc()), page, per_page, 'api.get_companies', param_dict)

    return jsonify(companies)


@bp.route('/v1/companies/<int:id>', methods=['GET'])
def get_company(id):
    return jsonify(Companies.query.get_or_404(id).to_dict())


@bp.route('/v1/companies', methods=['POST'])
@jwt_required()
def add_company():
    data = request.get_json() or {}

    try:
        validated_data = CompaniesValidationSchema().load(data)
    except ValidationError as err:
        return bad_request(err.messages)

    # Check if city is already in DB:
    city = Cities()
    validated_data['city_id'] = city.get_or_create(validated_data)

    # Create new company
    new_company = Companies()
    fields = ['company_name', 'logo_image_src',
              'website', 'year', 'company_size', 'city_id']
    for field in fields:
        if field in validated_data:
            setattr(new_company, field, validated_data[field])

    db.session.add(new_company)
    db.session.commit()

    # Insert Meta Data:
    meta = ['disciplines', 'branches', 'tags']
    for field in meta:
        if field in validated_data:
            insert_meta(validated_data[field], field, new_company.company_id)

    # Create response
    response = jsonify(new_company.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for(
        'api.get_company', id=new_company.company_id)

    cache.clear()
    return response


@bp.route('/v1/companies/<int:id>', methods=['PATCH'])
@jwt_required()
def update_company(id):
    company = Companies.query.get_or_404(id)

    data = request.get_json() or {}

    try:
        validated_data = CompaniesPatchSchema().load(data, partial=True)
    except ValidationError as err:
        return bad_request(err.messages)

    fields_in_related_tables = ['city_name', 'disciplines', 'branches', 'tags']
    for field in fields_in_related_tables:
        if field in validated_data:
            if field == 'city_name':
                city_dict = insert_city(validated_data)
                validated_data['city_id'] = city_dict['city_id']
                validated_data.pop('city_name')
            if field in ['disciplines', 'branches', 'tags']:
                # TODO: Only removes the records from the companies_meta table, not the actual records in the Meta table (as these could still be in use by other companies)
                # RAW SQL statement for finding orphaned meta records: "SELECT * FROM Meta WHERE meta_id NOT IN (SELECT meta_id FROM companies_meta);"
                db.session.execute("DELETE FROM companies_meta WHERE companies_meta.company_id = :id AND companies_meta.meta_id IN (SELECT Meta.meta_id FROM Meta WHERE Meta.type = :type)", {
                                   "id": id, "type": field})

                # Adds the meta data:
                insert_meta(validated_data[field], field, id)
                validated_data.pop(field)

    # Make the update in the DB
    for field in validated_data:
        setattr(company, field, validated_data[field])
    db.session.commit()

    # Create response
    response = jsonify(company.to_dict())
    response.status_code = 200
    response.headers['Location'] = url_for('api.get_company', id=id)

    cache.clear()
    return response


@bp.route('/v1/companies/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_company(id):
    company = Companies.query.get_or_404(id)
    db.session.delete(company)
    db.session.commit()

    message = {}
    message['message'] = f"Company with company_id={id} has been deleted"

    response = jsonify(message)
    response.status_code = 200

    cache.clear()
    return response


@bp.route('/v1/upload', methods=['POST'])
@jwt_required()
def upload_file():
    if 'file' not in request.files:
        return error_response(400, "No file key in request.files")

    img = request.files['file']
    if img.filename == "":
        return error_response(400, "Please select a file")

    filename = secure_filename(img.filename)
    file_ext = os.path.splitext(filename)[1]

    if file_ext not in Config.UPLOAD_EXTENSIONS or file_ext != validate_image(img.stream):
        return error_response(400, f"Invalid file extension, please use {Config.UPLOAD_EXTENSIONS}")

    output = {}
    output['url'] = str(upload_file_to_s3(img, Config.S3_BUCKET_NAME))

    response = jsonify(output)
    response.status_code = 201

    return response

    # TODO: We could also think about nameing the file ourselves...
    # uploaded_file.save(os.path.join('static/avatars', current_user.get_id()))
    # something like <company_id>_logo_<company_name>

    # Additionally, it overrides files with the same name already in the bucket
