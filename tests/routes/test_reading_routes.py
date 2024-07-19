import pytest
from app import db
from flask import json
from app.models.reading_model import Reading
from app.models.user_model import User
from app.auth.auth import AuthError


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


@pytest.fixture
def test_user():
    # Setup: Create a user
    user = User(
        auth0_user_id="test_user_id", 
        email="test@example.com", 
        name="John Doe"  # Ensure this field is populated as it's non-nullable
    )
    db.session.add(user)
    db.session.commit()
    yield user
    # Teardown: Delete the user
    db.session.delete(user)
    db.session.commit()


def test_get_readings_no_readings(client, mock_auth, test_user):
    response = client.get(
        "/api/readings/", headers={"Authorization": "Bearer mock_token"}
    )
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == "No readings found"


def test_get_readings_with_data(client, mock_auth, test_user):
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


def test_get_readings_pagination(client, mock_auth, test_user):
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


def test_get_readings_forbidden(client, mock_auth, test_user):
    """
    # GIVEN a Card instance
    #WHEN to_dict() is called
    #THEN it should return a dictionary with the card's data
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
    response = client.get("/api/readings/")
    assert response.status_code == 401
    data = response.get_json()
    assert data['code'] == "authorization_header_missing"  # Corrected to match the actual output
    assert data['description'] == "Authorization header is expected."  # Ensure description matches too


# GET:reading-detail
def test_get_reading_detail(client, mock_auth, test_user):
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


def test_get_reading_detail_not_found(client, mock_auth, test_user):
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


def test_get_reading_detail_unauthorized(client, mock_auth, test_user):
    mock_auth.return_value = {
        "sub": "wrong_user_id",
        "permissions": ["get:reading-detail"],
    }
    
    # Create a user with the correct user ID
    correct_user = User(auth0_user_id="correct_user_id", name="Correct User", email="correct@example.com")
    db.session.add(correct_user)
    db.session.commit()

    # Create a reading that belongs to the correct user
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
        # Clean up: delete the test reading and the correct user
        db.session.delete(test_reading)
        db.session.delete(correct_user)
        db.session.commit()


def test_get_reading_detail_forbidden(client, mock_auth, test_user):
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
            "You don’t have the permission to access the requested resource"
            in response.data.decode()
        )
    else:
        # If it's JSON, parse it
        data = json.loads(response.data)
        assert data['code'] == "unauthorized"
        assert "permission not found" in data['description'].lower()


# PATCH:question
def test_update_reading_question(client, mock_auth, test_user):
    mock_auth.return_value = {"sub": "test_user_id", "permissions": ["patch:question"]}

    # Create a test reading
    test_reading = Reading(
        auth0_user_id="test_user_id",
        question="Original question?",
        spread_data=1,  # Assuming this is correct based on your database structure
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
        # Use 'reading_id' instead of 'id' to match the actual API response
        assert data["reading_id"] == test_reading.id
        assert data["new_question"] == new_question  # Ensure the new question matches what was sent
    finally:
        # Clean up: delete the test reading
        db.session.delete(test_reading)
        db.session.commit()


def test_update_reading_question_not_found(client, mock_auth, test_user):
    mock_auth.return_value = {"sub": "test_user_id", "permissions": ["patch:question"]}

    response = client.patch(
        "/api/readings/9999/question",
        headers={"Authorization": "Bearer mock_token"},
        json={"question": "Updated question?"},
    )
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
    assert "not found" in data["error"].lower()


# REALLY NOT SURE ABOUT THIS
def test_update_reading_question_forbidden(client, mock_auth, test_user):
    mock_auth.return_value = {"sub": "test_user_id", "permissions": []}  # No permissions

    response = client.patch(
        "/api/readings/1/question",
        headers={"Authorization": "Bearer mock_token"},
        json={"question": "Updated question?"},
    )
    assert response.status_code == 403

    # Check if the response is HTML
    if "text/html" in response.content_type:
        assert "Forbidden" in response.data.decode()
        assert (
            "You don’t have the permission to access the requested resource"
            in response.data.decode()
        )
    else:
        # If it's JSON, parse it
        data = json.loads(response.data)
        assert data['code'] == "unauthorized"
        assert "permission not found" in data['description'].lower()


def test_update_reading_question_unauthorized(client, mock_auth, test_user):
    mock_auth.return_value = {
        "sub": "wrong_user_id",
        "permissions": ["patch:question"],
    }

    # Ensure the correct user is in the database
    correct_user = User(auth0_user_id="correct_user_id", name="Correct User", email="correct@example.com")
    db.session.add(correct_user)
    db.session.commit()

    # Ensure the reading exists for the correct user
    test_reading = Reading(
        auth0_user_id="correct_user_id", question="Original question?", spread_data=1
    )
    db.session.add(test_reading)
    db.session.commit()

    new_question = "Updated question?"
    response = client.patch(
        f"/api/readings/{test_reading.id}/question",
        headers={"Authorization": "Bearer mock_token"},
        json={"question": new_question},
    )

    # Check response: should be 404 since user IDs do not match
    assert response.status_code == 404, "Expected a 404 Not Found due to user ID mismatch"
    assert "Reading not found or you don't have permission to update it" in response.get_json()["error"]


# DELETE:reading
def test_delete_reading(client, mock_auth, test_user):
    mock_auth.return_value = {"sub": "test_user_id", "permissions": ["delete:reading"]}

    # Create a test reading
    test_reading = Reading(
        auth0_user_id="test_user_id",
        question="Test question?",
        spread_data=1,  # Adjust this based on your spread_data structure
    )
    db.session.add(test_reading)
    db.session.commit()

    try:
        response = client.delete(
            f"/api/readings/{test_reading.id}",
            headers={"Authorization": "Bearer mock_token"},
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["message"] == "Reading successfully deleted"  # Update this line to match the actual message
    finally:
        # Clean up: ensure the reading is deleted
        if Reading.query.get(test_reading.id):
            db.session.delete(test_reading)
            db.session.commit()


def test_delete_reading_not_found(client, mock_auth, test_user):
    mock_auth.return_value = {"sub": "test_user_id", "permissions": ["delete:reading"]}

    response = client.delete(
        "/api/readings/9999", headers={"Authorization": "Bearer mock_token"}
    )
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
    assert "not found" in data["error"].lower()


def test_delete_reading_forbidden(client, mock_auth, test_user):
    mock_auth.return_value = {"sub": "test_user_id", "permissions": []}  # No permissions

    response = client.delete(
        "/api/readings/1", headers={"Authorization": "Bearer mock_token"}
    )
    assert response.status_code == 403

    data = json.loads(response.data)
    assert "code" in data
    assert data["code"] == "unauthorized"
    assert "description" in data
    assert "permission not found" in data["description"].lower()


def test_delete_reading_unauthorized(client, mock_auth, test_user):
    mock_auth.return_value = {
        "sub": "wrong_user_id",
        "permissions": ["delete:reading"],
    }

    # Create a reading that belongs to a different user
    test_reading = Reading(
        auth0_user_id="correct_user_id", question="Test question?", spread_data=1
    )
    db.session.add(test_reading)
    db.session.commit()

    try:
        response = client.delete(
            f"/api/readings/{test_reading.id}",
            headers={"Authorization": "Bearer mock_token"},
        )
        assert response.status_code == 403, "Expected forbidden status code when trying to delete a reading that does not belong to the authenticated user"
        data = json.loads(response.data)
        assert "error" in data
        assert "unauthorized to delete this reading" == data["error"].lower()
    finally:
        db.session.delete(test_reading)
        db.session.commit()

