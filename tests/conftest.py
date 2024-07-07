import pytest
from app import create_app, db


"""
@pytest.fixture(scopre='module')
def test_client():
    flask_app = create_app('config.TestConfig')

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture(scope='module')
def init_database(test_cleint):
    db.create_all()
    # insert data
    # Add test data
    yield  # test
    db.drop_all()
"""