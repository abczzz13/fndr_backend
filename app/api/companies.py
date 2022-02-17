from flask import jsonify, request, url_for, abort
from app import db
from app.models import Companies, Cities, Meta, companies_meta
from app.api import bp
# from app.api.errors import bad_request


@bp.route('/companies', methods=['GET'])
def get_companies():
    all_companies = Companies.query.all()
    output = []
    for company in all_companies:
        output.append(company.to_dict())
    return jsonify(output)


@bp.route('/companies/<int:id>', methods=['GET'])
def get_company_test(id):
    return jsonify(Companies.query.get_or_404(id).to_dict())
