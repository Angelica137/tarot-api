import datetime
import pytest
from app import create_app, db
from sqlalchemy.orm import scoped_session, sessionmaker
from app.models.reading_model import Reading
from unittest.mock import patch, Mock
from flask import session, abort
from app.routes.error_handlers import register_error_handlers


pytest_plugins = ["pytest_mock"]


@pytest.fixture(autouse=True)
def clear_db(session):
    session.query(Reading).delete()
    session.commit()
    yield


pytest_plugins = ["pytest_mock"]


def create_test_app():
    app = create_app("testing")
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SECRET_KEY"] = "test-secret-key"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"

    register_error_handlers(app)

    @app.route("/trigger_400")
    def trigger_400():
        abort(400, description="Bad request")

    @app.route("/trigger_401")
    def trigger_401():
        abort(401, description="Unauthorized")

    @app.route("/trigger_403")
    def trigger_403():
        abort(403, description="Forbidden")

    @app.route("/trigger_405", methods=["GET"])
    def trigger_405():
        return "This route only allows GET"

    @app.route("/trigger_500")
    def trigger_500():
        abort(500, description="Internal server error")

    return app


@pytest.fixture(scope="module")
def test_app():
    app = create_test_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="module")
def test_db(test_app):
    return db


@pytest.fixture(scope="module")
def client(test_app):
    return test_app.test_client(use_cookies=True)


@pytest.fixture(scope="function")
def session(test_db):
    connection = test_db.engine.connect()
    transaction = connection.begin()
    session_factory = sessionmaker(bind=connection)
    session = scoped_session(session_factory)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def sample_card_data():
    return {
        "name": "The Fool",
        "number": "0",
        "arcana": "Major Arcana",
        "suit": "Trump",
        "img": "m00.jpg",
        "fortune_telling": ["Watch for new projects and new beginnings"],
        "keywords": ["freedom"],
        "meanings": {"light": ["Freeing yourself from limitation"]},
        "archetype": "The Divine Madman",
        "hebrew_alphabet": "Aleph/Ox/1",
        "numerology": "0 (off the scale; pure potential)",
        "elemental": "Air",
        "mythical_spiritual": "Adam before the fall...",
        "questions_to_ask": ["What would I do if I felt free to take a leap?"],
        "affirmation": "I am open to all possibilities.",
        "astrology": "Uranus, Air",
    }


@pytest.fixture
def sample_reading_data():
    return {
        "id": 1,
        "question": "What do I need to know?",
        "user_id": 1,
        "spread_data": 1,
        "created_at": datetime(2021, 1, 1, 12, 0, 0),
        "updated_at": datetime(2021, 1, 1, 12, 0, 0),
    }


@pytest.fixture
def sample_spread_card_data():
    return {
        "id": 1,
        "position": 1,
        "position_name": "Past",
        "position_interpretation": "Sample interpretation",
        "spread_id": 1,
        "card_id": 1,
    }


@pytest.fixture
def sample_spread_data():
    return {"name": "Sample Spread", "number_of_cards": 5, "layout_id": 1}


@pytest.fixture
def sample_spread_layout_data():
    return {
        "id": 1,
        "name": "Three Card Spread",
        "layout_description": json.dumps(
            {
                "type": "linear",
                "positions": [
                    {"name": "Past", "x": 0, "y": 0},
                    {"name": "Present", "x": 1, "y": 0},
                    {"name": "Future", "x": 2, "y": 0},
                ],
            }
        ),
    }


@pytest.fixture
def sample_user_data():
    return {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "securepassword",
        "role": "user",
    }


@pytest.fixture
def session_app(test_app):
    with test_app.test_request_context():
        yield test_app


# Auth0 mock to test auth routes
@pytest.fixture
def mock_auth0_client(monkeypatch):
    mock_client = Mock()
    mock_client.authorize_redirect.return_value = "http://mock-redirect"
    monkeypatch.setattr("app.routes.auth_routes.get_auth0_client", lambda: mock_client)
    return mock_client


@pytest.fixture
def mock_config(monkeypatch):
    config = {
        "AUTH0_DOMAIN": "test.auth0.com",
        "AUTH0_CLIENT_ID": "test-client-id",
        "API_AUDIENCE": "test-audience",
        "APPLICATION_ROOT": "/",
        "SERVER_NAME": "localhost",
        "PREFERRED_URL_SCHEME": "http",
    }
    monkeypatch.setattr("flask.current_app.config", config)


@pytest.fixture
def mock_auth0(monkeypatch):
    mock = Mock()
    mock.authorize_redirect.return_value = "http://mock-redirect"
    monkeypatch.setattr("app.routes.auth_routes.get_auth0_client", lambda: mock)
    return mock


@pytest.fixture
def mock_config(monkeypatch):
    config = {
        "AUTH0_DOMAIN": "test.auth0.com",
        "AUTH0_CLIENT_ID": "test-client-id",
        "API_AUDIENCE": "test-audience",
    }
    monkeypatch.setattr("flask.current_app.config", config)
    return config
