"""
This module provides all the endpoints for companies API:

GET     /v1/companies       Returns all companies, multiple query parameters can be used
POST    /v1/companies       Creates a new company
GET     /v1/companies/:id   Returns company with specific company_id
PATCH   /v1/companies/:id   Updates company with specific company_id
DELETE  /v1/companies/:id   Deletes company with specific company_id

"""
import os
from app import db, cache
from app.api import bp
from app.errors.handlers import bad_request, error_response
from app.models import Companies, Cities, Meta, companies_meta, CompaniesValidationSchema, CompaniesPatchSchema
from app.import_data_v2 import insert_meta, insert_city
from app.utils import upload_file_to_s3, validate_image
from config import Config
from flask import jsonify, request, url_for
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from werkzeug.utils import secure_filename


@bp.route("/v1/companies", methods=["GET"])
@cache.cached(timeout=30, query_string=True)
def get_companies():
    """GET     /v1/companies       Returns all companies, multiple query parameters can be used"""

    # Preparing the dict with all key/values from the request
    request_dict = request.args.to_dict()

    # Variables
    page = int(request_dict.pop("page", 1))
    per_page = int(request_dict.pop("per_page", 15))
    parameters = [
        "company_name",
        "company_like",
        "city_name",
        "city_id",
        "city_like",
        "region",
        "company_size",
        "year",
        "tags",
        "branches",
        "disciplines",
        "page",
        "per_page",
    ]
    meta = ["tags", "branches", "disciplines"]
    query = Companies.query.join(Cities)

    # Iterate over the query parameters and adjust query accordingly
    for key in request_dict:
        if key not in parameters:
            string = (
                "The parameter(s) you have used are unknown. Please use one or multiple of the following parameters: "
            )
            first = True
            for parameter in parameters:
                if first:
                    string += f"{parameter}"
                    first = False
                else:
                    string += f", {parameter}"
            return error_response(400, string)
        if hasattr(Companies, key) and key != "city_name":
            query = query.filter(getattr(Companies, key) == request_dict[key])
        if hasattr(Cities, key):
            query = query.filter(getattr(Cities, key) == request_dict[key])
        if key == "company_like":
            query = query.filter(Companies.company_name.ilike("%" + request_dict[key] + "%"))
        if key == "city_like":
            query = query.filter(Cities.city_name.ilike("%" + request_dict[key] + "%"))
        if key in meta:
            query = (
                query.join(companies_meta)
                .join(Meta)
                .filter(Meta.type == key)
                .filter(Meta.meta_string.ilike("%" + request_dict[key] + "%"))
            )

    # Create dictionary output, including pagination and meta info
    companies = Companies.to_collection_dict(
        query.order_by(Companies.company_id.asc()), page, per_page, "api.get_companies"
    )

    return jsonify(companies)


@bp.route("/v1/companies", methods=["POST"])
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
    validated_data["city_id"] = city.get_or_create(validated_data)

    # Create new company
    new_company = Companies()
    fields = ["company_name", "logo_image_src", "website", "year", "company_size", "city_id"]
    for field in fields:
        if field in validated_data:
            setattr(new_company, field, validated_data[field])

    db.session.add(new_company)
    db.session.commit()

    # Insert Meta Data:
    meta = ["disciplines", "branches", "tags"]
    for field in meta:
        if field in validated_data:
            insert_meta(validated_data[field], field, new_company.company_id)

    # Create response
    response = jsonify(new_company.to_dict())
    response.status_code = 201
    response.headers["Location"] = url_for("api.get_company", company_id=new_company.company_id)

    cache.clear()
    return response


@bp.route("/v1/companies/<int:company_id>", methods=["GET"])
@cache.cached(timeout=30, query_string=True)
def get_company(company_id):
    """GET     /v1/companies/:id   Returns company with specific company_id"""
    return jsonify(Companies.query.get_or_404(company_id).to_dict())


@bp.route("/v1/companies/<int:company_id>", methods=["PATCH"])
@jwt_required()
def update_company(company_id):
    """PATCH   /v1/companies/:id   Updates company with specific company_id"""
    company = Companies.query.get_or_404(company_id)

    data = request.get_json() or {}
    data["id_for_check_company"] = company.company_id

    # Validate input
    try:
        validated_data = CompaniesPatchSchema().load(data, partial=True)
    except ValidationError as err:
        return bad_request(err.messages)

    # Make the update in the DB for city and meta infor
    fields_in_related_tables = ["city_name", "disciplines", "branches", "tags"]
    for field in fields_in_related_tables:
        if field in validated_data:
            if field == "city_name":
                validated_data["city_id"] = insert_city(validated_data)
                validated_data.pop("city_name")
            if field in ["disciplines", "branches", "tags"]:
                db.session.execute(
                    "DELETE FROM companies_meta \
                        WHERE companies_meta.company_id = :id \
                            AND companies_meta.meta_id IN (SELECT Meta.meta_id \
                                FROM Meta WHERE Meta.type = :type)",
                    {"id": company_id, "type": field},
                )

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
    response.headers["Location"] = url_for("api.get_company", company_id=company_id)

    cache.clear()
    return response


@bp.route("/v1/companies/<int:company_id>", methods=["DELETE"])
@jwt_required()
def delete_company(company_id):
    """DELETE  /v1/companies/:id   Deletes company with specific company_id"""
    # Lookup company_id and delete if exists
    company = Companies.query.get_or_404(company_id)
    db.session.delete(company)
    db.session.commit()

    # Create response
    message = {}
    message["message"] = f"Company with company_id={company_id} has been deleted"
    response = jsonify(message)
    response.status_code = 200

    cache.clear()
    return response


@bp.route("/v1/upload", methods=["POST"])
@jwt_required()
def upload_file():
    if "file" not in request.files:
        return error_response(400, "No file key in request.files")

    img = request.files["file"]
    if img.filename == "":
        return error_response(400, "Please select a file")

    filename = secure_filename(img.filename)
    file_ext = os.path.splitext(filename)[1]

    if file_ext not in Config.UPLOAD_EXTENSIONS or file_ext != validate_image(img.stream):
        return error_response(400, f"Invalid file extension, please use .gif, .jpg or .png")

    output = {}
    output["url"] = str(upload_file_to_s3(img, Config.S3_BUCKET_NAME))

    response = jsonify(output)
    response.status_code = 201

    return response

    # TODO: We could also think about nameing the file ourselves...
    # uploaded_file.save(os.path.join('static/avatars', current_user.get_id()))
    # something like <company_id>_logo_<company_name>

    # Additionally, it overrides files with the same name already in the bucket
