import json
from app import db
from app.models import Companies, Cities, Meta, companies_meta

# Variables
import_file = 'test.json'

# company_size enum dict
size = {
    '1-10': 'SMALL',
    '11-50': 'MEDIUM',
    '51-100': 'LARGE',
    'GT-100': 'XLARGE'
}

# region enum dict
provincie = {
    'Drenthe': 'DR',
    'Flevoland': 'FL',
    'Friesland': 'FR',
    'Gelderland': 'GD',
    'Groningen': 'GR',
    'Limburg': 'LB',
    'Noord-Brabant': 'NB',
    'Noord-Holland': 'NH',
    'Overijssel': 'OV',
    'Utrecht': 'UT',
    'Zuid-Holland': 'ZH',
    'Zeeland': 'ZL'
}

# Opening JSON file
file = open(import_file)

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

    # Meta: Disciplines
    # Check if disciplines is not empty
    if agency['disciplines'] is not None:

        # Iterate over the disciplines
        for discipline in agency['disciplines']:

            # Check if the discipline is already in the Meta table
            discipline_check = Meta.query.filter_by(
                type='Discipline', meta_string=discipline).first()

            # Add the discipline if not in Meta table
            if discipline_check is None:
                discipline_input = Meta(
                    type='Discipline', meta_string=discipline)
                db.session.add(discipline_input)
                db.session.commit()

                # Query the newly added discipline from the Meta table
                discipline_check = Meta.query.filter_by(
                    type='Discipline', meta_string=discipline).first()
            '''
            # Get the meta_id for the companies_meta table if the discipline was already in the table or just added to the table
            meta_id = discipline_check.meta_id

            # Add the company_id and meta_id to the companies_meta table
            # TODO: Probably have to do this a different way as this is a normal table...
            meta_input = companies_meta(meta_id=meta_id, company_id=company_id)
            db.session.add(meta_input)
            db.session.commit()
            '''

    # Meta: Branches
    # Check if branches is not empty
    if agency['branches'] is not None:

        # Iterate over the branches
        for branch in agency['branches']:

            # Check if the branch is already in the Meta table
            branch_check = Meta.query.filter_by(
                type='Branch', meta_string=branch).first()

            # Add the branch if not in Meta table
            if branch_check is None:
                branch_input = Meta(type='Branch', meta_string=branch)
                db.session.add(branch_input)
                db.session.commit()

                # Query the newly added branch from the Meta table
                branch_check = Meta.query.filter_by(
                    type='Branch', meta_string=branch).first()
            '''
            # Get the meta_id for the companies_meta table if the branch was already in the table or just added to the table
            meta_id = branch_check.meta_id

            # Add the company_id and meta_id to the companies_meta table
            # TODO: Probably have to do this a different way as this is a normal table...
            meta_input = companies_meta(meta_id=meta_id, company_id=company_id)
            db.session.add(meta_input)
            db.session.commit()
            '''

    # Meta: Tags
    # Check if tags is not empty
    if agency['tags'] is not None:

        # Iterate over the tags
        for tag in agency['tags']:

            # Check if the tag is already in the Meta table
            tag_check = Meta.query.filter_by(
                type='Tag', meta_string=tag).first()

            # Add the tag if not in Meta table
            if tag_check is None:
                tag_input = Meta(type='Tag', meta_string=tag)
                db.session.add(tag_input)
                db.session.commit()

                # Query the newly added tag from the Meta table
                tag_check = Meta.query.filter_by(
                    type='Tag', meta_string=tag).first()
            '''
            # Get the meta_id for the companies_meta table if the tag was already in the table or just added to the table
            meta_id = tag_check.meta_id

            # Add the company_id and meta_id to the companies_meta table
            # TODO: Probably have to do this a different way as this is a normal table...
            meta_input = companies_meta(meta_id=meta_id, company_id=company_id)
            db.session.add(meta_input)
            db.session.commit()

            # company = Company()
            # metas = Meta()
            # company.meta.append(metas)
            '''

    # print(f'id = {company_id}, name = {company_name}, company_size = {company_size}, region = {region}')
'''

# Closing the file
# Doesn't do anything?
import_file.close()
'''
