import pytest
from app import create_app
from app.extensions import db
from app.models import Event

@pytest.fixture
def client(tmp_path, monkeypatch):
    # override database to a temp file
    db_file = tmp_path / 'test.sqlite3'
    monkeypatch.setenv('DATABASE_URL', f'sqlite:///{db_file}')
    app = create_app()
    client = app.test_client()
    with app.app_context():
        db.create_all()
    yield client

def test_health(client):
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.json == {'status': 'ok'}

def test_post_and_get_event(client):
    evt = {'event_type': 'click', 'timestamp': '2025-05-03T12:00:00Z', 'metadata': {'x': 1}}
    resp = client.post('/events', json=evt)
    assert resp.status_code == 200
    assert resp.json['inserted'] == 1

    resp2 = client.get('/events')
    assert resp2.status_code == 200
    assert len(resp2.json['events']) == 1
    assert resp2.json['events'][0]['event_type'] == 'click'
