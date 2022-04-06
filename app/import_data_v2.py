import json
from app.utils_import import insert_city, insert_company, insert_meta


def import_data(import_file):

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
            insert_meta(agency["disciplines"], "disciplines", company_id)
            insert_meta(agency["branches"], "branches", company_id)
            insert_meta(agency["tags"], "tags", company_id)

    return
