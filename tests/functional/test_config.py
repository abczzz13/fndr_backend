import os
from flask import current_app


def test_testing_config(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the configuration for testing is requested
    THEN check that the configuratuon is valid
    """
    test_client.config.from_object('TestConfig')
    assert test_client.config['DEBUG']
    assert test_client.config['TESTING']
    assert not test_client.config['PRESERVE_CONTEXT_ON_EXCEPTION']
    assert test_client.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get(
        'DATABASE_TEST_URL')


def test_development_config(current_app):
    """
    GIVEN a Flask application configured for development
    WHEN the configuration for development is requested
    THEN check that the configuratuon is valid
    """
    current_app.config.from_object('config.DevelopmentConfig')
    assert current_app.config['DEBUG']
    assert not current_app.config['TESTING']
    assert current_app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get(
        'DATABASE_URL')


def test_production_config(app):
    """
    GIVEN a Flask application configured for production
    WHEN the configuration for production is requested
    THEN check that the configuratuon is valid
    """
    app.config.from_object('config.ProductionConfig')
    assert not app.config['DEBUG']
    assert not app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get(
        'DATABASE_URL')
