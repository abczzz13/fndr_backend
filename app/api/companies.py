from flask import jsonify, request, url_for, abort
from flask_login import login_required
from flask_jwt_extended import create_access_token, jwt_required
from app import db, cache
from app.models import Companies, Cities, Meta, companies_meta, Users
from app.api import bp
from sqlalchemy import func
from app.api.errors import bad_request, error_response
# TODO: Looking into errors, validation and bad requests

'''
@bp.route('/companies', methods=['GET'])
def test_get_companies():
    all_companies = Companies.query.all()
    return jsonify([company.to_dict() for company in all_companies])


# What about multiple parameters? Combination of multiple parameters
@bp.route('/query', methods=['GET'])
def test_query():
    # Probably possible to do this more efficient? Join tables?
    if 'city' in request.args:
        city = request.args.get('city')
        city_id = Cities.query.filter_by(city_name=city).first()
        companies = Companies.query.filter_by(city_id=city_id.city_id)
    elif 'size' in request.args:
        size = request.args.get('size')
        companies = Companies.query.filter_by(company_size=size)
    elif 'year' in request.args:
        year = request.args.get('year')
        companies = Companies.query.filter_by(year=year)
    # Probably possible to do this more efficient? Join tables?
    elif 'region' in request.args:
        region = request.args.get('region')
        city_ids = Cities.query.filter_by(region=region)
        companies = []
        for id in city_ids:
            list_companies = Companies.query.filter_by(city_id=id.city_id)
            for company in list_companies:
                companies.append(company)
    else:
        companies = Companies.query.all()
    return jsonify([company.to_dict() for company in companies])


@bp.route('/pagination', methods=['GET'])
def test_pagination():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    companies = Companies.to_collection_dict(
        Companies.query, page, per_page, 'api.test_pagination')
    return jsonify(companies)


@bp.route('/like', methods=['GET'])
def test_like():
    city_like = request.args.get('city_like')
    # result = session.query(Customers).filter(Customers.name.like('Ra%'))
    city_ids = Cities.query.filter(
        Cities.city_name.like('%' + city_like + '%'))
    # city_ids = Cities.query.like(city_name=city_like)
    companies = []
    for id in city_ids:
        list_companies = Companies.query.filter_by(city_id=id.city_id)
        for company in list_companies:
            companies.append(company)
    return jsonify([company.to_dict() for company in companies])
'''


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
    pass


@bp.route('/v1/companies/<int:id>', methods=['GET'])
def get_company(id):
    return jsonify(Companies.query.get_or_404(id).to_dict())


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
            # TODO: implement order by
            pass
        if parameter == 'page':
            page = int(param_dict[parameter])
        if parameter == 'per_page':
            per_page = int(param_dict[parameter])

    # Add pagination
    companies = Companies.to_collection_dict(
        query, page, per_page, 'api.get_companies')
    # TODO:Still need to fix the links in the to_collection_dict method
    # Probably have to use the **kwargs to ...

    return jsonify(companies)


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
    return jsonify(company.to_dict())
    # cache.delete('all_tasks')


@bp.route('/v1/companies/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_company(id):
    company = Companies.query.get_or_404(id)
    db.session.delete(company)
    db.session.commit()
    return f'company_id: {id}'
    # cache.delete('all_tasks')
