"""
This module provides all the endpoints for companies API:

GET     /v1/companies       Returns all companies, multiple query parameters can be used
POST    /v1/companies       Creates a new company
GET     /v1/companies/:id   Returns company with specific company_id
PATCH   /v1/companies/:id   Updates company with specific company_id
DELETE  /v1/companies/:id   Deletes company with specific company_id

"""
from app import db, cache
from app.api import bp
from app.errors.handlers import bad_request, error_response
from app.models import Companies, Cities, Meta, companies_meta, CompaniesValidationSchema, CompaniesPatchSchema
from app.import_data_v2 import insert_meta, insert_city
from flask import jsonify, request, url_for
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError


@bp.route('/v1/companies', methods=['GET'])
@cache.cached(timeout=30, query_string=True)
def get_companies():
    """GET     /v1/companies       Returns all companies, multiple query parameters can be used"""
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
        query.order_by(Companies.company_id.asc()),
        page, per_page, 'api.get_companies')

    return jsonify(companies)


@bp.route('/v1/companies', methods=['POST'])
@jwt_required()
def add_company():
    """POST    /v1/companies       Creates a new company"""
    data = request.get_json() or {}

    # Validate input
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


@bp.route('/v1/companies/<int:company_id>', methods=['GET'])
@cache.cached(timeout=30, query_string=True)
def get_company(company_id):
    """GET     /v1/companies/:id   Returns company with specific company_id"""
    return jsonify(Companies.query.get_or_404(company_id).to_dict())


@bp.route('/v1/companies/<int:company_id>', methods=['PATCH'])
@jwt_required()
def update_company(company_id):
    """PATCH   /v1/companies/:id   Updates company with specific company_id"""
    company = Companies.query.get_or_404(company_id)

    data = request.get_json() or {}
    data['id_for_check_company'] = company.company_id

    # Validate input
    try:
        validated_data = CompaniesPatchSchema().load(data, partial=True)
    except ValidationError as err:
        return bad_request(err.messages)

    # Make the update in the DB for city and meta infor
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
                db.session.execute(
                    "DELETE FROM companies_meta \
                        WHERE companies_meta.company_id = :id \
                            AND companies_meta.meta_id IN (SELECT Meta.meta_id \
                                FROM Meta WHERE Meta.type = :type)",
                    {"id": company_id, "type": field})

                # Adds the meta data:
                insert_meta(validated_data[field], field, company_id)
                validated_data.pop(field)

    # Make the update in the DB for the other fields
    for field in validated_data:
        setattr(company, field, validated_data[field])
    db.session.commit()

    # Create response
    response = jsonify(company.to_dict())
    response.status_code = 200
    response.headers['Location'] = url_for('api.get_company', id=id)

    cache.clear()
    return response


@bp.route('/v1/companies/<int:company_id>', methods=['DELETE'])
@jwt_required()
def delete_company(company_id):
    """DELETE  /v1/companies/:id   Deletes company with specific company_id"""
    # Lookup company_id and delete if exists
    company = Companies.query.get_or_404(company_id)
    db.session.delete(company)
    db.session.commit()

    # Create response
    message = {}
    message['message'] = f"Company with company_id={company_id} has been deleted"
    response = jsonify(message)
    response.status_code = 200

    cache.clear()
    return response
