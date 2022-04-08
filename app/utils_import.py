""" This module provides custom utility functions importing data into the Database."""
import json
import os
from app import db
from app.models import Companies, Cities, Meta, Users
from app.utils import get_coordinates


def create_admin():
    """Create a new admin

    Parameters:
    No parameters can be provided, admin created will be hardcoded and based
    on environmental variables.

    Returns:
    """
    admin = Users(username=os.environ.get("ADMIN_USERNAME"), email=os.environ.get("ADMIN_EMAIL"))
    admin.set_password(os.environ.get("ADMIN_PW"))

    db.session.add(admin)
    db.session.commit()

    return


def insert_city(company_dict: dict) -> int:
    """Import the a city into the DB

    Parameters:
    company_dict (dict): a dictionary containing at least the city_name

    Returns:
    city_id (int)
    """
    # Correct for multiple inputs (import from json uses "city", API endpoints use "city_name" ):
    if "city_name" not in company_dict:
        company_dict["city_name"] = company_dict["city"]

    # Check if city already present in DB
    query = Cities.query.filter_by(city_name=company_dict["city_name"].title()).one_or_none()

    # Return city_id if city can be found
    if query is not None:
        return query.city_id

    # Else add the city
    else:
        regions = [
            "Remote",
            "Drenthe",
            "Flevoland",
            "Friesland",
            "Gelderland",
            "Groningen",
            "Limburg",
            "Noord-Brabant",
            "Noord-Holland",
            "Overijssel",
            "Utrecht",
            "Zuid-Holland",
            "Zeeland",
        ]
        if "region" not in company_dict or company_dict["region"] not in regions:
            company_dict["region"] = "Remote"

        coordinates = get_coordinates(company_dict["city_name"])

        city = Cities(
            city_name=company_dict["city_name"].title(),
            region=company_dict["region"],
            city_lat=coordinates["lat"],
            city_lng=coordinates["lng"],
        )

        # Insert into DB
        db.session.add(city)
        db.session.commit()

    return city.city_id


def insert_company(company_dict: dict, city_id: int) -> int:
    """Import the a company into the DB

    Parameters:
    dict (dict): a dictionary containing the company information

    Returns:
    company_id (int)
    """
    # Validate company_size
    sizes = ["1-10", "11-50", "51-100", "GT-100"]
    if company_dict["companySize"] in sizes:
        company_size = company_dict["companySize"]
    else:
        company_size = "1-10"

    # Prepare company_insert
    company = Companies(
        company_name=company_dict["name"].title(),
        logo_image_src=company_dict["eguideImageSrc"],
        city_id=city_id,
        website=company_dict["website"],
        year=company_dict["yearEstablished"],
        company_size=company_size,
    )

    # Insert into DB
    db.session.add(company)
    db.session.commit()

    return company.company_id


def insert_meta(meta_list: list, type: str, company_id: int):
    """Import the meta data of a certain type for a company into the DB

    Parameters:
    meta_list (list): a list of all the meta items for a certain meta_type
    type (str): the meta_type: disciplines, branches, tags
    company_id (int): the company_id for which the meta data is imported

    Returns:
    Imports the data into the DB
    """
    if meta_list:
        for meta_string in meta_list:
            meta = Meta()
            meta_id = meta.get_or_create(meta_string, type)

            try:
                meta_input = f"INSERT INTO companies_meta (meta_id, company_id) \
                                    VALUES ({meta_id}, {company_id}) \
                                        ON CONFLICT DO NOTHING"
                db.session.execute(meta_input)
                db.session.commit()
            except:
                print(f"Company ID ({company_id}) has duplicate meta ({meta_id})")
    return


def import_data(import_file: json):
    """Import the meta data of a certain type for a company into the DB

    Parameters:
    meta_list (list): a list of all the meta items for a certain meta_type
    type (str): the meta_type: disciplines, branches, tags
    company_id (int): the company_id for which the meta data is imported

    Returns:
    Imports the data into the DB
    """
    # Opening JSON file
    with open(import_file) as file:

        # returns JSON object as a dictionary
        data = json.load(file)

        # Iterating through the agencies in the json file
        for agency in data["agencies"]:

            # Insert the city and get the city_id
            city_id = insert_city(agency)

            # Insert the company and the company_id
            company_id = insert_company(agency, city_id)

            # Insert meta
            meta_types = ["tags", "branches", "disciplines"]
            for meta in meta_types:
                insert_meta(agency[meta], meta, company_id)

    return
