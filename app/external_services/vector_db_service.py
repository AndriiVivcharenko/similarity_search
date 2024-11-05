from abc import ABC, abstractmethod
from typing import List

from app.models.query_response import QueryMatch


class IVectorDBService(ABC):

    @abstractmethod
    def query_index(self, embedded_text, top_k=3) -> List[QueryMatch]:
        pass

    @abstractmethod
    def upsert(self, id, embedding, text):
        pass

    @abstractmethod
    def delete_all(self):
        pass
