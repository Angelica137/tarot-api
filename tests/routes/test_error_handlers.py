import pytest
from flask import Flask, jsonify

# from app.routes.error_handlers import register_error_handlers


def test_400_bad_request(client):
    response = client.get("/trigger_400")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Bad request"


def test_401_unauthorized(client):
    response = client.get("/trigger_401")
    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] == "Unauthorized"


def test_403_forbidden(client):
    response = client.get("/trigger_403")
    assert response.status_code == 403
    data = response.get_json()
    assert data["error"] == "Forbidden"


def test_404_not_found(client):
    response = client.get("/non_existent_route")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Resource not found"


def test_405_method_not_allowed(client):
    response = client.post("/trigger_405")
    assert response.status_code == 405
    data = response.get_json()
    assert data["error"] == "Method not allowed"


def test_500_internal_server_error(client):
    response = client.get("/trigger_500")
    assert response.status_code == 500
    data = response.get_json()
    assert data["error"] == "Internal server error"


def test_404_error(client):
    response = client.get("/non_existent_route")
    assert response.status_code == 404
    data = response.get_json()
    if data is None:
        assert "not found" in response.data.decode().lower()
    else:
        assert "error" in data
        assert "not found" in data["error"].lower()
