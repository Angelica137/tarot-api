import pytest
from app import create_app, db


def test_hello_world(client):
    response = client.get('/api/')
    assert response.status_code == 200
    assert b"Welcome, login to continue" in response.data


def test_db_connection(client):
    response = client.get('/api/test_db')
    assert response.status_code == 200, "Database connection failed"
    data = response.get_json()
    assert "Database connection successful" in data['message']
