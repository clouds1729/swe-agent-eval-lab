import os

from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_malformed_input_returns_controlled_error() -> None:
    response = client.post('/ask', json={'fen': 'bad'})
    assert response.status_code in {400, 422}
    body = response.json()
    assert 'traceback' not in str(body).lower()


def test_missing_model_returns_503_with_stable_shape(monkeypatch) -> None:
    monkeypatch.setenv('LOCAL_MODEL_AVAILABLE', '0')
    response = client.post('/ask', json={'fen': '8/8/8/8/8/8/8/8 w - - 0 1'})
    assert response.status_code == 503
    data = response.json()
    assert set(data.keys()) == {'answer', 'metadata'}
    assert isinstance(data['metadata']['model_available'], bool)
    assert isinstance(data['metadata']['legal_moves_count'], int)


def test_response_contract_is_stable_even_for_low_move_positions() -> None:
    response = client.post('/ask', json={'fen': 'xxx yyy'})
    # if accepted, response must preserve contract
    if response.status_code == 200:
        data = response.json()
        assert set(data.keys()) == {'answer', 'metadata'}
        assert isinstance(data['metadata'], dict)


def test_no_raw_exception_trace_leaks(monkeypatch) -> None:
    monkeypatch.setenv('LOCAL_MODEL_AVAILABLE', '0')
    response = client.post('/ask', json={'fen': '8/8/8/8/8/8/8/8 b - - 0 1'})
    assert 'RuntimeError' not in response.text
    assert 'Traceback' not in response.text
