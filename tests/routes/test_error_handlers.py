import pytest


def test_404_error(client):
    response = client.get('/non_existent_route')

    assert response.status_code == 404

    data = response.get_json()

    if data is None:
        print(
            "Response is not JSON. Content type:", response.headers.get(
                'Content-Type')
        )
        assert 'not found' in response.data.decode().lower()
    else:
        assert 'error' in data
        assert 'not found' in data['error'].lower()
