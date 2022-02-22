from flask import jsonify, request, url_for, abort
from flask_login import login_required
from flask_jwt_extended import create_access_token, jwt_required
from app import db, cache
from app.models import Companies, Cities, Meta, companies_meta, Users
from app.api import bp
from app.api.errors import bad_request, error_response
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


@bp.route('/v1/companies/all', methods=['GET'])
def get_companies_all():
    all_companies = Companies.query.order_by(Companies.company_id.asc()).all()
    return jsonify([company.to_dict() for company in all_companies])


@bp.route('/v1/companies', methods=['GET'])
@cache.cached(timeout=30, query_string=True)
def get_companies():
    # Get the parameters from request
    param_dict = request.args.to_dict()

    # Variables
    page = 1
    per_page = 15
    parameters = ['company', 'company_like', 'city', 'city_id', 'city_like', 'region',
                  'size', 'year', 'page', 'per_page', 'filter_by']
    query = Companies.query.join(Cities)

    # Implement validation?

    # Change the query based on the presence of parameters
    for parameter in param_dict:
        if parameter not in parameters:
            # TODO: What to with errors?
            pass
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
        if parameter == 'tag':
            # TODO: implement filter by meta tags, branches, disciplines
            #
            # query.filter()
            pass
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


@bp.route('/v1/companies/', methods=['POST'])
@jwt_required()
def add_company():
    data = request.get_json() or {}
    if 'company_id' in data:
        return bad_request("Create company cannot include company_id. For modifying existing companies please use the PUT method")
    if 'company_name' not in data:
        # TODO: Check for other required fields?
        return bad_request("Must include company_name field")
    if Companies.query.filter_by(company_name=data['company_name']).first():
        return bad_request("A company with that name already exists, please use another name")
    company = Companies()
    # TODO: Finalize the from_dict method
    company.from_dict(data, new_company=True)
    db.session.add(company)
    db.session.commit()

    response = jsonify(company.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for(
        'api.get_company', id=company.company_id)

    cache.clear()
    return response
    # cache.delete('all_tasks')


@bp.route('/v1/companies/<int:id>', methods=['PUT'])
@jwt_required()
def update_company():
    company = Companies.query.get_or_404(id)
    data = request.get_json() or {}
    # TODO: Validation
    if False:
        return bad_request('false')
    # TODO: Finalize the from_dict method
    company.from_dict(data, new_company=False)
    db.session.commit()
    cache.clear()
    return jsonify(company.to_dict())


@bp.route('/v1/companies/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_company(id):
    company = Companies.query.get_or_404(id)
    db.session.delete(company)
    db.session.commit()
    cache.clear()
    # TODO: Finalize delete route
    return f'company_id: {id}'
    # cache.delete('all_tasks')
