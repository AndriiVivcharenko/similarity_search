from fastapi.testclient import TestClient

from app.config import settings
from app.main import app
from app.models.query_response import QueryResponseModel

client = TestClient(app)


def test_query_empty_x_token():
    response = client.get('/query')
    assert response.status_code == 400


def test_query_invalid_x_token():
    response = client.get('/query', headers={'x-token': 'invalid'})
    assert response.status_code == 400


def test_query_x_token():
    response = client.get('/query', headers={'x-token': settings.x_token}, params={'q': 'test'})
    assert response.status_code == 200


def test_query_empty_q():
    response = client.get('/query', headers={'x-token': settings.x_token}, params={'q': ''})
    assert 400 <= response.status_code < 500


def test_query_top_k():
    response = client.get('/query', headers={'x-token': settings.x_token}, params={'q': "Explainable AI", "top_k": 1})
    assert response.status_code == 200

    res_model = QueryResponseModel(**response.json())
    assert len(res_model.matches) == 1
    assert res_model.query == 'Explainable AI'


def test_query_top_k_default():
    response = client.get('/query', headers={'x-token': settings.x_token}, params={'q': "Explainable AI"})
    assert response.status_code == 200
    
    res_model = QueryResponseModel(**response.json())
    assert len(res_model.matches) == 3
    assert res_model.query == 'Explainable AI'
    
    
