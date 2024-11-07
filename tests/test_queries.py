import random
from unittest.mock import MagicMock

import numpy as np
import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app, container
from app.models.query_response import QueryResponseModel, RestoreEmbeddingsResponseModel, QueryMatch
from app.services.transformer_service import TransformerService
from app.services.vector_db_service import IVectorDBService

client = TestClient(app)


@pytest.fixture()
def mock_vectordb_service():
    mock_vectordb = MagicMock(spec=IVectorDBService)

    db = []

    def query_index(embedded_text, top_k=3):
        return [
            QueryMatch(
                text=db[i].get("text"),
                score=random.uniform(0, 1),
            ) for i in range(min(len(db), top_k))
        ]

    def upsert(id, embedding, text):
        db.append({
            "id": id,
            "embedding": embedding,
            "text": text,
        })

    def delete_all():
        db.clear()

    mock_vectordb.query_index.side_effect = query_index
    mock_vectordb.upsert.side_effect = upsert
    mock_vectordb.delete_all.side_effect = delete_all

    return mock_vectordb


@pytest.fixture()
def mock_transformer_service():
    mock_transformer = MagicMock(spec=TransformerService)

    def embed_text(text):
        # return random numpy vector
        vector = np.array([])
        for _ in range(len(text)):
            vector = np.append(vector, np.random.random(len(text)))
        return vector

    mock_transformer.embed_text.side_effect = embed_text

    return mock_transformer

@pytest.fixture(autouse=True)
def populate_db(mock_vectordb_service, mock_transformer_service):
    mock_vectordb_service.delete_all()
    for i in range(10):
        text = str(i)
        mock_vectordb_service.upsert(
            id=i,
            embedding=mock_transformer_service.embed_text(text),
            text=text,
        )

@pytest.fixture(autouse=True)
def override_mock_vectordb_service(
        mock_vectordb_service,
        mock_transformer_service
):
    container.vectordb_service.override(mock_vectordb_service)
    container.transformer_service.override(mock_transformer_service)



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


def test_restore_embeddings_x_token():
    response = client.post('/query/restore_embeddings', headers={'x-token': settings.x_token})
    assert response.status_code == 200


def test_restore_embeddings_invalid_x_token():
    response = client.post('/query/restore_embeddings', headers={'x-token': "invalid"})
    assert response.status_code == 400


def test_restore_embeddings_empty_x_token():
    response = client.post('/query/restore_embeddings', headers={})
    assert response.status_code == 400


def test_restore_embeddings():
    response = client.post('/query/restore_embeddings', headers={'x-token': settings.x_token})
    assert response.status_code == 200

    res_model = RestoreEmbeddingsResponseModel(**response.json())

    assert res_model.number_of_embeddings > 0
