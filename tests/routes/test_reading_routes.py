import pytest
from app import db
from flask import json, session
from app.models.reading_model import Reading
from app import db
from app.auth.auth import AuthError
import json


@pytest.fixture
def mock_auth(mocker):
    mock = mocker.patch("app.auth.auth.verify_decode_jwt")
    mock.return_value = {
        "sub": "test_user_id",
        "permissions": [
            "get:readings",
            "get:reading-detail",
            "patch:question",
            "delete:reading",
        ],
    }
    return mock


@pytest.fixture
def mock_token():
    return "mock_token"


def test_get_readings_no_readings(client, mock_auth):
    response = client.get(
        "/api/readings/", headers={"Authorization": "Bearer mock_token"}
    )
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == "No readings found"


def test_get_readings_with_data(client, mock_auth):
    # Create a test reading
    test_reading = Reading(
        auth0_user_id="test_user_id",
        question="Test question?",
        spread_data=1,  # Adjust this based on your spread_data structure
    )
    db.session.add(test_reading)
    db.session.commit()

    try:
        response = client.get(
            "/api/readings/", headers={"Authorization": "Bearer mock_token"}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "readings" in data
        assert len(data["readings"]) > 0
        assert data["readings"][0]["question"] == "Test question?"
    finally:
        # Clean up: delete the test reading
        db.session.delete(test_reading)
        db.session.commit()


def test_get_readings_pagination(client, mock_auth):
    # Create multiple test readings
    for i in range(15):  # Creating 15 readings
        test_reading = Reading(
            auth0_user_id="test_user_id",
            question=f"Test question {i}?",
            spread_data=1,
        )
        db.session.add(test_reading)
    db.session.commit()

    try:
        # Test first page
        response = client.get(
            "/api/readings/?page=1&per_page=10",
            headers={"Authorization": "Bearer mock_token"},
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data["readings"]) == 10
        assert data["total"] == 15
        assert data["pages"] == 2
        assert data["current_page"] == 1

        # Test second page
        response = client.get(
            "/api/readings/?page=2&per_page=10",
            headers={"Authorization": "Bearer mock_token"},
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data["readings"]) == 5
        assert data["current_page"] == 2
    finally:
        # Clean up: delete all test readings
        Reading.query.filter_by(auth0_user_id="test_user_id").delete()
        db.session.commit()


def test_get_readings_forbidden(client, mock_auth):
    """
    GIVEN a Card instance
    WHEN to_dict() is called
    THEN it should return a dictionary with the card's data
    """
    # Override the mock to remove the 'get:readings' permission
    mock_auth.return_value = {
        "sub": "test_user_id",
        "permissions": [],  # No permissions
    }
    response = client.get(
        "/api/readings/", headers={"Authorization": "Bearer mock_token"}
    )
    assert response.status_code == 403


def test_get_readings_unauthorized(client):
    """
    GIVEN an unauthenticated user
    WHEN the user attempts to access the /api/readings/ endpoint without a token
    THEN the response should have a 401 Unauthorized status code
    """
    with pytest.raises(AuthError) as excinfo:
        client.get("/api/readings/")

    assert excinfo.value.status_code == 401
    assert excinfo.value.error == {
        "code": "authorization_header_missing",
        "description": "Authorization header is expected.",
    }


# GET:reading-detail
def test_get_reading_detail(client, mock_auth):
    mock_auth.return_value = {
        "sub": "test_user_id",
        "permissions": ["get:reading-detail"],
    }

    # Create a test reading
    test_reading = Reading(
        auth0_user_id="test_user_id",
        question="Test question?",
        spread_data=1,  # Adjust this based on your spread_data structure
    )
    db.session.add(test_reading)
    db.session.commit()

    try:
        response = client.get(
            f"/api/readings/{test_reading.id}",
            headers={"Authorization": "Bearer mock_token"},
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["id"] == test_reading.id
        assert data["question"] == "Test question?"
    finally:
        # Clean up: delete the test reading
        db.session.delete(test_reading)
        db.session.commit()


def test_get_reading_detail_not_found(client, mock_auth):
    mock_auth.return_value = {
        "sub": "test_user_id",
        "permissions": ["get:reading-detail"],
    }
    response = client.get(
        "/api/readings/9999", headers={"Authorization": "Bearer mock_token"}
    )
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
    assert "not found" in data["error"].lower()


def test_get_reading_detail_unauthorized(client, mock_auth):
    mock_auth.return_value = {
        "sub": "wrong_user_id",
        "permissions": ["get:reading-detail"],
    }
    # Create a reading that belongs to a different user
    test_reading = Reading(
        auth0_user_id="correct_user_id", question="Test question?", spread_data=1
    )
    db.session.add(test_reading)
    db.session.commit()

    try:
        response = client.get(
            f"/api/readings/{test_reading.id}",
            headers={"Authorization": "Bearer mock_token"},
        )
        assert response.status_code == 401
        data = json.loads(response.data)
        assert "error" in data
        assert "unauthorized" in data["error"].lower()
    finally:
        db.session.delete(test_reading)
        db.session.commit()


def test_get_reading_detail_forbidden(client, mock_auth):
    mock_auth.return_value = {
        "sub": "test_user_id",
        "permissions": [],  # No permissions
    }
    response = client.get(
        "/api/readings/1", headers={"Authorization": "Bearer mock_token"}
    )
    assert response.status_code == 403

    # Check if the response is HTML
    if "text/html" in response.content_type:
        assert "Forbidden" in response.data.decode()
        assert (
            "You don&#39;t have the permission to access the requested resource"
            in response.data.decode()
        )
    else:
        # If it's JSON, parse it
        data = json.loads(response.data)
        assert "error" in data
        assert "forbidden" in data["error"].lower()


# PATCH:question
def test_update_reading_question(client, mock_auth):
    mock_auth.return_value = {"sub": "test_user_id", "permissions": ["patch:question"]}

    # Create a test reading
    test_reading = Reading(
        auth0_user_id="test_user_id",
        question="Original question?",
        spread_data=1,  # Adjust this based on your spread_data structure
    )
    db.session.add(test_reading)
    db.session.commit()

    new_question = "Updated question?"
    try:
        response = client.patch(
            f"/api/readings/{test_reading.id}/question",
            headers={"Authorization": "Bearer mock_token"},
            json={"question": new_question},
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["message"] == "Reading question updated successfully"
        assert data["new_question"] == new_question
    finally:
        # Clean up: delete the test reading
        db.session.delete(test_reading)
        db.session.commit()


def test_update_reading_question_bad_request(client, mock_auth):
    mock_auth.return_value = {"sub": "test_user_id", "permissions": ["patch:question"]}

    # Create a test reading
    test_reading = Reading(
        auth0_user_id="test_user_id",
        question="Original question?",
        spread_data=1,  # Adjust this based on your spread_data structure
    )
    db.session.add(test_reading)
    db.session.commit()

    try:
        response = client.patch(
            f"/api/readings/{test_reading.id}/question",
            headers={"Authorization": "Bearer mock_token"},
            json={},  # Empty JSON to trigger bad request
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "not provided" in data["error"].lower()
    finally:
        # Clean up: delete the test reading
        db.session.delete(test_reading)
        db.session.commit()


def test_update_reading_question_forbidden(client, mock_auth):
    mock_auth.return_value = {
        "sub": "test_user_id",
        "permissions": [],  # No permissions
    }

    response = client.patch(
        "/api/readings/1/question",
        headers={"Authorization": "Bearer mock_token"},
        json={"question": "New question?"},
    )
    assert response.status_code == 403

    # Check if the response is HTML
    if "text/html" in response.content_type:
        assert "Forbidden" in response.data.decode()
    else:
        data = json.loads(response.data)
        assert "error" in data
        assert "forbidden" in data["error"].lower()


def test_update_reading_question_unauthorized(client, mock_auth):
    # Create a test reading for the correct user
    correct_reading = Reading(
        auth0_user_id="correct_user_id", question="Original question?", spread_data=1
    )
    db.session.add(correct_reading)
    db.session.commit()

    # Verify the reading was created
    print(f"Created reading with ID: {correct_reading.id}")

    # Check if the reading exists in the database
    check_reading = Reading.query.get(correct_reading.id)
    print(f"Reading in DB: {check_reading}")
    if check_reading:
        print(f"Reading auth0_user_id: {check_reading.auth0_user_id}")

    # Mock auth for a different user
    mock_auth.return_value = {"sub": "wrong_user_id", "permissions": ["patch:question"]}

    try:
        response = client.patch(
            f"/api/readings/{correct_reading.id}/question",
            headers={"Authorization": "Bearer mock_token"},
            json={"question": "New question?"},
        )
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")

        # Check for 401 or 404
        assert response.status_code in [401, 404]

        if response.status_code == 401:
            data = json.loads(response.data)
            assert "error" in data
            assert "unauthorized" in data["error"].lower()
        elif response.status_code == 404:
            data = json.loads(response.data)
            assert "error" in data
            assert "not found" in data["error"].lower()
    finally:
        # Clean up: delete the test reading
        db.session.delete(correct_reading)
        db.session.commit()
