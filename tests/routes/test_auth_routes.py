import pytest
import responses
from flask import session
import os

@pytest.mark.parametrize("route", ["/api/login", "/api/logout", "/api/callback"])
@responses.activate
def test_auth_routes_exist(client, route):
    auth_domain = os.getenv('AUTH_DOMAIN', 'https://example.com')
    auth_well_known_url = f"{auth_domain}/.well-known/openid-configuration"

    # Mock the necessary auth0 URL
    responses.add(responses.GET, auth_well_known_url, json={'key': 'value'}, status=200)
    
    # Mock your API routes
    responses.add(responses.GET, f'{auth_domain}/api/login', json={'key': 'value'}, status=200)
    responses.add(responses.GET, f'{auth_domain}/api/logout', json={'key': 'value'}, status=200)
    responses.add(responses.GET, f'{auth_domain}/api/callback', json={'key': 'value'}, status=200)

    with client.session_transaction() as sess:
        sess["state"] = "test_state"
    response = client.get(route)
    print(f"Testing route: {route}, Response status code: {response.status_code}")
    assert response.status_code != 404, f"Route {route} not found"

def test_print_routes(client):
    print("\nRegistered routes:")
    for rule in client.application.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule}")

def test_print_config(test_app):
    print("\nApplication config:")
    for key, value in test_app.config.items():
        if not isinstance(value, dict) and not callable(value):
            print(f"{key}: {value}")


