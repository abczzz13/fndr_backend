from app import db, cache
from app.api import bp
from app.api.errors import bad_request, error_response
from app.models import Companies, Cities, Meta, companies_meta, Users, CompaniesValidationSchema, CompaniesPatchSchema
from app.import_data_v2 import insert_meta, insert_city
from flask import jsonify, request, url_for
from flask_jwt_extended import create_access_token, jwt_required
from marshmallow import ValidationError


# TODO: Looking into errors, validation and bad requests


@bp.route('/v1/token', methods=['POST'])
def create_token():
    # Get User credentials from POST
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Lookup user from DB and check credentials, return error if not valid
    user = Users.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return error_response(401, "Invalid user credentials")

    # Create and return token if credentials are valid
    access_token = create_access_token(identity=user.id)
    return jsonify({'token': access_token, 'user_id': user.id})


@bp.route('v1/token', methods=['DELETE'])
@jwt_required()
def revoke_token():
    # TODO: Revoke token
    pass


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
    page = 1
    per_page = 15
    parameters = ['company', 'company_like', 'city', 'city_id', 'city_like', 'region',
                  'size', 'year', 'tag', 'branch', 'discipline', 'page', 'per_page', 'filter_by']
    query = Companies.query.join(Cities)

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
        if parameter == 'page':
            page = int(param_dict[parameter])
        if parameter == 'per_page':
            per_page = int(param_dict[parameter])

    # Add pagination
    companies = Companies.to_collection_dict(
        query.order_by(Companies.company_id.asc()), page, per_page, 'api.get_companies')
    # TODO:Still need to fix the links in the to_collection_dict method
    # Probably have to use the **kwargs to ...

    return jsonify(companies)


@bp.route('/v1/companies/<int:id>', methods=['GET'])
def get_company(id):
    return jsonify(Companies.query.get_or_404(id).to_dict())


@bp.route('/v1/companies', methods=['POST'])
@jwt_required()
def add_company():
    data = request.get_json() or {}

    try:
        result = CompaniesValidationSchema().load(data)
    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        return bad_request(err.messages)

    # TODO: Validate if company name is already in DB?

    new_company = Companies(company_name=result['company_name'], logo_image_src=result['logo_image_src'],
                            website=result['website'], year=result['year'], company_size=result['company_size'])

    # Check if city is already in DB:
    city = Cities.query.filter_by(
        city_name=result['city_name'].title()).first()
    if city is not None:
        new_company.city_id = city.city_id
        db.session.add(new_company)
        db.session.commit()
    else:
        new_city = Cities(
            city_name=result['city_name'].title(), region=result['region'])
        new_city.company.append(new_company)
        db.session.add(new_city)
        db.session.commit()

    # Insert Meta Data:
    insert_meta(result['disciplines'], 'disciplines', new_company.company_id)
    insert_meta(result['branches'], 'branches', new_company.company_id)
    insert_meta(result['tags'], 'tags', new_company.company_id)

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
