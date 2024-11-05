from typing import List

from pydantic import BaseModel


class QueryMatch(BaseModel):
    score: float
    text: str


class QueryResponseModel(BaseModel):
    query: str
    matches: List[QueryMatch]


class RestoreEmbeddingsResponseModel(BaseModel):
    number_of_embeddings: int
    