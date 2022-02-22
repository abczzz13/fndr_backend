from app.models import Companies, Cities, Meta, companies_meta, Users


def test_companies_model(client, init_testdb):
    '''
    GIVEN a Companies model
    WHEN a new company is created
    THEN check the company_id, company_name, logo_image_src, city_id, website, year, company_size
    '''
    company = Companies(company_name='Testing Company', logo_image_src='http://www.testing.com/image.png',
                        website='http://www.testing.com', year='2021', company_size='11-50')

    assert company.company_name == 'Testing Company'
    assert company.logo_image_src == 'http://www.testing.com/image.png'
    assert company.website == 'http://www.testing.com'
    assert company.year == '2021'
    assert company.company_size == '11-50'


def test_cities_model(client, init_testdb):
    '''
    GIVEN a Cities model
    WHEN a new city is created
    THEN check the city_id, city_name, region
    '''
    city = Cities(city_name='Verzonnen Stad', region='Noord-Holland')

    assert city.city_name == 'Verzonnen Stad'
    assert city.region == 'Noord-Holland'


def test_meta_model(client, init_testdb):
    '''
    GIVEN a Meta model
    WHEN a new meta is created
    THEN check the type, meta_string
    '''
    meta = Meta(type='Discipline', meta_string='Application Testing')

    assert meta.type == 'Discipline'
    assert meta.meta_string == 'Application Testing'


def test_users_model(client, init_testdb, new_user):
    '''
    GIVEN a Users model
    WHEN a new user is created
    THEN check the username, email, password
    '''

    assert new_user.username == 'Test User'
    assert new_user.email == 'test@fnder-backend.com'
    assert new_user.check_password('testtest')
