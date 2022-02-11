from flask import jsonify
from app import app
# from models import Companies


@app.route("/")
@app.route("/index")
def index():
    return "Under construction"


# Beginning of API
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
