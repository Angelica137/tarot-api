import json
import pytest
from app.models.reading_model import Reading
from app import db


@pytest.fixture
def mock_auth(mocker):
    return mocker.patch("app.auth.auth.verify_decode_jwt")


@pytest.fixture
def mock_get_spread_data(mocker):
    return mocker.patch("app.routes.spread_routes.get_spread_data")


# GET /spreads/<int:spread_id>
def test_get_spread_success(client, mock_auth, mock_get_spread_data):
    mock_auth.return_value = {"sub": "test_user_id", "permissions": ["get:spread"]}
    mock_get_spread_data.return_value = {"id": 1, "name": "Test Spread"}

    response = client.get(
        "/api/spreads/1", headers={"Authorization": "Bearer mock_token"}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "id" in data
    assert "name" in data


def test_get_spread_with_question(client, mock_auth, mock_get_spread_data):
    mock_auth.return_value = {"sub": "test_user_id", "permissions": ["get:spread"]}
    mock_get_spread_data.return_value = {"id": 1, "name": "Test Spread"}

    response = client.get(
        "/api/spreads/1?question=Test%20Question",
        headers={"Authorization": "Bearer mock_token"},
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "question" in data
    assert data["question"] == "Test Question"


def test_get_spread_unauthorized(client, mock_auth):
    mock_auth.return_value = {"sub": "test_user_id", "permissions": []}
    response = client.get(
        "/api/spreads/1", headers={"Authorization": "Bearer mock_token"}
    )
    assert response.status_code == 403


# POST /spreads/<int:spread_id>
def test_save_reading_success(client, mock_auth, mock_get_spread_data):
    mock_auth.return_value = {"sub": "test_user_id", "permissions": ["post:spread"]}
    mock_get_spread_data.return_value = {"id": 1, "name": "Test Spread"}

    response = client.post(
        "/api/spreads/1",
        headers={"Authorization": "Bearer mock_token"},
        json={"question": "Test Question"},
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert "message" in data
    assert "reading_id" in data


def test_save_reading_no_user_id(client, mock_auth):
    mock_auth.return_value = {"permissions": ["post:spread"]}  # No 'sub' key
    response = client.post(
        "/api/spreads/1",
        headers={"Authorization": "Bearer mock_token"},
        json={"question": "Test Question"},
    )
    assert response.status_code == 401


def test_save_reading_spread_not_found(client, mock_auth, mock_get_spread_data):
    mock_auth.return_value = {"sub": "test_user_id", "permissions": ["post:spread"]}
    mock_get_spread_data.return_value = None

    response = client.post(
        "/api/spreads/1",
        headers={"Authorization": "Bearer mock_token"},
        json={"question": "Test Question"},
    )
    assert response.status_code == 404


def test_save_reading_db_error(client, mock_auth, mock_get_spread_data, mocker):
    mock_auth.return_value = {"sub": "test_user_id", "permissions": ["post:spread"]}
    mock_get_spread_data.return_value = {"id": 1, "name": "Test Spread"}

    # Mock db.session.commit to raise an exception
    mocker.patch("app.db.session.commit", side_effect=Exception("DB Error"))

    response = client.post(
        "/api/spreads/1",
        headers={"Authorization": "Bearer mock_token"},
        json={"question": "Test Question"},
    )
    assert response.status_code == 500
    data = json.loads(response.data)
    assert "error" in data


def test_save_reading_unauthorized(client, mock_auth):
    mock_auth.return_value = {"sub": "test_user_id", "permissions": []}
    response = client.post(
        "/api/spreads/1",
        headers={"Authorization": "Bearer mock_token"},
        json={"question": "Test Question"},
    )
    assert response.status_code == 403
