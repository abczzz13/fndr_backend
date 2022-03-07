import json
from app import db
from app.models import Companies, Cities, Meta, companies_meta

'''
Run within Flask Shell
Run the following commands in the Flask Shell:
from app.import_data_v2 import import_data
import_data('db.json')
'''


def insert_meta(meta_list, type, company_id):
    if meta_list is not None:

        for meta_string in meta_list:

            meta = Meta()
            meta_id = meta.get_or_create(meta_string, type)

            try:
                meta_input = f'INSERT INTO companies_meta (meta_id, company_id) VALUES ({meta_id}, {company_id}) ON CONFLICT DO NOTHING'
                db.session.execute(meta_input)
                db.session.commit()
            except:
                print(
                    f"Company ID ({company_id}) has duplicate meta ({meta_id})")
    return


def import_data(import_file):

    # Opening JSON file
    with open(import_file) as file:

        # returns JSON object as a dictionary
        data = json.load(file)
        cities = {}

        # Iterating through the agencies in the json file
        for agency in data['agencies']:

         # Validate region
            regions = ['Remote', 'Drenthe', 'Flevoland', 'Friesland', 'Gelderland', 'Groningen', 'Limburg',
                       'Noord-Brabant', 'Noord-Holland', 'Overijssel', 'Utrecht', 'Zuid-Holland', 'Zeeland']
            if agency['region'].title() in regions:
                region = agency['region'].title()
            else:
                region = 'Remote'

            # Validate company_size
            sizes = ['1-10', '11-50', '51-100', 'GT-100']
            if agency['companySize'] in sizes:
                company_size = agency['companySize']
            else:
                company_size = '1-10'

            # Check if the city is already in the cities dict
            if agency['city'].title() not in cities.values():

                # If city is not in the cities dict, add the city and company to the DB
                city_insert = Cities(
                    city_name=agency['city'].title(), region=region)
                company_insert = Companies(company_name=agency['name'].title(), logo_image_src=agency['eguideImageSrc'],
                                           website=agency['website'], year=agency['yearEstablished'], company_size=company_size)
                city_insert.company.append(company_insert)
                db.session.add(city_insert)
                db.session.commit()

                # Add the city_id and city_name to the cities dict:
                cities[city_insert.city_id] = city_insert.city_name

            # If city is in the cities dict, add the company with the city_id from the cities dict to the DB
            else:
                # Get the city_id
                city_id = [k for k, v in cities.items() if v ==
                           agency['city'].title()][0]

                # Insert the company into the DB
                company_insert = Companies(company_name=agency['name'].title(), logo_image_src=agency['eguideImageSrc'], city_id=city_id,
                                           website=agency['website'], year=agency['yearEstablished'], company_size=company_size)
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
