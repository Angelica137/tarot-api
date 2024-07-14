import pytest
from app import db
from flask import json
from app.models.reading_model import Reading
from app.services.spread_service import get_spread_data
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token
from tests.conftest import clear_db


@pytest.fixture
def auth_headers():
    # Mock JWT token - in a real scenario, you'd generate a valid token
    access_token = create_access_token(identity=1)
    return {'Authorization': f'Bearer {access_token}'}


def test_simple_route(client):
    response = client.get('/api/test')
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == "Test route works"


def test_save_reading(client, auth_headers, session, mocker, sample_spread_data):
    mocker.patch('flask_jwt_extended.get_jwt_identity', return_value=1)
    mocker.patch('app.services.spread_service.get_spread_data', return_value=sample_spread_data)

    response = client.post('/api/readings', json={
        'question': 'Test question',
        'user_id': 1,
        'spread_data': sample_spread_data
    }, headers=auth_headers)

    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.data}")

    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'reading_id' in data
    assert data['message'] == 'Reading saved successfully'


def test_get_readings(client, auth_headers, session, mocker):
    mocker.patch('flask_jwt_extended.get_jwt_identity', return_value=1)

    # Add some test readings
    for i in range(15):
        reading = Reading(question=f'Test question {i}', user_id=1, spread_data={'mock': 'data'})
        session.add(reading)
    session.commit()

    response = client.get('/api/readings/', headers=auth_headers, follow_redirects=True)

    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['readings']) == 10  # default per_page
    assert data['total'] == 15
    assert data['pages'] == 2
    assert data['current_page'] == 1
    assert data['has_next'] is True
    assert data['has_prev'] is False


def test_get_reading(client, auth_headers, session, mocker):
    mocker.patch('flask_jwt_extended.get_jwt_identity', return_value=1)

    reading = Reading(question='Test question', user_id=1, spread_data={'mock': 'data'})
    session.add(reading)
    session.commit()

    response = client.get(f'/api/readings/{reading.id}', headers=auth_headers)

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['question'] == 'Test question'


def test_delete_reading(client, auth_headers, mocker, test_app):
    mocker.patch('flask_jwt_extended.get_jwt_identity', return_value=1)

    with test_app.app_context():
        reading = Reading(question='Test question', user_id=1, spread_data={'mock': 'data'})
        db.session.add(reading)
        db.session.commit()

        response = client.delete(f'/api/readings/{reading.id}', headers=auth_headers)

        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Reading deleted successfully'

        # Verify reading is deleted
        deleted_reading = db.session.query(Reading).get(reading.id)
        print(f"Deleted reading: {deleted_reading}")
        assert deleted_reading is None
