import os
# from flask import current_app
import pdb

'''
def test_testing_config(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the configuration for testing is requested
    THEN check that the configuratuon is valid
    """
    # client.config.from_object('TestConfig')
    pdb.set_trace()
    client.config.from_object()
    assert client.config['DEBUG']
    assert client.config['TESTING']
    assert not client.config['PRESERVE_CONTEXT_ON_EXCEPTION']
    assert client.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get(
        'DATABASE_TEST_URL')



def test_development_config(client):
    """
    GIVEN a Flask application configured for development
    WHEN the configuration for development is requested
    THEN check that the configuratuon is valid
    """
    client.config.from_object('config.DevelopmentConfig')
    assert client.config['DEBUG']
    assert not client.config['TESTING']
    assert client.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get(
        'DATABASE_URL')


def test_production_config(client):
    """
    GIVEN a Flask application configured for production
    WHEN the configuration for production is requested
    THEN check that the configuratuon is valid
    """
    client.config.from_object('config.ProductionConfig')
    assert not client.config['DEBUG']
    assert not client.config['TESTING']
    assert client.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get(
        'DATABASE_URL')
'''
