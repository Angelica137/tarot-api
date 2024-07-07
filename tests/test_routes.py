def test_hello_world(cleint):
    response = cleint.get('/')
    assert response.status_code == 200
    assert b"Hello, World!" in response.data