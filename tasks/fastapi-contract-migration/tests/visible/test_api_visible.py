from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_health_ok() -> None:
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


def test_ask_happy_path_has_contract() -> None:
    payload = {'fen': '8/8/8/8/8/8/8/8 w - - 0 1'}
    response = client.post('/ask', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert 'answer' in data
    assert 'metadata' in data
    assert isinstance(data['metadata']['legal_moves_count'], int)
