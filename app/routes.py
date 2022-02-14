from flask import jsonify
from app import app
from app.models import Companies, Cities, Meta, companies_meta


@app.route("/")
@app.route("/index")
def index():
    return "Under construction"


# Beginning of API
@app.route('/companies', methods=['GET'])
def get_all_companies():
    all_companies = Companies.query.all()
    output = []
    for company in all_companies:
        current_company = {}
        current_company["company_id"] = company.company_id
        current_company["company_name"] = company.company_name
        current_company["logo_image_src"] = company.logo_image_src
        current_company["website"] = company.website
        current_company["year"] = company.year
        current_company["company_size"] = company.company_size.value

        city = Cities.query.filter_by(city_id=company.city_id).first()
        current_company["city_name"] = city.city_name
        current_company["region"] = city.region.value

        current_company['disciplines'] = []
        current_company['branches'] = []
        current_company['tags'] = []

        # TODO: Findout if we can make these queries easier and more performant
        metas = Meta.query.join(Meta.company).filter_by(
            company_id=company.company_id).all()
        for meta in metas:
            query = Meta.query.filter_by(meta_id=meta.meta_id).first()

            if query.type.value == "Discipline":
                current_company['disciplines'].append(query.meta_string)
            if query.type.value == "Branch":
                current_company['branches'].append(query.meta_string)
            if query.type.value == "Tag":
                current_company['tags'].append(query.meta_string)

        output.append(current_company)
    return jsonify(output)


'''
@app.route('/companies/<int:id>', methods=['GET'])
def get_company(id):
    return jsonify(Companies.query.get_or_404(id).to_dict())
    # Need to define the method to_dict in the Companies Class model

@app.route('/companies?cities=<city>', methods=['GET'])
def get_companies_in_city(city):
    # query
    return jsonify( .to_dict())
    # Need to define the method to_dict in the Companies Class model
'''
