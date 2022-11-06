import sqlite3

import pytest
from fauxsnow.db import get_db, get_resorts, get_resort_by_id


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)

def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('fauxsnow.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called

def test_get_resorts(app):
    with app.app_context():
        db = get_db()
        resorts = get_resorts()
        assert len(resorts) == 2
        assert resorts[0]['state_short'] == 'IN'
        assert resorts[1]['state_short'] == 'NC'

def test_get_resort(app):
    with app.app_context():
        db = get_db()
        resort = get_resort_by_id('paoli-peaks')
        assert resort['state_short'] == 'IN'
        assert resort['sum_forecast_snow'] == 2