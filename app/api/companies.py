from flask import jsonify, request, url_for, abort
from app import db
from app.models import Companies, Cities, Meta, companies_meta
from app.api import bp
# from app.api.errors import bad_request
# TODO: Looking into errors, validation and bad requests


@bp.route('/companies', methods=['GET'])
def get_companies():
    all_companies = Companies.query.all()
    return jsonify([company.to_dict() for company in all_companies])


@bp.route('/companies/<int:id>', methods=['GET'])
def get_company_test(id):
    return jsonify(Companies.query.get_or_404(id).to_dict())


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


@bp.route('pagination', methods=['GET'])
def test_pagination():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    companies = Companies.to_collection_dict(
        Companies.query, page, per_page, 'api.test_pagination')
    return jsonify(companies)


@bp.route('like', methods=['GET'])
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
