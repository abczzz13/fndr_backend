import json
from app import db
from app.models import Companies, Cities, Meta, companies_meta

'''
Run within Flask Shell
Run the following commands in the Flask Shell:
from app.import_data_v2 import import_data
import_data('db.json')
'''


# Function to insert meta data
# Example insert_meta(agency['disciplines'], 'disciplines', company_id)
def import_data(import_file):
    def insert_meta(input, type, company_id):
        if input is not None:
            # Iterate over the meta type
            for item in input:

                # Check if the meta string is already in the Meta table
                item_check = Meta.query.filter_by(
                    type=type, meta_string=item).first()

                # Add the meta string if not in Meta table
                if item_check is None:
                    item_input = Meta(type=type, meta_string=item)
                    db.session.add(item_input)
                    db.session.commit()

                    # Query the newly added meta string from the Meta table
                    item_check = item_input

                # Get the meta_id for the companies_meta table if the meta string was already in the table or just added to the table
                meta_id = item_check.meta_id

                # Add the company_id and meta_id to the companies_meta table
                try:
                    meta_input = f'INSERT INTO companies_meta (meta_id, company_id) VALUES ({meta_id}, {company_id}) ON CONFLICT DO NOTHING'
                    db.session.execute(meta_input)
                    db.session.commit()
                except:
                    print(
                        f"Company ID ({company_id}) has duplicate meta ({meta_id})")
        return

    # Opening JSON file
    with open(import_file) as file:

        # returns JSON object as
        # a dictionary
        data = json.load(file)
        cities = {}

        # Iterating through the agencies in the json file
        for agency in data['agencies']:

            # .strip() ? -> breaks it
            # Check if the city is already in the cities dict
            if agency['city'].capitalize() not in cities.values():
                # If city is not in the cities dict, add the city and company to the DB
                city_insert = Cities(
                    city_name=agency['city'].capitalize(), region=agency['region'])
                company_insert = Companies(company_name=agency['name'], logo_image_src=agency['eguideImageSrc'],
                                           website=agency['website'], year=agency['yearEstablished'], company_size=agency['companySize'])
                city_insert.company.append(company_insert)
                db.session.add(city_insert)
                db.session.commit()

                # Add the city_id and city_name to the cities dict:
                cities[city_insert.city_id] = city_insert.city_name

            # If city is in the cities dict, add the company with the city_id from the cities dict to the DB
            else:
                # Get the city_id
                city_id = [k for k, v in cities.items() if v ==
                           agency['city'].capitalize()][0]

                # Insert the company into the DB
                company_insert = Companies(company_name=agency['name'], logo_image_src=agency['eguideImageSrc'], city_id=city_id,
                                           website=agency['website'], year=agency['yearEstablished'], company_size=agency['companySize'])
                db.session.add(company_insert)
                db.session.commit()

            # Insert meta information with insert_meta() function
            insert_meta(agency['disciplines'], 'disciplines',
                        company_insert.company_id)
            insert_meta(agency['branches'], 'branches',
                        company_insert.company_id)
            insert_meta(agency['tags'], 'tags', company_insert.company_id)

    # Closing the file
    file.close()
