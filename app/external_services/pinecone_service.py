from typing import List

import pinecone

from app.config import settings
from app.external_services.vector_db_service import IVectorDBService
from app.models.query_response import QueryMatch


class PineconeService(IVectorDBService):

    def __init__(self):
        self.pc = pinecone.Pinecone(
            api_key=settings.pinecone_api_key,

        )

        if settings.pinecone_index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                settings.pinecone_index_name,
                dimension=settings.pinecone_dimensions,
                spec=pinecone.ServerlessSpec(
                    cloud=settings.pinecone_spec_cloud,
                    region=settings.pinecone_spec_region,
                )
            )

        self.index = self.pc.Index(settings.pinecone_index_name)

    def upsert(self, uid, embedding, text):
        self.index.upsert([(str(uid), embedding, {"text": text})])

    def delete_all(self):
        self.index.delete(delete_all=True)

    def query_index(self, embedded_text, top_k=3) -> List[QueryMatch]:
        query_results = self.index.query(
            vector=embedded_text,
            top_k=top_k,
            include_metadata=True
        )

        matches = []

        for result in query_results["matches"]:
            score = result['score']
            text = result["metadata"]["text"]
            matches.append(QueryMatch(
                score=score,
                text=text,
            ))

        return matches
