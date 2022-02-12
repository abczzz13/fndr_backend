import json
from app import db
from app.models import Companies, Cities, Meta, companies_meta


# Function to insert meta data
# Example insert_meta(agency['disciplines'], 'Discipline')
def insert_meta(input, type):
    if input is not None:
        # Iterate over the disciplines
        for item in input:

            # Check if the discipline is already in the Meta table
            item_check = Meta.query.filter_by(
                type=type, meta_string=item).first()

            # Add the discipline if not in Meta table
            if item_check is None:
                item_input = Meta(type=type, meta_string=item)
                db.session.add(item_input)
                db.session.commit()

                # Query the newly added discipline from the Meta table
                item_check = Meta.query.filter_by(
                    type=type, meta_string=item).first()

            # Get the meta_id for the companies_meta table if the discipline was already in the table or just added to the table
            meta_id = item_check.meta_id

            # Add the company_id and meta_id to the companies_meta table
            meta_input = f'INSERT INTO companies_meta (meta_id, company_id) VALUES ({meta_id}, {company_id})'
            db.session.execute(meta_input)
            db.session.commit()
    return


# Variables
import_file = 'test.json'

# Opening JSON file
with open(import_file) as file:

    # returns JSON object as
    # a dictionary
    data = json.load(file)

    # Iterating through the agencies in the json file
    for agency in data['agencies']:

        # Check if the city is already in the Cities table
        city_name = agency['city']
        city_check = Cities.query.filter_by(city_name=city_name).first()

        # Add the city if city not in Cities table
        if city_check is None:

            # Get the values for the Cities table
            # city_name = agency['city']
            region = agency['region']

            # Create the insert for the Cities table and add it
            city_insert = Cities(city_name=city_name, region=region)
            db.session.add(city_insert)
            db.session.commit()

            # Query the newly added city from the Cities table
            city_check = Cities.query.filter_by(city_name=city_name).first()

        # Get the city_id for the Companies table if the city was already in the table or just added to the table
        city_id = city_check.city_id

        # Get the values for the Companies table
        company_id = agency['id']
        company_name = agency['name']
        logo_image_src = agency['eguideImageSrc']
        website = agency['website']
        year = agency['yearEstablished']
        company_size = agency['companySize']

        # Create the insert for the company in the Companies table and add it
        company_insert = Companies(company_name=company_name, logo_image_src=logo_image_src, city_id=city_id,
                                   website=website, year=year, company_size=company_size)
        db.session.add(company_insert)
        db.session.commit()

        # Insert meta information with insert_meta() function
        insert_meta(agency['disciplines'], 'Discipline')
        insert_meta(agency['branches'], 'Branch')
        insert_meta(agency['tags'], 'Tag')

# Closing the file
file.close()
