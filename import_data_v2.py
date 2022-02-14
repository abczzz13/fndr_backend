import json
from app import db
from app.models import Companies, Cities, Meta, companies_meta


# What to do with data validation? For SQL injections, SQLAlchemy takes care of that as long as you don't use any SQL syntax. In this case only SQL is used for the many-to-many companies_meta table, which is filled with Foreign Key id's created by the DB itself.
# What to do with errors?
# Maybe truncate DB before running script? Possibly with a check Y/N?
# Think about precautions when importing big files?


# Function to insert meta data
# Example insert_meta(agency['disciplines'], 'Discipline', company_id)
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


# Variables
import_file = 'db.json'

# Opening JSON file
with open(import_file) as file:

    # returns JSON object as
    # a dictionary
    data = json.load(file)

    # Iterating through the agencies in the json file
    for agency in data['agencies']:

        # Check if the city is already in the Cities table
        city_check = Cities.query.filter_by(city_name=agency['city']).first()

        # Add the city if city not in Cities table
        if city_check is None:

            # Create the insert for the Cities table and add it
            city_insert = Cities(
                city_name=agency['city'], region=agency['region'])
            db.session.add(city_insert)
            db.session.commit()

            # Query the newly added city from the Cities table
            city_check = city_insert

        # Get the city_id for the Companies table if the city was already in the table or just added to the table
        city_id = city_check.city_id

        # Create the insert for the company in the Companies table and add it
        company_insert = Companies(company_name=agency['name'], logo_image_src=agency['eguideImageSrc'], city_id=city_id,
                                   website=agency['website'], year=agency['yearEstablished'], company_size=agency['companySize'])
        db.session.add(company_insert)
        db.session.commit()

        # Insert meta information with insert_meta() function
        insert_meta(agency['disciplines'], 'Discipline',
                    company_insert.company_id)
        insert_meta(agency['branches'], 'Branch', company_insert.company_id)
        insert_meta(agency['tags'], 'Tag', company_insert.company_id)

# Closing the file
file.close()
