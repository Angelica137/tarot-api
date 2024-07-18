import pytest
import app
from flask import session


@pytest.fixture
def client(test_app):
    return test_app.test_client(use_cookies=True)


"""
@pytest.fixture(autouse=True)
def mock_session(monkeypatch):
    mock_dict = {}
    monkeypatch.setattr(session, '_get_current_object', lambda: mock_dict)
    return mock_dict
"""


@pytest.fixture
def mock_auth(mocker):
    mock = mocker.patch("app.auth.auth.verify_decode_jwt")
    mock.return_value = {"permissions": ["get:card"]}
    return mock


@pytest.fixture
def mock_token():
    return "mock_token"


def test_login_route(client):
    response = client.get("/api/login")
    print(f"\nLogin route status code: {response.status_code}")
    print(f"Login route data: {response.data}")
    assert response.status_code == 302  # Expecting a redirect


def test_callback_route(client, mocker):
    # Mock the get_auth0_client function
    # test wil not work withotut this
    mock_auth0 = mocker.patch("app.routes.auth_routes.get_auth0_client")
    mock_auth0.return_value.authorize_access_token.return_value = {
        "access_token": "mock_access_token",
        "id_token": "mock_id_token",
    }
    mock_auth0.return_value.get.return_value.json.return_value = {
        "sub": "mock_user_id",
    }

    # Set up the session state
    with client.session_transaction() as sess:
        sess["state"] = "test_state"

    # Make the request
    response = client.get("/api/callback?state=test_state")

    print(f"\nCallback route status code: {response.status_code}")
    print(f"Callback route data: {response.data}")

    # Assert the expected behavior
    assert response.status_code == 302  # Expecting a redirect
    assert response.location == "/api/"  # Check the redirect location

    # Verify that the session was updated correctly
    with client.session_transaction() as sess:
        assert "jwt_payload" in sess
        assert "profile" in sess
        assert "access_token" in sess
        assert sess["profile"]["user_id"] == "mock_user_id"


def test_logout_route(client):
    response = client.get("/api/logout")
    print(f"\nLogout route status code: {response.status_code}")
    print(f"Logout route data: {response.data}")
    assert response.status_code == 302  # Expecting a redirect


def test_print_routes(client):
    print("\nRegistered routes:")
    for rule in client.application.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule}")
