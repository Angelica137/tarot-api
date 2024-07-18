import pytest
import responses
from flask import session


@pytest.mark.parametrize("route", ["/api/login", "/api/logout", "/api/callback"])
@responses.activate
@pytest.mark.skip(reason="Skipping test for now due to unresolved configuration issue")
def test_auth_routes_exist(client, route):
    responses.add(
        responses.GET,
        "/.well-known/openid-configuration",
        json={"key": "value"},
        status=200,
    )
    responses.add(responses.GET, "/api/login", json={"key": "value"}, status=200)
    responses.add(responses.GET, "/api/logout", json={"key": "value"}, status=200)
    responses.add(responses.GET, "/api/callback", json={"key": "value"}, status=200)

    with client.session_transaction() as sess:
        sess["state"] = "test_state"
    response = client.get(route)
    assert response.status_code != 404, f"Route {route} not found"


@pytest.mark.skip(reason="Skipping test for now due to unresolved configuration issue")
def test_print_routes(client):
    print("\nRegistered routes:")
    for rule in client.application.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule}")


@pytest.mark.skip(reason="Skipping test for now due to unresolved configuration issue")
def test_print_config(test_app):
    print("\nApplication config:")
    for key, value in test_app.config.items():
        if not isinstance(value, dict) and not callable(value):
            print(f"{key}: {value}")
