from flask import jsonify, request, url_for, abort
from app import db
from app.models import Companies, Cities, Meta, companies_meta
from app.api import bp
# from app.api.errors import bad_request


@bp.route('/companies/<int:id>', methods=['GET'])
def get_company(id):
    company = Companies.query.filter_by(company_id=id).first()
    # company = Companies.query.get_or_404(company_id=id)
    current_company = {}
    current_company["company_id"] = company.company_id
    current_company["company_name"] = company.company_name
    current_company["logo_image_src"] = company.logo_image_src
    current_company["website"] = company.website
    current_company["year"] = company.year
    current_company["company_size"] = company.company_size.value
    current_company["city_name"] = company.city.city_name
    current_company["region"] = company.city.region.value

    current_company['disciplines'] = []
    current_company['branches'] = []
    current_company['tags'] = []

    metas = Meta.query.join(Meta.company).filter_by(
        company_id=company.company_id).all()

    for meta in metas:
        if meta.type.value == "Discipline":
            current_company['disciplines'].append(meta.meta_string)
        if meta.type.value == "Branch":
            current_company['branches'].append(meta.meta_string)
        if meta.type.value == "Tag":
            current_company['tags'].append(meta.meta_string)

    return jsonify(current_company)
