import pytest
from app import create_app, db


def test_db_connection(client):
    response = client.get("/dev/test_db")
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.data}")
    assert response.status_code == 200, f"Database connection failed: {response.data}"
    data = response.get_json()
    assert "Database connection successful" in data["message"]
