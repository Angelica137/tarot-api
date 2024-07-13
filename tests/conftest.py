import pytest
from app import create_app, db
from sqlalchemy.orm import scoped_session, sessionmaker


@pytest.fixture(scope='module')
def test_app():
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_ECHO'] = True

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def test_db(test_app):
    return db


@pytest.fixture(scope='module')
def client(test_app):
    return test_app.test_client()


@pytest.fixture(scope='function')
def session(test_db):
    connection = test_db.engine.connect()
    transaction = connection.begin()
    session_factory = sessionmaker(bind=connection)
    session = scoped_session(session_factory)
    yield session
    session.close()
    transaction.rollback()
    connection.close()
