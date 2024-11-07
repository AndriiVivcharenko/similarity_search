from typing import List

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance, ScoredPoint

from app.config import settings
from app.models.query_response import QueryMatch
from app.services.vector_db_service import IVectorDBService


class QDrantService(IVectorDBService):

    def __init__(self):
        self.qdrant = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
        )

        if not self.qdrant.collection_exists(collection_name=settings.qdrant_index_name):
            self.qdrant.create_collection(
                collection_name=settings.qdrant_index_name,
                vectors_config=VectorParams(
                    size=settings.pinecone_dimensions,
                    distance=Distance.COSINE
                )
            )

    def query_index(self, embedded_text, top_k=3) -> List[QueryMatch]:
        res: List[ScoredPoint] = self.qdrant.search(
            collection_name=settings.qdrant_index_name,
            query_vector=embedded_text,
            limit=top_k,
        )

        matches = []

        for item in res:
            matches.append(
                QueryMatch(
                    score=item.score,
                    text=item.payload.get("text"),
                )
            )

        return matches

    def upsert(self, id, embedding, text):
        self.qdrant.upsert(settings.qdrant_index_name, points=[
            PointStruct(
                id=id,
                vector=embedding,
                payload={"text": text}
            )
        ])

    def delete_all(self):
        self.qdrant.delete(settings.qdrant_index_name)
