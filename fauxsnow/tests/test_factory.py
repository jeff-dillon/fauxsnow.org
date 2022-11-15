from fauxsnow import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_coming_soon(client):
    response = client.get('/comingsoon')
    assert b'Coming Soon' in response.data

def test_about(client):
    response = client.get('/about')
    assert b'About' in response.data

def test_main(client):
    response = client.get('/')
    assert b'Ski' in response.data

def test_detail(client):
    response = client.get('/resort/paoli-peaks/')
    assert b'Paoli' in response.data