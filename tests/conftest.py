import pytest
from app import create_app, db
from config import TestConfig
from app.models import Companies, Cities, Meta, companies_meta
import pdb
import os


@pytest.fixture(scope='module')
def client():

    flask_app = create_app(TestConfig)

    # Create a test client
    with flask_app.test_client() as test_client:

        # Establish the application context
        with flask_app.app_context():
            yield test_client


@pytest.fixture(scope='module')
def init_testdb(client):

    # Create the database
    db.create_all()

    # Return the DB
    yield db

    # Drop the DB after testing
    # db.drop_all()


'''
@pytest.fixture(scope='module')
def insert_data_db(client, init_testdb):

    # Insert some data
    company1 = Companies(company_name="Testing Company #1", logo_image_src="http://www.testing.com/image1.png",
                         website="http://www.testing.com/1", year="2021", company_size="1-10")
    company2 = Companies(company_name="Testing Company #2", logo_image_src="http://www.testing.com/image2.png",
                         website="http://www.testing.com/2", year="2022", company_size="11-50")

    city1 = Cities(city_name="Amsterdam", region="Noord-Holland")
    city2 = Cities(city_name="Rotterdam", region="Zuid-Holland")

    # city1.company.append(company1)
    # city2.company.append(company2)

    db.session.add(city1)
    db.session.add(city2)

    meta1 = Meta(type="Discipline", meta_string="IT")
    meta2 = Meta(type="Branch", meta_string="Backend")
    meta3 = Meta(type="Tag", meta_string="Python")
    db.session.add(meta1)
    db.session.add(meta2)
    db.session.add(meta3)

    db.session.commit()

    meta_input1 = f'INSERT INTO companies_meta (meta_id, company_id) VALUES (1, 2) ON CONFLICT DO NOTHING'
    meta_input2 = f'INSERT INTO companies_meta (meta_id, company_id) VALUES (3, 1) ON CONFLICT DO NOTHING'
    db.session.execute(meta_input1)
    db.session.execute(meta_input2)

    db.session.commit()


@pytest.fixture(scope='module')
def insert_data_db_script(client, init_testdb):
    insert_data()
'''
