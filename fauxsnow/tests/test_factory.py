from fauxsnow import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_coming_soon(client):
    response = client.get('/')
    assert b'Coming Soon' in response.data